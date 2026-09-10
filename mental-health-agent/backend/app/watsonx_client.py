"""
IBM watsonx.ai Granite model client.

Wraps the ibm-watsonx-ai SDK and exposes a simple generate() interface
that agents can call.
"""
from __future__ import annotations

import logging
from typing import List, Optional

from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as Params

from app.config import get_settings

logger = logging.getLogger(__name__)
_settings = get_settings()


def _build_client() -> APIClient:
    creds = Credentials(
        url=_settings.watsonx_url,
        api_key=_settings.watsonx_api_key,
    )
    return APIClient(creds)


class GraniteClient:
    """Thin wrapper around IBM Granite model inference."""

    def __init__(self, model_id: Optional[str] = None):
        self._model_id = model_id or _settings.granite_chat_model
        self._client = _build_client()
        self._model = ModelInference(
            model_id=self._model_id,
            api_client=self._client,
            project_id=_settings.watsonx_project_id,
        )

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        stop_sequences: Optional[List[str]] = None,
    ) -> str:
        """Call Granite and return the generated text string."""
        params = {
            Params.MAX_NEW_TOKENS: max_tokens,
            Params.TEMPERATURE: temperature,
            Params.DECODING_METHOD: "sample",
        }
        if stop_sequences:
            params[Params.STOP_SEQUENCES] = stop_sequences

        try:
            result = self._model.generate_text(prompt=prompt, params=params)
            return result.strip()
        except Exception as exc:
            logger.error("Granite generate error: %s", exc)
            return (
                "I'm sorry, I'm having trouble generating a response right now. "
                "If you're in distress, please reach out to a crisis helpline immediately."
            )

    def generate_structured(self, prompt: str, max_tokens: int = 256) -> str:
        """Lower-temperature call for structured / analytical outputs."""
        return self.generate(prompt, max_tokens=max_tokens, temperature=0.2)


# Singleton – shared across agents
_granite_chat: Optional[GraniteClient] = None
_granite_instruct: Optional[GraniteClient] = None


def get_chat_client() -> GraniteClient:
    global _granite_chat
    if _granite_chat is None:
        _granite_chat = GraniteClient(_settings.granite_chat_model)
    return _granite_chat


def get_instruct_client() -> GraniteClient:
    global _granite_instruct
    if _granite_instruct is None:
        _granite_instruct = GraniteClient(_settings.granite_instruct_model)
    return _granite_instruct
