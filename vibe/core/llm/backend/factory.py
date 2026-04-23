from __future__ import annotations

from vibe.core.config import Backend
from vibe.core.llm.backend.generic import GenericBackend
from vibe.core.llm.backend.mistral import MistralBackend
from vibe.core.llm.backend.openai import OpenAIBackend

BACKEND_FACTORY = {
    Backend.MISTRAL: MistralBackend,
    Backend.OPENAI: OpenAIBackend,
    Backend.GENERIC: GenericBackend,
    Backend.OLLAMA: GenericBackend,
}
