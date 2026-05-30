# ✈️ Flight Agent

A conversational AI agent for flight booking and KLM baggage policy queries. Built with LangGraph's ReAct loop — the agent decides which tool to call based on what you ask, remembers your conversation across messages, and responds in plain English.

**Live demo → [luxury-youtiao-5bef59.netlify.app](https://luxury-youtiao-5bef59.netlify.app)**  
**API → [flight-agent-1.onrender.com](https://flight-agent-1.onrender.com/docs)**

> ⚠️ **Demo project.** Uses hardcoded flight data, not real airline APIs. The RAG tool retrieves from a local KLM baggage policy document — not a live search tool.

---

## What it does

- Check flight availability between airports
- Book a flight (returns a mock confirmation)
- File a customer complaint
- Answer KLM baggage policy questions — powered by BM25 retrieval over `klm_baggage.txt`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent framework | LangGraph (ReAct loop) |
| LLM | Groq — llama-3.3-70b-versatile |
| RAG retrieval | BM25Retriever (rank_bm25) — no local ML model |
| Conversation memory | LangGraph MemorySaver checkpointer |
| Backend | FastAPI + Uvicorn, deployed on Render |
| Frontend | Vanilla HTML/CSS/JS, deployed on Netlify |
| Cross-origin | FastAPI CORSMiddleware |

**Why BM25 instead of vector embeddings?**  
The original implementation used HuggingFace `sentence-transformers` which pulls in PyTorch — blowing past Render's free tier 512MB RAM limit on startup. BM25 is pure Python, needs ~5MB RAM, and works well for keyword-heavy policy queries.

---

## Architecture

```
User → Netlify frontend
         ↓ POST /chat
    FastAPI (Render)
         ↓
    LangGraph ReAct agent
         ↓ (tool routing)
    ┌────────────────────────────┐
    │  check_flight              │
    │  book_flight               │
    │  book_complaint            │
    │  rag_tool (BM25 retriever) │
    └────────────────────────────┘
         ↓
    Groq API (llama-3.3-70b)
```

The agent uses a `MemorySaver` checkpointer — each session gets a `thread_id` so the agent remembers earlier messages within the same conversation.

See [ARCHITECTURE.md](ARCHITECTURE.md) for a full breakdown of each file.

---

## File Structure

```
├── api.py           # FastAPI app — /chat endpoint + CORS
├── graph.py         # LangGraph StateGraph + MemorySaver checkpointer
├── tools.py         # BM25 RAG tool + flight/complaint tools
├── context.py       # Model name + system prompt config
├── state.py         # State and InputState definitions
├── utils.py         # load_chat_model helper
├── prompts.py       # System prompt
├── klm_baggage.txt  # RAG knowledge base (KLM baggage policy)
├── requirements.txt
└── runtime.txt      # Python version pin for Render
```

---

## Run locally

```bash
git clone https://github.com/MAGUIRE-GOATED/Flight_agent
cd Flight_agent
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_key_here
```

Start the API:
```bash
uvicorn api:app --reload
```

Then open `http://localhost:8000/docs` to try it via Swagger UI.

---

## Deployment

- **Backend** — Render (free tier). `runtime.txt` pins the Python version. Auto-deploys on push to `main`. Note: free instances sleep after inactivity — first request after idle takes ~50s.
- **Frontend** — Netlify (drag and drop `index.html`). CORS is scoped to the Netlify URL in `api.py`.

