# MindBridge — AI-Powered Mental Health Awareness & Support Agent

> **Disclaimer:** MindBridge is an AI support tool and is **not a replacement for professional medical or psychological care.** If you or someone you know is in immediate danger, call your local emergency number (112 / 911 / 999) or visit the Crisis Support page.

---

## Overview

MindBridge is an **Agentic AI web application** for mental-health awareness, empathetic conversational support, distress-signal detection, and crisis resource connection.

It uses:
- **IBM Granite Models** — via IBM watsonx.ai for all AI generation
- **Multi-Agent Orchestration** — four specialised agents coordinated by a central orchestrator
- **RAG Pipeline** — Retrieval-Augmented Generation backed by verified mental-health documents
- **React + FastAPI** — modern full-stack web application

---

## Architecture

```
User Input
    │
    ▼
┌─────────────────────────────────────────┐
│              Orchestrator               │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │   Distress Detection Agent      │    │
│  │  (keyword screen + Granite)     │    │
│  └──────────────┬──────────────────┘    │
│                 │ risk_level            │
│         ┌───────┴────────┐             │
│       LOW/MOD           HIGH           │
│         │                │             │
│  ┌──────┴──────┐  ┌──────┴──────┐     │
│  │ Awareness   │  │   Crisis    │     │
│  │    Agent   │  │   Agent     │     │
│  │ Empathetic  │  │  + Safety   │     │
│  │    Agent   │  │   Filter    │     │
│  └──────┬──────┘  └──────┬──────┘     │
│         │                │             │
│         └────────┬───────┘             │
│                  │ RAG retrieval        │
│         ┌────────┴───────┐             │
│         │  Chroma/FAISS  │             │
│         │  Vector Store  │             │
│         └────────────────┘             │
└─────────────────────────────────────────┘
    │
    ▼
 Safe Response → Frontend
```

---

## Project Structure

```
mental-health-agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application & API routes
│   │   ├── config.py            # Settings from .env
│   │   ├── models.py            # Pydantic request/response models
│   │   ├── orchestrator.py      # Agent routing orchestrator
│   │   ├── watsonx_client.py    # IBM Granite model client
│   │   ├── rag_pipeline.py      # RAG: load → chunk → embed → retrieve
│   │   ├── journal_service.py   # Journal save & AI analysis
│   │   └── agents/
│   │       ├── awareness_agent.py    # Educational content agent
│   │       ├── distress_agent.py     # Risk classification agent
│   │       ├── empathetic_agent.py   # Conversational support agent
│   │       └── crisis_agent.py       # High-risk safety agent
│   ├── data/
│   │   └── knowledge_base/      # Seed .txt files for RAG indexing
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Dashboard.tsx    # Home dashboard
    │   │   ├── ChatPage.tsx     # AI chat interface
    │   │   ├── JournalPage.tsx  # Private journaling
    │   │   ├── ResourcesPage.tsx # Mental health education
    │   │   └── CrisisPage.tsx   # Crisis helplines & guidance
    │   ├── App.tsx              # Router & sidebar layout
    │   ├── api.ts               # Axios API client
    │   └── types.ts             # Shared TypeScript types
    ├── package.json
    └── vite.config.ts
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- IBM Cloud account with watsonx.ai access
- IBM Granite model access in your watsonx.ai project

### 1. Backend Setup

```bash
cd mental-health-agent/backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env         # Windows
cp .env.example .env           # macOS/Linux
# Edit .env and add your IBM watsonx.ai credentials

# Start the API server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd mental-health-agent/frontend

npm install
npm run dev
# Open http://localhost:3000
```

### 3. Configuration (`.env`)

| Variable | Description |
|---|---|
| `WATSONX_API_KEY` | Your IBM Cloud API key |
| `WATSONX_PROJECT_ID` | Your watsonx.ai project ID |
| `WATSONX_URL` | watsonx.ai endpoint (default: us-south) |
| `GRANITE_CHAT_MODEL` | Granite chat model ID |
| `CHROMA_PERSIST_DIR` | Where to persist the vector store |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/chat` | Main chat endpoint (agent orchestrator) |
| `POST` | `/api/distress-analysis` | Standalone distress analysis |
| `POST` | `/api/journal` | Save a journal entry |
| `POST` | `/api/journal/analyse` | Save and AI-analyse a journal entry |
| `GET` | `/api/resources` | Get crisis/support resources |

Interactive API docs available at `http://localhost:8000/docs`.

---

## Multi-Agent Workflow

1. **User sends a message** via the React chat interface.
2. **Orchestrator** receives the message and calls the **Distress Detection Agent**.
3. Distress agent runs a **keyword pre-filter** and then calls **IBM Granite** for structured risk analysis. Returns `low`, `moderate`, or `high`.
4. Based on the risk level:
   - **Low** → Educational query? → **Awareness Agent** (RAG-grounded). Conversational? → **Empathetic Agent**.
   - **Moderate** → **Empathetic Agent** with encouraging professional support.
   - **High** → **Crisis Response Agent** — safety-first, provides verified helpline resources, applies a safety content filter.
5. The selected agent retrieves relevant context from the **Chroma vector store** (RAG) and crafts a prompt for **IBM Granite**.
6. The Granite response is post-processed and returned to the user along with the risk level and any relevant resources.

---

## Safety & Ethical Design

- ❌ Never diagnoses any mental-health condition
- ❌ Never provides instructions for self-harm
- ❌ Never presents itself as a human therapist
- ✅ Always directs high-risk users to verified human support
- ✅ Applies a safety content filter on all crisis agent responses
- ✅ Requires explicit user consent for journal analysis
- ✅ RAG-grounded responses reduce hallucination on sensitive topics
- ✅ Clear AI disclaimer on every page and in every response

---

## Technology Stack

| Component | Technology |
|---|---|
| AI Models | IBM Granite 13B (chat + instruct) |
| AI Platform | IBM watsonx.ai |
| Agent Framework | Custom orchestrator + LangChain utilities |
| RAG | LangChain + HuggingFace Embeddings |
| Vector Store | ChromaDB (persistent) |
| Backend | Python 3.10+ / FastAPI |
| Frontend | React 18 + TypeScript + Vite |
| Styling | Custom CSS with design tokens |

---

## Future Scope

- Voice interface with multilingual support
- Wearable / health device integration
- IBM Langflow visual workflow builder integration
- User accounts with secure persistent journal storage
- Counselor-facing professional dashboard
- Mobile application (React Native)
