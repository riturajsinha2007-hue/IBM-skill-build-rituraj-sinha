"""
Crisis Response Agent

Activated when a HIGH risk level is detected.  Prioritises user safety,
provides verified crisis resources, and encourages immediate human contact.

SAFETY RULES (enforced in prompts and post-processing):
  - Never provide methods or instructions for self-harm.
  - Never trivialise or dismiss the user's feelings.
  - Always direct to human help.
  - Never act as a therapist or emergency responder.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from app.models import Message, Resource
from app.rag_pipeline import get_rag_pipeline
from app.watsonx_client import get_chat_client

logger = logging.getLogger(__name__)

# Verified global / regional crisis resources
_CRISIS_RESOURCES: List[Resource] = [
    Resource(
        name="iCall (India)",
        description="Psychosocial helpline for mental-health support.",
        contact="9152987821",
        url="https://icallhelpline.org",
        location="India",
    ),
    Resource(
        name="Vandrevala Foundation (India)",
        description="24×7 mental-health helpline.",
        contact="1860-2662-345",
        url="https://www.vandrevalafoundation.com",
        location="India",
    ),
    Resource(
        name="Snehi (India)",
        description="Emotional support and suicide prevention helpline.",
        contact="+91-44-24640050",
        url="https://snehi.org",
        location="India",
    ),
    Resource(
        name="988 Suicide & Crisis Lifeline (USA)",
        description="Free, confidential crisis support 24/7.",
        contact="988",
        url="https://988lifeline.org",
        location="USA",
    ),
    Resource(
        name="Crisis Text Line (USA/UK/Canada)",
        description="Text HOME to 741741 for free crisis support.",
        contact="Text HOME to 741741",
        url="https://www.crisistextline.org",
        location="USA, UK, Canada",
    ),
    Resource(
        name="Samaritans (UK & Ireland)",
        description="Emotional support for anyone in distress.",
        contact="116 123",
        url="https://www.samaritans.org",
        location="UK, Ireland",
    ),
    Resource(
        name="Befrienders Worldwide",
        description="Global network of emotional-support volunteers.",
        url="https://www.befrienders.org",
        location="Global",
    ),
    Resource(
        name="WHO Mental Health Resources",
        description="WHO guidance on mental-health crises and support.",
        url="https://www.who.int/health-topics/mental-health",
        location="Global",
    ),
]

_CRISIS_PROMPT = """\
You are a compassionate crisis-support companion.  A user is experiencing
significant emotional distress or may be in crisis.

Your ONLY goals right now:
1. Acknowledge the user's pain with deep compassion — they are heard.
2. Gently but clearly encourage them to contact a crisis helpline or a trusted
   person RIGHT NOW.
3. Remind them that this feeling is temporary and help is available.
4. Do NOT provide any information about methods of self-harm.
5. Do NOT attempt to solve underlying life problems.
6. Do NOT act as a therapist.
7. Keep the response warm, brief (3-5 sentences), and focused on getting
   the user to reach out to a human.

Reference context:
{rag_context}

User message: {user_message}

Compassionate response:"""


class CrisisResponseAgent:
    """Safety-first agent for HIGH-risk conversations."""

    def __init__(self):
        self._model = get_chat_client()
        self._rag = get_rag_pipeline()

    def respond(
        self,
        message: str,
        history: List[Message],
        location: Optional[str] = None,
    ) -> tuple[str, List[Resource]]:
        """Return (response_text, crisis_resources)."""
        rag_context = self._rag.retrieve(
            "crisis support suicide prevention immediate help", k=3
        )

        prompt = _CRISIS_PROMPT.format(
            rag_context=rag_context or "",
            user_message=message,
        )

        reply = self._model.generate(prompt, max_tokens=300, temperature=0.6)
        reply = self._safety_filter(reply)

        resources = self._select_resources(location)
        return reply, resources

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _safety_filter(text: str) -> str:
        """Block any accidentally generated harmful content."""
        harmful_patterns = [
            "how to", "method", "overdose on", "use a", "jump from",
            "tie a", "hang", "cut your",
        ]
        lower = text.lower()
        for pattern in harmful_patterns:
            if pattern in lower:
                logger.warning(
                    "Safety filter triggered – replacing response. Pattern: %s", pattern
                )
                return (
                    "I hear that you're in a lot of pain right now, and I want you to know "
                    "that your life has value. Please reach out to a crisis helpline or a "
                    "trusted person immediately — you don't have to face this alone. "
                    "Help is available 24/7."
                )
        return text

    @staticmethod
    def _select_resources(location: Optional[str]) -> List[Resource]:
        """Return location-relevant resources, always include global ones."""
        if not location:
            return _CRISIS_RESOURCES

        location_lower = location.lower()
        relevant = [
            r for r in _CRISIS_RESOURCES
            if r.location
            and (
                location_lower in r.location.lower()
                or "global" in r.location.lower()
            )
        ]
        return relevant if relevant else _CRISIS_RESOURCES
