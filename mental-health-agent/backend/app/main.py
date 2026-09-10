"""
FastAPI application – main entry point.
"""
from __future__ import annotations

import logging
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.journal_service import JournalService
from app.models import (
    ChatRequest,
    ChatResponse,
    DistressAnalysisRequest,
    DistressAnalysisResponse,
    JournalAnalysisResponse,
    JournalEntry,
)
from app.orchestrator import Orchestrator

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI Mental Health Support API",
    description=(
        "Agentic AI mental-health awareness and suicide prevention backend. "
        "Powered by IBM Granite via IBM watsonx.ai."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Singletons (lazy-initialised on first request)
# ---------------------------------------------------------------------------
_orchestrator: Orchestrator | None = None
_journal_service: JournalService | None = None


def _get_orchestrator() -> Orchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator


def _get_journal_service() -> JournalService:
    global _journal_service
    if _journal_service is None:
        _journal_service = JournalService()
    return _journal_service


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "mental-health-agent"}


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

@app.post("/api/chat", response_model=ChatResponse, tags=["chat"])
def chat(request: ChatRequest):
    """Main conversational endpoint. Routes through the agent orchestrator."""
    session_id = request.session_id or str(uuid.uuid4())
    try:
        return _get_orchestrator().handle(
            session_id=session_id,
            message=request.message,
            history=request.history,
            location=request.location,
        )
    except Exception as exc:
        logger.exception("Chat error for session %s: %s", session_id, exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


# ---------------------------------------------------------------------------
# Distress Analysis (standalone endpoint)
# ---------------------------------------------------------------------------

@app.post(
    "/api/distress-analysis",
    response_model=DistressAnalysisResponse,
    tags=["analysis"],
)
def distress_analysis(request: DistressAnalysisRequest):
    """Analyse a piece of text for potential distress signals."""
    from app.agents.distress_agent import DistressDetectionAgent
    try:
        agent = DistressDetectionAgent()
        return agent.analyse(request.text)
    except Exception as exc:
        logger.exception("Distress analysis error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error.")


# ---------------------------------------------------------------------------
# Journal
# ---------------------------------------------------------------------------

@app.post("/api/journal", response_model=JournalEntry, tags=["journal"])
def save_journal(entry: JournalEntry):
    """Save a journal entry."""
    return _get_journal_service().save(entry)


@app.post(
    "/api/journal/analyse",
    response_model=JournalAnalysisResponse,
    tags=["journal"],
)
def analyse_journal(entry: JournalEntry):
    """Save and analyse a journal entry (requires user consent via entry.analyze=True)."""
    if not entry.analyze:
        raise HTTPException(
            status_code=400,
            detail="Set analyze=true to consent to AI analysis of your entry.",
        )
    return _get_journal_service().analyse(entry)


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

@app.get("/api/resources", tags=["resources"])
def get_resources(location: str | None = None):
    """Return crisis and mental-health support resources."""
    from app.agents.crisis_agent import _CRISIS_RESOURCES

    if location:
        lower = location.lower()
        filtered = [
            r for r in _CRISIS_RESOURCES
            if r.location
            and (lower in r.location.lower() or "global" in r.location.lower())
        ]
        return filtered if filtered else _CRISIS_RESOURCES

    return _CRISIS_RESOURCES
