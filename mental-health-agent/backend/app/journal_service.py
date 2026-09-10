"""
Journal service – stores entries in memory (swap for a real DB in production)
and optionally analyses them via the Distress Detection Agent.
"""
from __future__ import annotations

import uuid
from typing import Dict, List

from app.agents.distress_agent import DistressDetectionAgent
from app.models import JournalAnalysisResponse, JournalEntry, RiskLevel
from app.rag_pipeline import get_rag_pipeline
from app.watsonx_client import get_chat_client

_store: Dict[str, JournalEntry] = {}


class JournalService:
    def __init__(self):
        self._distress = DistressDetectionAgent()
        self._model = get_chat_client()
        self._rag = get_rag_pipeline()

    def save(self, entry: JournalEntry) -> JournalEntry:
        entry_id = str(uuid.uuid4())
        entry.entry_id = entry_id
        _store[entry_id] = entry
        return entry

    def analyse(self, entry: JournalEntry) -> JournalAnalysisResponse:
        entry_id = entry.entry_id or str(uuid.uuid4())
        distress = self._distress.analyse(entry.content)

        # Generate a supportive reflection
        rag_context = self._rag.retrieve(entry.content, k=3)
        reflection_prompt = (
            f"A user wrote the following private journal entry:\n\"{entry.content}\"\n\n"
            f"Reference context:\n{rag_context}\n\n"
            "Provide a brief (2-3 sentence) warm, supportive reflection on this entry. "
            "Do not diagnose. Do not repeat the user's words back verbatim.\n"
            "Reflection:"
        )
        reflection = self._model.generate(
            reflection_prompt, max_tokens=200, temperature=0.7
        )

        # Derive sentiment label
        sentiment = self._derive_sentiment(distress.risk_level)

        # Suggestions based on risk
        suggestions = self._build_suggestions(distress.risk_level)

        return JournalAnalysisResponse(
            entry_id=entry_id,
            sentiment=sentiment,
            risk_level=distress.risk_level,
            reflection=reflection,
            suggestions=suggestions,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _derive_sentiment(risk: RiskLevel) -> str:
        return {
            RiskLevel.LOW: "Generally positive / neutral",
            RiskLevel.MODERATE: "Signs of stress or low mood",
            RiskLevel.HIGH: "Significant emotional distress",
        }[risk]

    @staticmethod
    def _build_suggestions(risk: RiskLevel) -> List[str]:
        base = [
            "Try a short breathing exercise — inhale 4s, hold 4s, exhale 6s.",
            "Journaling regularly can help track emotional patterns over time.",
        ]
        if risk == RiskLevel.MODERATE:
            base += [
                "Consider talking to a trusted friend or counselor about how you're feeling.",
                "A short walk or gentle movement can help shift your mood.",
            ]
        elif risk == RiskLevel.HIGH:
            base = [
                "Please consider reaching out to a mental-health professional or crisis helpline today.",
                "You do not have to carry this alone — trusted support is available 24/7.",
            ]
        return base
