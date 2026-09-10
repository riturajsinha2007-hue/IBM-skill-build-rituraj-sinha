"""
Distress Detection Agent

Analyses user text for emotional distress signals and returns a RiskLevel
(low / moderate / high).  This is NOT clinical diagnosis – it is supportive
risk-awareness to route the user to the most appropriate agent.
"""
from __future__ import annotations

import json
import logging
import re

from app.models import DistressAnalysisResponse, RiskLevel
from app.rag_pipeline import get_rag_pipeline
from app.watsonx_client import get_instruct_client

logger = logging.getLogger(__name__)

# Keyword heuristics used as a fast pre-filter BEFORE calling Granite
_HIGH_RISK_KEYWORDS = [
    "kill myself", "end my life", "want to die", "suicidal", "suicide",
    "i dont want to live", "i don't want to live", "no reason to live",
    "take my own life", "hurt myself", "self-harm", "cut myself",
    "overdose", "jump off", "hang myself",
]

_MODERATE_KEYWORDS = [
    "hopeless", "helpless", "worthless", "can't go on", "can't cope",
    "breaking down", "falling apart", "nobody cares", "all alone",
    "severe depression", "severe anxiety", "panic attack",
    "extremely stressed", "losing my mind",
]


def _keyword_screen(text: str) -> RiskLevel | None:
    lower = text.lower()
    for kw in _HIGH_RISK_KEYWORDS:
        if kw in lower:
            return RiskLevel.HIGH
    for kw in _MODERATE_KEYWORDS:
        if kw in lower:
            return RiskLevel.MODERATE
    return None


_ANALYSIS_PROMPT = """\
You are a mental-health risk-awareness assistant. Your role is to assess text
for potential emotional distress signals and categorise the risk level.

IMPORTANT:
- You are NOT performing clinical diagnosis.
- Risk levels: "low", "moderate", or "high".
- Return ONLY a JSON object with these keys:
  - "risk_level": one of "low", "moderate", "high"
  - "signals": a list of brief signal descriptions (max 5)
  - "recommended_action": a one-sentence recommended next step

{context}

Text to analyse:
\"\"\"{text}\"\"\"

JSON response:
"""


class DistressDetectionAgent:
    """Analyses text and returns a structured DistressAnalysisResponse."""

    def __init__(self):
        self._model = get_instruct_client()
        self._rag = get_rag_pipeline()

    def analyse(self, text: str) -> DistressAnalysisResponse:
        # 1. Fast keyword pre-filter
        keyword_risk = _keyword_screen(text)
        if keyword_risk == RiskLevel.HIGH:
            return DistressAnalysisResponse(
                risk_level=RiskLevel.HIGH,
                signals_detected=["Strong high-risk language detected"],
                recommended_action=(
                    "Please reach out to a crisis helpline or trusted person immediately."
                ),
            )

        # 2. RAG context for grounded analysis
        rag_context = self._rag.retrieve(
            "distress signals emotional risk mental health assessment"
        )
        context_block = (
            f"Reference context:\n{rag_context}\n\n" if rag_context else ""
        )

        prompt = _ANALYSIS_PROMPT.format(context=context_block, text=text)
        raw = self._model.generate_structured(prompt, max_tokens=300)

        # 3. Parse JSON from model output
        try:
            # Extract JSON object even if model adds surrounding text
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                risk_level = RiskLevel(data.get("risk_level", "low"))
                # Honour keyword pre-filter minimum
                if keyword_risk == RiskLevel.MODERATE and risk_level == RiskLevel.LOW:
                    risk_level = RiskLevel.MODERATE
                return DistressAnalysisResponse(
                    risk_level=risk_level,
                    signals_detected=data.get("signals", []),
                    recommended_action=data.get(
                        "recommended_action",
                        "Continue monitoring and consider speaking with a professional.",
                    ),
                )
        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning("Failed to parse distress JSON: %s — raw: %s", exc, raw)

        # Fallback
        return DistressAnalysisResponse(
            risk_level=keyword_risk or RiskLevel.LOW,
            signals_detected=[],
            recommended_action="Consider speaking with a mental-health professional.",
        )
