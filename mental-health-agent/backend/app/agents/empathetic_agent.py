"""
Empathetic Support Agent

Handles general mental-health conversations at LOW and MODERATE concern
levels. Provides supportive, context-aware, non-diagnostic responses
grounded in RAG-retrieved educational content.
"""
from __future__ import annotations

import logging
from typing import List

from app.models import Message
from app.rag_pipeline import get_rag_pipeline
from app.watsonx_client import get_chat_client

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are an empathetic, warm mental-health support companion.

Your role:
- Listen attentively and respond with care and compassion.
- Provide supportive reflections and acknowledge emotions.
- Share general coping strategies, mindfulness tips, or self-care suggestions
  when appropriate.
- Ask one gentle follow-up question to understand the user better.
- NEVER diagnose any medical or psychological condition.
- NEVER provide medical advice or prescriptions.
- ALWAYS remind users that you are an AI and not a replacement for professional care.
- If the user expresses ongoing distress, gently encourage professional support.

Use the following reference context (from verified sources) if relevant:
{rag_context}

Conversation so far:
{history}

User: {user_message}
Assistant:"""


class EmpatheticSupportAgent:
    """Generates warm, supportive conversational responses."""

    def __init__(self):
        self._model = get_chat_client()
        self._rag = get_rag_pipeline()

    def respond(self, message: str, history: List[Message]) -> str:
        rag_context = self._rag.retrieve(message)
        history_text = self._format_history(history)

        prompt = _SYSTEM_PROMPT.format(
            rag_context=rag_context or "No additional reference context available.",
            history=history_text or "No previous messages.",
            user_message=message,
        )

        response = self._model.generate(prompt, max_tokens=450, temperature=0.75)
        return self._append_disclaimer(response)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_history(history: List[Message]) -> str:
        if not history:
            return ""
        lines = []
        for msg in history[-10:]:  # keep last 10 turns
            role = "User" if msg.role == "user" else "Assistant"
            lines.append(f"{role}: {msg.content}")
        return "\n".join(lines)

    @staticmethod
    def _append_disclaimer(text: str) -> str:
        disclaimer = (
            "\n\n---\n*Remember: I'm an AI support companion, not a licensed therapist. "
            "For professional support, please consider speaking with a mental-health professional.*"
        )
        if "not a replacement" not in text.lower() and "AI" not in text:
            return text + disclaimer
        return text
