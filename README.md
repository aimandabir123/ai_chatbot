# 🤖 Apple AI Support Agent
### Agentic · Multi-Product · Tool-Calling · Groq · FAISS · Streamlit


## Supported Products (4)

| Product | Category | Price |
|---------|----------|-------|
| 🥽 Apple Vision Pro | Spatial Computing | $3,499 |
| 📱 iPhone 15 Pro | Smartphone | $999 |
| 💻 MacBook Pro M3 | Laptop | $1,999 |
| 🎧 AirPods Pro 2 | Audio | $249 |

---

## Agent Tools (8)

| Tool | When the agent calls it |
|------|------------------------|
| search_knowledge_base | Every question — RAG search |
| detect_product | First — identifies which product |
| create_ticket | Issue needs follow-up |
| check_ticket_status | Customer provides ticket ID |
| get_product_details | General product questions |
| compare_two_products | Comparing two products |
| escalate_to_human_agent | Customer asks for human |
| record_customer_feedback | Customer rates experience |

---

## Setup (5 steps)

### Step 1 — Get FREE Groq API Key
```
1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Click API Keys → Create API Key
4. Copy the key — it starts with gsk_
```

### Step 2 — Configure .env
```bash
cd backend
# Windows:
copy .env.example .env
# Mac/Linux:
cp .env.example .env

# Open .env and set:
GROQ_API_KEY=gsk_your_key_here
```

### Step 3 — Start Backend (Terminal 1)
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Wait for: `✅  Agent is ready!`

### Step 4 — Start Frontend (Terminal 2)
```bash
cd frontend
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

### Step 5 — Open Browser
```
http://localhost:8501
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | /health | Check backend status |
| POST | /chat | Send message to agent |
| GET | /products | List all products |
| GET | /faq | All FAQ data |
| GET | /tools | List agent tools |
| POST | /ticket | Create support ticket |
| GET | /tickets | List all tickets |
| POST | /feedback | Submit rating |
| GET | /analytics | Dashboard data |
| GET | /sessions | Active sessions |
| GET | /docs | Swagger UI |

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| GROQ_API_KEY missing | Add key to backend/.env |
| Connection refused | Start backend with uvicorn |
| (venv) not showing | Run activate command again |
| ModuleNotFoundError | Run pip install -r requirements.txt |
| FAISS install fails on Windows | pip install faiss-cpu --no-cache-dir |

---

Tech Stack: FastAPI · LangChain · Groq · FAISS · HuggingFace · Streamlit · Plotly
