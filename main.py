"""
main.py
FastAPI server — all API routes for the agentic multi-product chatbot.

Run with:
    uvicorn main:app --reload --port 8000
"""

import uuid
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from products       import PRODUCTS, PRODUCT_FAQ
from knowledge_base import build_vector_store
from tools          import inject, ALL_TOOLS
from agent          import build_agent, new_memory, chat as agent_chat
from sentiment      import analyze
from ticket_manager import TicketManager
from analytics      import Analytics

# ── App setup ─────────────────────────────────────────────────
app = FastAPI(
    title="Apple AI Support Agent",
    description="Agentic chatbot with tool-calling — 4 products, 8 tools, Groq LLM",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global state ──────────────────────────────────────────────
_vector_store  = None
_agent         = None
_ticket_mgr    = TicketManager()
_analytics     = Analytics()
_sessions: dict[str, dict] = {}


@app.on_event("startup")
async def startup():
    global _vector_store, _agent
    print("\n" + "=" * 50)
    print("  Apple AI Support Agent — Starting up")
    print("=" * 50)
    print(f"  Products: {', '.join(p['name'] for p in PRODUCTS.values())}")

    _vector_store = build_vector_store()
    inject(_vector_store, _ticket_mgr, _analytics)
    _agent = build_agent(ALL_TOOLS)

    print(f"  Tools: {len(ALL_TOOLS)}")
    print("=" * 50)
    print("  ✅  Agent is ready!")
    print("  📖  API docs: http://localhost:8000/docs")
    print("=" * 50 + "\n")


# ── Request / Response models ─────────────────────────────────
class ChatRequest(BaseModel):
    message:    str
    session_id: Optional[str] = None

class TicketRequest(BaseModel):
    name:        str
    email:       str
    product:     str
    category:    str
    priority:    str
    description: str
    session_id:  Optional[str] = None

class FeedbackRequest(BaseModel):
    session_id: str
    message_id: str
    rating:     int


# ── Health / Info ─────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "status":   "online",
        "agent":    "Apple AI Support Agent",
        "products": len(PRODUCTS),
        "tools":    len(ALL_TOOLS),
        "model":    _agent["model"] if _agent else "not ready",
        "docs":     "http://localhost:8000/docs",
    }


@app.get("/health")
def health():
    return {
        "status":          "healthy",
        "agent_ready":     _agent is not None,
        "vector_store":    _vector_store is not None,
        "active_sessions": len(_sessions),
        "total_tickets":   len(_ticket_mgr.list_all()),
    }


# ── Chat ──────────────────────────────────────────────────────
@app.post("/chat")
def chat(req: ChatRequest):
    """
    Send a message to the AI agent.
    The agent will autonomously detect the product, search the knowledge base,
    create tickets, escalate to humans, and more — all decided by the LLM.
    """
    if not _agent:
        raise HTTPException(status_code=503, detail="Agent not ready yet. Please wait.")

    # Get or create session
    sid = req.session_id or str(uuid.uuid4())
    if sid not in _sessions:
        _sessions[sid] = {
            "memory":     new_memory(),
            "product":    None,
            "turn_count": 0,
            "tools_seen": [],
            "started_at": datetime.datetime.utcnow().isoformat(),
        }
    sess = _sessions[sid]
    sess["turn_count"] += 1

    # Run the agent
    try:
        result = agent_chat(_agent, sess["memory"], req.message)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    answer     = result["output"]
    tools_used = result["tools_used"]
    steps      = result["steps"]

    # Analytics
    sent = analyze(req.message)
    _analytics.track(sid, req.message, answer, sent, tools_used)

    # Update session product if detected
    detected = _extract_product(steps)
    if detected:
        sess["product"] = detected
    sess["tools_seen"].extend(tools_used)

    import os
    return {
        "session_id":   sid,
        "response":     answer,
        "tools_used":   tools_used,
        "steps":        steps,
        "product":      sess.get("product"),
        "sentiment":    sent,
        "turn_count":   sess["turn_count"],
        "model":        _agent["model"],
        "timestamp":    datetime.datetime.utcnow().isoformat(),
    }


# ── Products ──────────────────────────────────────────────────
@app.get("/products")
def get_products():
    return {
        "products": [
            {
                "id":        pid,
                "name":      p["name"],
                "emoji":     p["emoji"],
                "color":     p["color"],
                "category":  p["category"],
                "price":     p["price"],
                "faq_count": sum(len(c["questions"]) for c in PRODUCT_FAQ.get(pid, [])),
            }
            for pid, p in PRODUCTS.items()
        ]
    }


# ── FAQ ───────────────────────────────────────────────────────
@app.get("/faq")
def get_all_faq():
    return {
        "products": [
            {
                "product_id":   pid,
                "product_name": PRODUCTS[pid]["name"],
                "emoji":        PRODUCTS[pid]["emoji"],
                "categories":   PRODUCT_FAQ[pid],
            }
            for pid in PRODUCT_FAQ
        ]
    }


@app.get("/faq/{product_id}")
def get_product_faq(product_id: str):
    if product_id not in PRODUCT_FAQ:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    return {
        "product":    PRODUCTS[product_id],
        "categories": PRODUCT_FAQ[product_id],
    }


# ── Tools info ────────────────────────────────────────────────
@app.get("/tools")
def get_tools():
    return {
        "tools": [
            {
                "name":        t.name,
                "description": (t.description or "")[:200],
            }
            for t in ALL_TOOLS
        ]
    }


# ── Tickets ───────────────────────────────────────────────────
@app.post("/ticket")
def create_ticket(req: TicketRequest):
    ticket = _ticket_mgr.create(
        name=req.name,
        email=req.email,
        product=req.product,
        category=req.category,
        priority=req.priority,
        description=req.description,
        session_id=req.session_id,
    )
    return {"success": True, "ticket": ticket}


@app.get("/tickets")
def list_tickets():
    return {"tickets": _ticket_mgr.list_all()}


@app.get("/ticket/{ticket_id}")
def get_ticket(ticket_id: str):
    t = _ticket_mgr.get(ticket_id.upper())
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return t


# ── Feedback ──────────────────────────────────────────────────
@app.post("/feedback")
def submit_feedback(req: FeedbackRequest):
    _analytics.record_feedback(req.session_id, req.message_id, req.rating)
    return {"success": True}


# ── Analytics ─────────────────────────────────────────────────
@app.get("/analytics")
def get_analytics():
    return _analytics.summary()


# ── Sessions ─────────────────────────────────────────────────
@app.get("/sessions")
def get_sessions():
    return {
        "sessions": [
            {
                "id":         sid,
                "product":    s.get("product"),
                "turns":      s.get("turn_count", 0),
                "tools_used": list(set(s.get("tools_seen", []))),
                "started_at": s.get("started_at"),
            }
            for sid, s in _sessions.items()
        ]
    }


# ── Helper ────────────────────────────────────────────────────
def _extract_product(steps: list) -> Optional[str]:
    """Try to extract the detected product ID from agent steps."""
    for step in steps:
        if step.get("tool") == "detect_product":
            output = step.get("output", "")
            for pid, p in PRODUCTS.items():
                if p["name"].lower() in output.lower():
                    return pid
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
