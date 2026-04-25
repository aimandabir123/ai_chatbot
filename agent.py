"""
agent.py
Agentic engine using Groq native tool-calling (function calling).
Much more reliable than ReAct string parsing.

How it works:
1. Send user message + all tool definitions to Groq
2. Groq decides which tool to call (returns structured JSON)
3. We execute the tool and send the result back
4. Groq calls more tools or returns a Final Answer
5. Repeat up to MAX_ROUNDS times
"""

import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    HumanMessage, AIMessage, SystemMessage, ToolMessage
)

load_dotenv()

MAX_ROUNDS = 6  # maximum tool-call rounds per user message

SYSTEM_PROMPT = """You are an expert Apple product support agent.

You support four products:
- Apple Vision Pro (spatial computing headset)
- iPhone 15 Pro (flagship smartphone)
- MacBook Pro M3 (professional laptop)
- AirPods Pro 2 (premium wireless earbuds)

Your behaviour rules:
1. Use detect_product first to identify which product the customer needs help with.
2. Use search_knowledge_base to find accurate answers — never guess or make up information.
3. Use create_ticket when the issue cannot be resolved through knowledge base answers alone.
4. Use escalate_to_human_agent when the customer asks for a human or is very frustrated.
5. Use check_ticket_status when the customer provides a ticket ID like AP-XXXXXX.
6. Use compare_two_products when asked to compare two products.
7. Use get_product_details when asked general questions about a product.
8. Use record_customer_feedback when the customer rates their experience.

Always be helpful, concise, and professional.
Always base your answers on what the tools return — never invent information.
"""


def build_agent(tools: list) -> dict:
    """
    Build the tool-calling agent.
    Returns a dict containing the configured LLM and tool map.
    """
    groq_key   = os.getenv("GROQ_API_KEY", "").strip()
    groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()

    if not groq_key:
        raise ValueError(
            "\n❌  GROQ_API_KEY is not set!\n"
            "   1. Visit https://console.groq.com and sign up (free)\n"
            "   2. Go to API Keys and create a new key\n"
            "   3. Open backend/.env and set: GROQ_API_KEY=gsk_...\n"
            "   4. Restart the backend server\n"
        )

    print(f"   🤖 Groq model: {groq_model}")
    print(f"   🔧 Tools available: {len(tools)}")

    llm = ChatGroq(
        api_key=groq_key,
        model_name=groq_model,
        temperature=0.1,
        max_tokens=2048,
    )

    # Bind all tools to the LLM for native tool-calling
    llm_with_tools = llm.bind_tools(tools)

    return {
        "llm":           llm_with_tools,
        "llm_plain":     llm,                           # fallback without tools
        "tools_by_name": {t.name: t for t in tools},
        "model":         groq_model,
    }


def new_memory() -> list:
    """Create a fresh conversation memory (list of LangChain messages)."""
    return []


def chat(agent: dict, memory: list, user_message: str) -> dict:
    """
    Process one user message through the agentic pipeline.

    Args:
        agent:        output of build_agent()
        memory:       list of previous messages (modified in-place)
        user_message: the customer's text

    Returns:
        {
            "output":     str   — the agent's final response
            "tools_used": list  — names of tools that were called
            "steps":      list  — [{tool, input, output}, ...]
        }
    """
    llm           = agent["llm"]
    llm_plain     = agent["llm_plain"]
    tools_by_name = agent["tools_by_name"]

    steps      = []
    tools_used = []

    # Build the message list: system prompt + recent history + new message
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages += memory[-14:]                             # keep last 7 exchanges
    messages.append(HumanMessage(content=user_message))

    # ── Agentic loop ─────────────────────────────────────────
    for round_num in range(MAX_ROUNDS):

        # Call the LLM
        try:
            response = llm.invoke(messages)
        except Exception as err:
            print(f"   ⚠️  LLM call failed on round {round_num}: {err}")
            # Fall back to plain LLM (no tools) so we always give an answer
            try:
                fallback_msgs = [SystemMessage(content=SYSTEM_PROMPT)]
                fallback_msgs += memory[-6:]
                fallback_msgs.append(HumanMessage(content=user_message))
                fallback = llm_plain.invoke(fallback_msgs)
                answer   = fallback.content or "I'm sorry, please try again."
            except Exception as err2:
                print(f"   ⚠️  Fallback also failed: {err2}")
                answer = (
                    "I'm having trouble connecting to the AI service right now. "
                    "Please try again in a moment, or contact Apple Support at 1-800-APL-CARE."
                )
            _save_to_memory(memory, user_message, answer)
            return {"output": answer, "tools_used": [], "steps": []}

        messages.append(response)

        # Check if Groq wants to call any tools
        tool_calls = getattr(response, "tool_calls", None) or []

        if not tool_calls:
            # No tool calls — Groq has given the final answer
            answer = (response.content or "").strip()
            if not answer:
                answer = "I've completed the lookup. Is there anything else I can help you with?"
            break

        # ── Execute each requested tool ───────────────────────
        for tc in tool_calls:
            tool_name = tc.get("name", "")
            tool_args = tc.get("args", {})
            tool_id   = tc.get("id", f"call_{round_num}_{tool_name}")

            print(f"   🔧 [{round_num + 1}] {tool_name}({str(tool_args)[:80]})")

            # Find and call the tool
            if tool_name not in tools_by_name:
                tool_result = f"Error: tool '{tool_name}' does not exist."
            else:
                try:
                    tool_fn = tools_by_name[tool_name]

                    # Handle different argument shapes
                    if not tool_args:
                        tool_result = tool_fn.invoke("")
                    elif isinstance(tool_args, dict):
                        if len(tool_args) == 1:
                            # Single-argument tool — pass the value directly
                            tool_result = tool_fn.invoke(list(tool_args.values())[0])
                        else:
                            # Multi-argument tool — pass the dict
                            tool_result = tool_fn.invoke(tool_args)
                    else:
                        tool_result = tool_fn.invoke(str(tool_args))

                except Exception as tool_err:
                    tool_result = f"Tool execution error: {tool_err}"
                    print(f"   ⚠️  Tool {tool_name} raised: {tool_err}")

            result_str = str(tool_result)
            print(f"   📋 Result: {result_str[:100]}...")

            # Record the step for display in the UI
            steps.append({
                "tool":   tool_name,
                "input":  str(tool_args)[:200],
                "output": result_str[:300],
            })
            tools_used.append(tool_name)

            # Feed the tool result back to the LLM
            messages.append(
                ToolMessage(content=result_str, tool_call_id=tool_id)
            )

    else:
        # Reached MAX_ROUNDS without a final answer
        answer = (
            "I have finished gathering information. "
            "Here is what I found. Please let me know if you need more details."
        )

    # ── Save exchange to memory ───────────────────────────────
    _save_to_memory(memory, user_message, answer)

    # Deduplicate tools_used while preserving order
    seen = set()
    unique_tools = []
    for t in tools_used:
        if t not in seen:
            seen.add(t)
            unique_tools.append(t)

    return {
        "output":     answer,
        "tools_used": unique_tools,
        "steps":      steps,
    }


def _save_to_memory(memory: list, user_msg: str, bot_msg: str):
    """Append exchange to memory and trim to last 20 messages."""
    memory.append(HumanMessage(content=user_msg))
    memory.append(AIMessage(content=bot_msg))
    if len(memory) > 20:
        del memory[:-20]
