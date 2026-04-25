"""
tools.py
All 8 tools the AI agent can call autonomously.
Uses LangChain @tool decorator — compatible with Groq tool-calling.
"""

import uuid
from langchain.tools import tool
from products import PRODUCTS, PRODUCT_FAQ

# ── Dependencies injected at startup ─────────────────────────
_vector_store = None
_ticket_mgr   = None
_analytics    = None


def inject(vector_store, ticket_manager, analytics_tracker):
    """Call this once at app startup to wire up shared state."""
    global _vector_store, _ticket_mgr, _analytics
    _vector_store = vector_store
    _ticket_mgr   = ticket_manager
    _analytics    = analytics_tracker


# ════════════════════════════════════════════════════════════
#  TOOL 1 — Search knowledge base
# ════════════════════════════════════════════════════════════
@tool
def search_knowledge_base(query: str) -> str:
    """Search the Apple product knowledge base for accurate answers.
    Use this for any question about product features, setup steps,
    troubleshooting, battery, camera, connectivity, or specifications.
    Input should be the customer's question or relevant keywords."""
    if _vector_store is None:
        return "Knowledge base is not available right now."
    try:
        docs = _vector_store.similarity_search(query, k=4)
        if not docs:
            return "No relevant information found for that query."
        parts = []
        for i, doc in enumerate(docs, 1):
            m = doc.metadata
            parts.append(
                f"[Result {i}] {m.get('product_name','Apple')} — {m.get('category','General')}:\n"
                f"{doc.page_content}"
            )
        return "\n\n".join(parts)
    except Exception as e:
        return f"Search failed: {e}"


# ════════════════════════════════════════════════════════════
#  TOOL 2 — Detect which product the customer needs help with
# ════════════════════════════════════════════════════════════
@tool
def detect_product(customer_message: str) -> str:
    """Detect which Apple product the customer is asking about.
    Always call this first on a new conversation.
    Input should be the full customer message."""
    msg    = customer_message.lower()
    scores = {}
    for pid, pdata in PRODUCTS.items():
        score = sum(1 for kw in pdata["keywords"] if kw in msg)
        if score > 0:
            scores[pid] = score

    if not scores:
        names = ", ".join(p["name"] for p in PRODUCTS.values())
        return (
            "Could not detect a specific product from the message. "
            f"Supported products are: {names}. "
            "Please ask the customer which product they need help with."
        )

    best = max(scores, key=scores.get)
    p    = PRODUCTS[best]
    return (
        f"Detected product: {p['emoji']} {p['name']} | "
        f"ID: {best} | Category: {p['category']} | Price: {p['price']}"
    )


# ════════════════════════════════════════════════════════════
#  TOOL 3 — Create support ticket
# ════════════════════════════════════════════════════════════
@tool
def create_ticket(
    customer_name: str,
    customer_email: str,
    product_name: str,
    issue_description: str,
    priority: str = "Medium",
) -> str:
    """Create a support ticket when the issue cannot be resolved through knowledge base answers,
    when the customer requests human support, or when the customer is very frustrated.
    Priority options: Low, Medium, High, Critical."""
    if _ticket_mgr is None:
        return "Ticket system is not available right now."
    try:
        ticket = _ticket_mgr.create(
            name=customer_name,
            email=customer_email,
            product=product_name,
            category="AI Agent — Auto Created",
            priority=priority,
            description=issue_description,
        )
        return (
            f"Support ticket created! "
            f"Ticket ID: {ticket['id']} | "
            f"Product: {product_name} | "
            f"Priority: {priority} | "
            f"SLA: {ticket['sla']} | "
            f"Assigned to: {ticket['assigned_to']} | "
            f"Confirmation will be sent to: {customer_email}"
        )
    except Exception as e:
        return f"Could not create ticket: {e}"


# ════════════════════════════════════════════════════════════
#  TOOL 4 — Check ticket status
# ════════════════════════════════════════════════════════════
@tool
def check_ticket_status(ticket_id: str) -> str:
    """Look up the current status of an existing support ticket.
    Use when the customer provides a ticket ID like AP-ABC123.
    Input should be the ticket ID string."""
    if _ticket_mgr is None:
        return "Ticket system is not available right now."
    ticket = _ticket_mgr.get(ticket_id.strip().upper())
    if not ticket:
        return (
            f"No ticket found with ID '{ticket_id}'. "
            "Please double-check the ticket ID and try again."
        )
    return (
        f"Ticket {ticket['id']}: "
        f"Status = {ticket['status']} | "
        f"Product = {ticket.get('product', 'N/A')} | "
        f"Priority = {ticket['priority']} | "
        f"SLA = {ticket['sla']} | "
        f"Assigned to = {ticket['assigned_to']} | "
        f"Created = {ticket['created_at'][:19]}"
    )


# ════════════════════════════════════════════════════════════
#  TOOL 5 — Get product details
# ════════════════════════════════════════════════════════════
@tool
def get_product_details(product_name: str) -> str:
    """Get detailed information about an Apple product including specs, price, and support topics.
    Use when the customer asks 'what is X', 'tell me about X', or 'what does X do'.
    Input should be the product name or one of: vision_pro, iphone_15_pro, macbook_pro_m3, airpods_pro"""
    query = product_name.lower().strip().replace(" ", "_").replace("-", "_")

    # Try exact match first
    pid = None
    if query in PRODUCTS:
        pid = query
    else:
        # Fuzzy match by name or keywords
        for k, p in PRODUCTS.items():
            if (query in p["name"].lower() or
                    p["name"].lower() in query or
                    any(kw in query for kw in p["keywords"])):
                pid = k
                break

    if pid is None:
        return (
            f"Product '{product_name}' not found. "
            f"Available products: {', '.join(p['name'] for p in PRODUCTS.values())}"
        )

    p         = PRODUCTS[pid]
    categories= [c["category"] for c in PRODUCT_FAQ.get(pid, [])]
    faq_count = sum(len(c["questions"]) for c in PRODUCT_FAQ.get(pid, []))

    return (
        f"{p['emoji']} {p['name']} | "
        f"Category: {p['category']} | "
        f"Starting price: {p['price']} | "
        f"Support topics: {', '.join(categories)} | "
        f"Total FAQ entries: {faq_count}"
    )


# ════════════════════════════════════════════════════════════
#  TOOL 6 — Compare two products
# ════════════════════════════════════════════════════════════
@tool
def compare_two_products(first_product: str, second_product: str) -> str:
    """Compare two Apple products side by side.
    Use when the customer asks 'what is the difference between X and Y'
    or 'should I buy X or Y'.
    Inputs should be product names."""

    def find_product(query: str):
        q = query.lower().strip().replace(" ", "_").replace("-", "_")
        if q in PRODUCTS:
            return q, PRODUCTS[q]
        for pid, pdata in PRODUCTS.items():
            if (q in pdata["name"].lower() or
                    pdata["name"].lower() in q or
                    any(kw in q for kw in pdata["keywords"])):
                return pid, pdata
        return None, None

    id_a, pa = find_product(first_product)
    id_b, pb = find_product(second_product)

    if not pa:
        return f"Could not find product '{first_product}'."
    if not pb:
        return f"Could not find product '{second_product}'."

    qa = sum(len(c["questions"]) for c in PRODUCT_FAQ.get(id_a, []))
    qb = sum(len(c["questions"]) for c in PRODUCT_FAQ.get(id_b, []))

    return (
        f"Comparison: {pa['emoji']} {pa['name']} vs {pb['emoji']} {pb['name']} — "
        f"{pa['name']}: category={pa['category']}, price={pa['price']}, {qa} FAQ entries. "
        f"{pb['name']}: category={pb['category']}, price={pb['price']}, {qb} FAQ entries."
    )


# ════════════════════════════════════════════════════════════
#  TOOL 7 — Escalate to human agent
# ════════════════════════════════════════════════════════════
@tool
def escalate_to_human_agent(reason: str, urgency: str = "Normal") -> str:
    """Escalate the conversation to a live human support agent.
    Use when the customer explicitly asks for a human, when multiple
    troubleshooting steps have failed, or when the issue involves
    safety, legal, or hardware damage concerns.
    Urgency options: Normal, High, Urgent."""
    ref    = "ESC-" + uuid.uuid4().hex[:6].upper()
    waits  = {"Normal": "2 to 4 hours", "High": "30 to 60 minutes", "Urgent": "10 to 15 minutes"}
    wait   = waits.get(urgency, "2 to 4 hours")

    return (
        f"Escalation confirmed. Reference number: {ref} | "
        f"Urgency: {urgency} | "
        f"Expected wait time: {wait} | "
        f"Contact Apple Support: call 1-800-APL-CARE or visit getsupport.apple.com | "
        f"Please share reference number {ref} when you connect with the agent. "
        f"Reason logged: {reason}"
    )


# ════════════════════════════════════════════════════════════
#  TOOL 8 — Record customer feedback
# ════════════════════════════════════════════════════════════
@tool
def record_customer_feedback(session_id: str, rating: int, comment: str = "") -> str:
    """Record customer satisfaction feedback for this support session.
    Use at the end of a resolved conversation when the customer rates their experience.
    Rating should be between 1 and 5, where 5 is the best."""
    if _analytics is not None:
        _analytics.record_feedback(
            session_id, "agent_session", 1 if rating >= 3 else -1
        )
    stars    = "★" * min(max(rating, 1), 5) + "☆" * max(0, 5 - rating)
    sentiment= "positive" if rating >= 4 else "neutral" if rating == 3 else "needs improvement"
    return (
        f"Feedback recorded — thank you! "
        f"Rating: {stars} ({rating}/5) — {sentiment}. "
        f"Comment: {comment if comment else 'none provided'}."
    )


# ── Tool registry — all tools available to the agent ─────────
ALL_TOOLS = [
    search_knowledge_base,
    detect_product,
    create_ticket,
    check_ticket_status,
    get_product_details,
    compare_two_products,
    escalate_to_human_agent,
    record_customer_feedback,
]
