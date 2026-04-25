"""
app.py
Streamlit frontend for the Agentic Multi-Product Apple AI Support Chatbot.

Run with:
    streamlit run app.py
"""

import streamlit as st
import requests
import uuid
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# ── Configuration ─────────────────────────────────────────────
BACKEND = "http://localhost:8000"

st.set_page_config(
    page_title="Apple AI Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu  { visibility: hidden; }
footer     { visibility: hidden; }
header     { visibility: hidden; }
.stApp     { background: #000000; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }

.top-banner {
    background: linear-gradient(135deg, #0a1628 0%, #0d0d0d 70%);
    border: 0.5px solid #1e1e1e;
    border-radius: 16px;
    padding: 22px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}
.top-banner h1 {
    font-size: 22px;
    font-weight: 700;
    color: #f5f5f7;
    letter-spacing: -0.5px;
    margin: 0 0 4px 0;
}
.top-banner h1 .hl { color: #f55036; }
.top-banner p { font-size: 13px; color: #6e6e73; margin: 0; }
.badges { display: flex; gap: 8px; flex-wrap: wrap; }
.badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 5px 12px; border-radius: 20px;
    font-size: 11px; font-weight: 600;
}
.b1 { background:#2d1610; color:#f55036; border:0.5px solid #5c2a1c; }
.b2 { background:#0d2b17; color:#30d158; border:0.5px solid #1e5530; }
.b3 { background:#0d1f3c; color:#2997ff; border:0.5px solid #1a3d6b; }
.b4 { background:#2b1d3a; color:#bf5af2; border:0.5px solid #5a2a7a; }

.step-card {
    background: #111;
    border: 0.5px solid #222;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 6px;
    font-size: 12px;
}
.step-tool-name { color: #f55036; font-weight: 600; font-size: 11px; margin-bottom: 3px; }
.step-inp  { color: #8e8e93; }
.step-out  { color: #6e6e73; font-size: 11px; margin-top: 3px; }

.faq-answer {
    font-size: 13px;
    color: #8e8e93;
    line-height: 1.75;
    white-space: pre-line;
    padding: 4px 0 8px 0;
}

.prod-card {
    background: #111;
    border: 0.5px solid #222;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}
.prod-emoji { font-size: 36px; margin-bottom: 8px; }
.prod-name  { font-size: 14px; font-weight: 600; color: #f5f5f7; margin-bottom: 3px; }
.prod-cat   { font-size: 11px; color: #6e6e73; }
.prod-price { font-size: 12px; color: #8e8e93; margin-top: 4px; }
.prod-faqs  { font-size: 11px; color: #555; margin-top: 6px; }

::-webkit-scrollbar       { width: 4px; }
::-webkit-scrollbar-thumb { background: #2c2c2e; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────
defaults = {
    "session_id":    str(uuid.uuid4()),
    "messages":      [],
    "sent_history":  [],
    "last_score":    0.5,
    "ticket_done":   None,
    "sel_product":   None,
    "tools_log":     [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── API helper ────────────────────────────────────────────────
def call(method: str, path: str, **kwargs):
    """Call the backend API. Returns JSON dict or None on error."""
    try:
        resp = getattr(requests, method)(
            f"{BACKEND}{path}", timeout=60, **kwargs
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error(
            "❌  Cannot reach the backend server.\n\n"
            "Make sure it is running:\n"
            "```\ncd backend\nuvicorn main:app --reload --port 8000\n```"
        )
        return None
    except requests.exceptions.HTTPError as he:
        st.error(f"Server error {he.response.status_code}: {he.response.text[:200]}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None


# ════════════════════════════════════════════════════════════════
#  BANNER
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="top-banner">
  <div>
    <h1>🤖 Apple AI Support <span class="hl">Agent</span></h1>
    <p>Agentic &nbsp;·&nbsp; Multi-Product &nbsp;·&nbsp;
       Tool-Calling &nbsp;·&nbsp; Groq LLM &nbsp;·&nbsp; FAISS RAG</p>
  </div>
  <div class="badges">
    <span class="badge b1">⚡ Agentic</span>
    <span class="badge b2">● Online</span>
    <span class="badge b3">🔧 8 Tools</span>
    <span class="badge b4">📦 4 Products</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════
(tab_chat, tab_products, tab_faq,
 tab_ticket, tab_analytics, tab_info) = st.tabs([
    "💬  Chat",
    "📦  Products",
    "📖  FAQ",
    "🎫  Ticket",
    "📊  Analytics",
    "🤖  Agent Info",
])


# ════════════════════════════════════════════════════════════════
#  TAB 1 — CHAT
# ════════════════════════════════════════════════════════════════
with tab_chat:
    main_col, side_col = st.columns([3, 1], gap="medium")

    # ── Side panel ────────────────────────────────────────────
    with side_col:
        st.markdown("#### 📦 Products")
        prods = call("get", "/products")
        if prods:
            for p in prods["products"]:
                is_sel = st.session_state.sel_product == p["id"]
                if st.button(
                    f"{p['emoji']}  {p['name']}",
                    key=f"pb_{p['id']}",
                    use_container_width=True,
                    type="primary" if is_sel else "secondary",
                ):
                    st.session_state.sel_product = p["id"]
                    st.session_state["_pf"] = f"Tell me about {p['name']}"
                    st.rerun()

        st.divider()
        st.markdown("#### ⚡ Quick Questions")
        quick = [
            "Vision Pro display is blurry",
            "iPhone 15 Pro camera ProRes",
            "MacBook Pro M3 running slow",
            "AirPods Pro 2 not connecting",
            "Compare iPhone and MacBook",
            "I need a human agent",
            "Create a support ticket",
        ]
        for q in quick:
            if st.button(q, key=f"qq_{q}", use_container_width=True):
                st.session_state["_pf"] = q
                st.rerun()

        st.divider()
        st.markdown("#### 😊 Sentiment")
        score = st.session_state.last_score
        emoji = "😊" if score >= 0.65 else "😐" if score >= 0.35 else "😟"
        label = "positive" if score >= 0.65 else "neutral" if score >= 0.35 else "negative"
        st.progress(float(score))
        st.caption(f"{emoji}  **{label}**  ·  {score:.2f}")

        if st.session_state.tools_log:
            st.divider()
            st.markdown("#### 🔧 Tools used")
            for t in list(dict.fromkeys(st.session_state.tools_log[-12:])):
                st.caption(f"• {t.replace('_', ' ')}")

    # ── Main chat area ────────────────────────────────────────
    with main_col:
        # Welcome message shown before first user message
        if not st.session_state.messages:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(
                    "Hi! I'm your **Apple AI Support Agent** ⚡\n\n"
                    "I can help you with:\n"
                    "- 🥽 **Apple Vision Pro** — spatial computing\n"
                    "- 📱 **iPhone 15 Pro** — smartphone\n"
                    "- 💻 **MacBook Pro M3** — laptop\n"
                    "- 🎧 **AirPods Pro 2** — earbuds\n\n"
                    "I automatically detect your product, search the knowledge base, "
                    "create support tickets when needed, and escalate to human agents. "
                    "Just describe your issue!"
                )

        # Render message history
        for msg in st.session_state.messages:
            av = "👤" if msg["role"] == "user" else "🤖"
            with st.chat_message(msg["role"], avatar=av):
                st.markdown(msg["content"])

                # Bot message metadata and reasoning steps
                if msg["role"] == "assistant":
                    caption_parts = []
                    if msg.get("product"):
                        if prods:
                            pname = next(
                                (p["name"] for p in prods["products"]
                                 if p["id"] == msg["product"]),
                                msg["product"],
                            )
                            caption_parts.append(f"📦 {pname}")
                    if msg.get("tools_used"):
                        tools_str = "  ·  ".join(
                            t.replace("_", " ")
                            for t in msg["tools_used"][:4]
                        )
                        caption_parts.append(f"🔧 {tools_str}")
                    if msg.get("model"):
                        caption_parts.append(f"⚡ {msg['model'].split('-')[0]}")
                    if caption_parts:
                        st.caption("  ·  ".join(caption_parts))

                    if msg.get("steps"):
                        n = len(msg["steps"])
                        with st.expander(
                            f"🔍  Agent reasoning  ({n} step{'s' if n != 1 else ''})",
                            expanded=False,
                        ):
                            for i, step in enumerate(msg["steps"], 1):
                                inp = step["input"][:160]
                                out = step["output"][:240]
                                st.markdown(f"""
<div class="step-card">
  <div class="step-tool-name">Step {i} — {step["tool"].replace("_", " ")}</div>
  <div class="step-inp">Input: {inp}{"..." if len(step["input"]) > 160 else ""}</div>
  <div class="step-out">Result: {out}{"..." if len(step["output"]) > 240 else ""}</div>
</div>""", unsafe_allow_html=True)

        # ── Chat input ────────────────────────────────────────
        pf         = st.session_state.pop("_pf", "")
        user_input = st.chat_input("Ask anything about any Apple product…")
        if pf and not user_input:
            user_input = pf

        if user_input:
            mid = str(uuid.uuid4())
            now = datetime.now().strftime("%H:%M")

            st.session_state.messages.append({
                "id":    mid,
                "role":  "user",
                "content": user_input,
                "time":  now,
            })
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤖  Agent is working — calling tools…"):
                    data = call("post", "/chat", json={
                        "message":    user_input,
                        "session_id": st.session_state.session_id,
                    })

                if data:
                    st.session_state.session_id = data.get(
                        "session_id", st.session_state.session_id
                    )

                    response    = data.get("response", "Sorry, no response available.")
                    tools_used  = data.get("tools_used", [])
                    steps       = data.get("steps", [])
                    sentiment   = data.get("sentiment", {})
                    product     = data.get("product")
                    model_used  = data.get("model", "groq")

                    st.markdown(response)

                    # Caption line
                    cp = []
                    if product and prods:
                        pname = next(
                            (p["name"] for p in prods["products"] if p["id"] == product),
                            product,
                        )
                        cp.append(f"📦 {pname}")
                    if tools_used:
                        cp.append("🔧 " + "  ·  ".join(
                            t.replace("_", " ") for t in tools_used[:4]
                        ))
                    cp.append(f"⚡ {model_used.split('-')[0]}")
                    st.caption("  ·  ".join(cp))

                    # Reasoning steps
                    if steps:
                        n = len(steps)
                        with st.expander(
                            f"🔍  Agent reasoning  ({n} step{'s' if n != 1 else ''})",
                            expanded=False,
                        ):
                            for i, step in enumerate(steps, 1):
                                inp = step["input"][:160]
                                out = step["output"][:240]
                                st.markdown(f"""
<div class="step-card">
  <div class="step-tool-name">Step {i} — {step["tool"].replace("_", " ")}</div>
  <div class="step-inp">Input: {inp}{"..." if len(step["input"]) > 160 else ""}</div>
  <div class="step-out">Result: {out}{"..." if len(step["output"]) > 240 else ""}</div>
</div>""", unsafe_allow_html=True)

                    # Sentiment bar
                    sc = float(sentiment.get("score", 0.5))
                    st.progress(sc, text=(
                        f"{sentiment.get('emoji','😐')}  "
                        f"Sentiment: **{sentiment.get('label','neutral')}**  ({sc:.2f})"
                    ))

                    # Feedback buttons
                    fc1, fc2, _ = st.columns([1, 1, 4])
                    with fc1:
                        if st.button("👍  Helpful", key=f"ph_{mid}"):
                            call("post", "/feedback", json={
                                "session_id": st.session_state.session_id,
                                "message_id": mid, "rating": 1,
                            })
                            st.success("Thanks! 🎉")
                    with fc2:
                        if st.button("👎  Not helpful", key=f"nh_{mid}"):
                            call("post", "/feedback", json={
                                "session_id": st.session_state.session_id,
                                "message_id": mid, "rating": -1,
                            })
                            st.warning("Sorry! Creating a ticket may help.")

                    # Save to history
                    st.session_state.messages.append({
                        "id":         mid + "_bot",
                        "role":       "assistant",
                        "content":    response,
                        "tools_used": tools_used,
                        "steps":      steps,
                        "product":    product,
                        "model":      model_used,
                        "time":       now,
                    })
                    st.session_state.sent_history.append(sc)
                    st.session_state.last_score = sc
                    st.session_state.tools_log.extend(tools_used)
                    if product:
                        st.session_state.sel_product = product


# ════════════════════════════════════════════════════════════════
#  TAB 2 — PRODUCTS
# ════════════════════════════════════════════════════════════════
with tab_products:
    st.markdown("### 📦 Supported Products")
    prods_data = call("get", "/products")
    if prods_data:
        cols = st.columns(4)
        for i, p in enumerate(prods_data["products"]):
            with cols[i % 4]:
                st.markdown(f"""
<div class="prod-card">
  <div class="prod-emoji">{p['emoji']}</div>
  <div class="prod-name">{p['name']}</div>
  <div class="prod-cat">{p['category']}</div>
  <div class="prod-price">From {p['price']}</div>
  <div class="prod-faqs">{p['faq_count']} FAQ entries</div>
</div>""", unsafe_allow_html=True)
                st.write("")
                if st.button(
                    f"Ask about {p['emoji']}",
                    key=f"apb_{p['id']}",
                    use_container_width=True,
                ):
                    st.session_state.sel_product = p["id"]
                    st.session_state["_pf"] = f"Tell me about the {p['name']}"
                    st.rerun()


# ════════════════════════════════════════════════════════════════
#  TAB 3 — FAQ
# ════════════════════════════════════════════════════════════════
with tab_faq:
    st.markdown("### 📖 FAQ — All Products")
    faq_data = call("get", "/faq")
    if faq_data:
        search = st.text_input(
            "🔍  Search across all products",
            placeholder="battery, camera, reset, blurry, setup…",
        )
        product_names = ["All Products"] + [
            p["product_name"] for p in faq_data["products"]
        ]
        product_filter = st.selectbox("Filter by product", product_names)

        for prod in faq_data["products"]:
            if product_filter != "All Products" and prod["product_name"] != product_filter:
                continue

            for cat in prod["categories"]:
                questions = cat["questions"]
                if search:
                    sq = search.lower()
                    questions = [
                        q for q in questions
                        if sq in q["q"].lower() or sq in q["a"].lower()
                    ]
                    if not questions:
                        continue

                header = (
                    f"{prod['emoji']}  {prod['product_name']}  —  "
                    f"{cat['category']}  ({len(questions)})"
                )
                with st.expander(header, expanded=bool(search)):
                    for item in questions:
                        st.markdown(f"**Q: {item['q']}**")
                        st.markdown(
                            f"<div class='faq-answer'>"
                            f"{item['a'].replace(chr(10), '<br>')}"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            "💬  Ask the agent",
                            key=f"fq_{item['q'][:28]}",
                        ):
                            st.session_state["_pf"] = item["q"]
                            st.info("✅  Click the **Chat** tab to see the answer.")
                        st.divider()
    else:
        st.warning("Could not load FAQs. Is the backend running?")


# ════════════════════════════════════════════════════════════════
#  TAB 4 — TICKET
# ════════════════════════════════════════════════════════════════
with tab_ticket:
    st.markdown("### 🎫 Create a Support Ticket")
    st.caption("Fill in the form and our team will contact you within the SLA window.")

    if st.session_state.ticket_done:
        t = st.session_state.ticket_done
        st.success(f"✅  Ticket **{t['id']}** created!")
        left, right = st.columns([3, 2])
        with left:
            st.table(pd.DataFrame([
                {"Field": "Ticket ID",   "Value": t["id"]},
                {"Field": "Product",     "Value": t.get("product", "N/A")},
                {"Field": "Priority",    "Value": t["priority"]},
                {"Field": "Status",      "Value": t["status"]},
                {"Field": "SLA",         "Value": t["sla"]},
                {"Field": "Assigned to", "Value": t["assigned_to"]},
            ]))
        with right:
            st.info(
                f"📧  Confirmation sent to **{t['email']}**\n\n"
                "📞  Urgent? Call **1-800-APL-CARE**\n\n"
                "🌐  Track at **getsupport.apple.com**"
            )
        if st.button("➕  Create another ticket"):
            st.session_state.ticket_done = None
            st.rerun()
    else:
        with st.form("ticket_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                t_name    = st.text_input("Full Name *", placeholder="Alex Johnson")
                t_email   = st.text_input("Email *",     placeholder="alex@example.com")
                t_serial  = st.text_input("Device Serial (optional)")
            with c2:
                t_product = st.selectbox("Product *", [
                    "",
                    "Apple Vision Pro",
                    "iPhone 15 Pro",
                    "MacBook Pro M3",
                    "AirPods Pro 2",
                    "Other",
                ])
                t_cat     = st.selectbox("Category *", [
                    "",
                    "Display / Optics",
                    "Battery & Charging",
                    "Audio / Spatial Sound",
                    "Eye / Hand Tracking",
                    "Software / Apps",
                    "Hardware Damage",
                    "Account & Billing",
                    "Other",
                ])
                t_pri     = st.selectbox("Priority", [
                    "Low", "Medium", "High", "Critical"
                ], index=1)

            t_desc = st.text_area(
                "Describe your issue *",
                placeholder=(
                    "Please describe:\n"
                    "1. What is the problem?\n"
                    "2. When did it start?\n"
                    "3. What have you already tried?"
                ),
                height=130,
            )
            submitted = st.form_submit_button(
                "🎫  Submit Support Ticket",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            errors = []
            if not t_name.strip():      errors.append("Full Name is required.")
            if not t_email.strip():     errors.append("Email is required.")
            if "@" not in t_email:      errors.append("Please enter a valid email.")
            if not t_product:           errors.append("Product is required.")
            if not t_cat:               errors.append("Category is required.")
            if not t_desc.strip():      errors.append("Issue description is required.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                with st.spinner("Creating ticket…"):
                    result = call("post", "/ticket", json={
                        "name":        t_name.strip(),
                        "email":       t_email.strip(),
                        "product":     t_product,
                        "category":    t_cat,
                        "priority":    t_pri,
                        "description": t_desc.strip(),
                        "session_id":  st.session_state.session_id,
                    })
                if result and result.get("success"):
                    st.session_state.ticket_done = result["ticket"]
                    st.rerun()
                else:
                    st.error("Failed to create ticket. Is the backend running?")


# ════════════════════════════════════════════════════════════════
#  TAB 5 — ANALYTICS
# ════════════════════════════════════════════════════════════════
with tab_analytics:
    st.markdown("### 📊 Analytics Dashboard")
    if st.button("🔄  Refresh"):
        st.rerun()

    adata = call("get", "/analytics")
    if adata:
        ov    = adata.get("overview",  {})
        fb    = adata.get("feedback",  {})
        sent  = adata.get("sentiment", {})
        tools = adata.get("top_tools", [])

        # KPI row
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("💬 Messages",     ov.get("total_messages", 0))
        k2.metric("🧑 Sessions",     ov.get("total_sessions",  0))
        k3.metric("👍 Satisfaction",
                  f"{fb.get('satisfaction_pct') or '—'}"
                  f"{'%' if fb.get('satisfaction_pct') else ''}")
        k4.metric("⏱ Uptime hrs",   ov.get("uptime_hours", 0))

        st.divider()
        ca, cb = st.columns(2)

        with ca:
            hist = st.session_state.sent_history or sent.get("history", [])
            if hist:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=hist, mode="lines+markers",
                    line=dict(color="#f55036", width=2),
                    marker=dict(size=5),
                    fill="tozeroy",
                    fillcolor="rgba(245,80,54,0.08)",
                ))
                fig.update_layout(
                    title="Sentiment score over time",
                    height=250,
                    paper_bgcolor="#0d0d0d", plot_bgcolor="#0d0d0d",
                    font=dict(color="#f5f5f7", size=11),
                    margin=dict(l=10, r=10, t=40, b=10),
                    yaxis=dict(range=[0, 1], gridcolor="#1e1e1e"),
                    xaxis=dict(gridcolor="#1e1e1e"),
                    showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Send some messages to see sentiment data here.")

        with cb:
            if tools:
                df_t = pd.DataFrame(tools)
                df_t["tool"] = df_t["tool"].str.replace("_", " ").str.title()
                fig2 = px.bar(
                    df_t, x="count", y="tool",
                    orientation="h",
                    color_discrete_sequence=["#2997ff"],
                    title="Agent tools called",
                )
                fig2.update_layout(
                    height=250,
                    paper_bgcolor="#0d0d0d", plot_bgcolor="#0d0d0d",
                    font=dict(color="#f5f5f7", size=11),
                    margin=dict(l=10, r=10, t=40, b=10),
                    xaxis=dict(gridcolor="#1e1e1e"),
                    yaxis=dict(gridcolor="#1e1e1e"),
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Tool usage will appear here after conversations.")

        # Sentiment distribution pie
        pos = sent.get("pos_pct", 0)
        neu = sent.get("neu_pct", 0)
        neg = sent.get("neg_pct", 0)
        if pos + neu + neg > 0:
            st.divider()
            fig3 = go.Figure(go.Pie(
                labels=["Positive 😊", "Neutral 😐", "Negative 😟"],
                values=[pos, neu, neg],
                hole=0.55,
                marker_colors=["#30d158", "#ff9500", "#ff453a"],
            ))
            fig3.update_layout(
                title="Sentiment distribution",
                height=280,
                paper_bgcolor="#0d0d0d",
                font=dict(color="#f5f5f7", size=11),
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(bgcolor="#0d0d0d"),
            )
            st.plotly_chart(fig3, use_container_width=True)

    else:
        st.warning("Analytics not available. Is the backend running?")


# ════════════════════════════════════════════════════════════════
#  TAB 6 — AGENT INFO
# ════════════════════════════════════════════════════════════════
with tab_info:
    st.markdown("### 🤖 Agent Architecture")

    st.markdown("""
**How the agent works (tool-calling pattern):**

1. User sends a message
2. Groq LLM + all 8 tools are sent to the API
3. Groq decides which tool to call — returns structured JSON (not text)
4. The tool runs and its result is sent back to Groq
5. Groq calls more tools OR gives the Final Answer
6. Steps 3-5 repeat up to 6 times per message
7. Final Answer is sent to the user

This is more reliable than ReAct string parsing because Groq returns
structured JSON tool calls — no regex matching that can break.
""")

    st.divider()

    # Tools list
    st.markdown("#### 🔧 Available Tools")
    tools_data = call("get", "/tools")
    if tools_data:
        t_col1, t_col2 = st.columns(2)
        for i, t in enumerate(tools_data["tools"]):
            col = t_col1 if i % 2 == 0 else t_col2
            with col:
                with st.expander(f"🔧  {t['name'].replace('_', ' ').title()}"):
                    st.caption(t["description"])

    st.divider()

    # Active sessions
    st.markdown("#### 💬 Active Sessions")
    sessions_data = call("get", "/sessions")
    if sessions_data and sessions_data.get("sessions"):
        df_s = pd.DataFrame([
            {
                "Session": s["id"][:10] + "…",
                "Product": s.get("product") or "detecting…",
                "Turns":   s.get("turns", 0),
                "Tools":   ", ".join(s.get("tools_used", [])) or "none yet",
            }
            for s in sessions_data["sessions"]
        ])
        st.dataframe(df_s, use_container_width=True, hide_index=True)
    else:
        st.info("No active sessions yet.")

    st.divider()

    # Tickets
    st.markdown("#### 🎫 All Tickets")
    tickets_data = call("get", "/tickets")
    if tickets_data:
        tl = tickets_data.get("tickets", [])
        if tl:
            df_tk = pd.DataFrame([
                {
                    "ID":       t["id"],
                    "Product":  t.get("product", "N/A"),
                    "Priority": t["priority"],
                    "Status":   t["status"],
                    "Created":  t["created_at"][:16].replace("T", " "),
                }
                for t in tl
            ])
            st.dataframe(df_tk, use_container_width=True, hide_index=True)
        else:
            st.info("No tickets yet.")


# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "🤖 Apple AI Support Agent  ·  "
    "Groq Tool-Calling  ·  LangChain  ·  FAISS  ·  Streamlit  ·  "
    f"Session: `{st.session_state.session_id[:14]}…`"
)
