"""
Agent Orchestrator

Routes incoming user messages through the pipeline:

  User Input
    → Distress Detection Agent  (risk classification)
    → Route to appropriate agent:
        LOW      → Awareness Agent  (if educational query)
                   Empathetic Agent (if conversational)
        MODERATE → Empathetic Agent
        HIGH     → Crisis Response Agent
    → Return ChatResponse
"""
from __future__ import annotations

import logging
import re
from typing import List, Optional

from app.agents.awareness_agent import AwarenessAgent
from app.agents.crisis_agent import CrisisResponseAgent
from app.agents.distress_agent import DistressDetectionAgent
from app.agents.empathetic_agent import EmpatheticSupportAgent
from app.models import AgentType, ChatResponse, Message, RiskLevel

logger = logging.getLogger(__name__)

# Patterns that indicate an educational / awareness intent
_AWARENESS_PATTERNS = re.compile(
    r"\b(what is|explain|tell me about|how does|define|symptoms of|causes of|"
    r"treatment for|therapy|information about|resources|coping with|mindfulness|"
    r"anxiety|depression|stress|wellbeing|mental health|self.care)\b",
    re.IGNORECASE,
)


class Orchestrator:
    """Central coordinator for all agents."""

    def __init__(self):
        self._distress = DistressDetectionAgent()
        self._empathetic = EmpatheticSupportAgent()
        self._awareness = AwarenessAgent()
        self._crisis = CrisisResponseAgent()

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def handle(
        self,
        session_id: str,
        message: str,
        history: List[Message],
        location: Optional[str] = None,
    ) -> ChatResponse:
        # Step 1: Distress detection
        distress_result = self._distress.analyse(message)
        risk_level = distress_result.risk_level

        logger.info(
            "Session %s | risk=%s | signals=%s",
            session_id,
            risk_level,
            distress_result.signals_detected,
        )

        # Step 2: Route to appropriate agent
        if risk_level == RiskLevel.HIGH:
            reply, resources = self._crisis.respond(message, history, location)
            agent_used = AgentType.CRISIS

        elif risk_level == RiskLevel.MODERATE:
            reply = self._empathetic.respond(message, history)
            resources = []
            agent_used = AgentType.EMPATHETIC

        else:
            # LOW risk — check intent
            if _AWARENESS_PATTERNS.search(message):
                reply = self._awareness.respond(message, history)
                agent_used = AgentType.AWARENESS
            else:
                reply = self._empathetic.respond(message, history)
                agent_used = AgentType.EMPATHETIC
            resources = []

        return ChatResponse(
            session_id=session_id,
            reply=reply,
            agent_used=agent_used,
            risk_level=risk_level,
            resources=resources,
        )
