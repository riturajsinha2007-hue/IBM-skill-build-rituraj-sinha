"""
Pydantic models for API request / response payloads.
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class AgentType(str, Enum):
    AWARENESS = "awareness"
    DISTRESS = "distress"
    EMPATHETIC = "empathetic"
    CRISIS = "crisis"


# ---------------------------------------------------------------------------
# Chat models
# ---------------------------------------------------------------------------

class Message(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str


# ---------------------------------------------------------------------------
# Resource model (defined early — referenced by ChatResponse)
# ---------------------------------------------------------------------------

class Resource(BaseModel):
    name: str
    description: str
    contact: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    message: str
    history: List[Message] = Field(default_factory=list)
    location: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    agent_used: AgentType
    risk_level: RiskLevel
    resources: List[Resource] = Field(default_factory=list)
    disclaimer: str = (
        "This AI is a supportive tool only and is not a replacement for "
        "professional medical or psychological care."
    )


# ---------------------------------------------------------------------------
# Journal models
# ---------------------------------------------------------------------------

class JournalEntry(BaseModel):
    entry_id: Optional[str] = None
    content: str
    analyze: bool = False


class JournalAnalysisResponse(BaseModel):
    entry_id: str
    sentiment: str
    risk_level: RiskLevel
    reflection: str
    suggestions: List[str]


# ---------------------------------------------------------------------------
# Distress analysis
# ---------------------------------------------------------------------------

class DistressAnalysisRequest(BaseModel):
    text: str
    context: Optional[str] = None


class DistressAnalysisResponse(BaseModel):
    risk_level: RiskLevel
    signals_detected: List[str]
    recommended_action: str
