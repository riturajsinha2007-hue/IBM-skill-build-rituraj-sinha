"""
Mental Health Awareness Agent

Retrieves and explains reliable, educational mental-health information
using the RAG pipeline backed by trusted knowledge sources.
"""
from __future__ import annotations

import logging
from typing import List

from app.models import Message
from app.rag_pipeline import get_rag_pipeline
from app.watsonx_client import get_chat_client

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are a knowledgeable mental-health awareness educator.

Your role:
- Explain mental-health topics (stress, anxiety, depression, mindfulness, etc.)
  in clear, accessible language.
- Base your explanations strictly on the reference context provided below.
- If the reference context does not contain an answer, say so honestly and
  suggest the user consult a professional or visit a trusted resource.
- NEVER diagnose any condition.
- Provide practical, evidence-informed general information only.
- End with a gentle reminder that professional support is available.

Reference context (from verified mental-health sources):
{rag_context}

Conversation so far:
{history}

User: {user_message}
Assistant:"""


class AwarenessAgent:
    """Provides RAG-grounded educational mental-health information."""

    def __init__(self):
        self._model = get_chat_client()
        self._rag = get_rag_pipeline()

    def respond(self, message: str, history: List[Message]) -> str:
        rag_context = self._rag.retrieve(message, k=5)
        history_text = self._format_history(history)

        prompt = _SYSTEM_PROMPT.format(
            rag_context=rag_context or "No specific reference material found.",
            history=history_text or "No previous messages.",
            user_message=message,
        )

        return self._model.generate(prompt, max_tokens=500, temperature=0.5)

    @staticmethod
    def _format_history(history: List[Message]) -> str:
        if not history:
            return ""
        lines = []
        for msg in history[-6:]:
            role = "User" if msg.role == "user" else "Assistant"
            lines.append(f"{role}: {msg.content}")
        return "\n".join(lines)
