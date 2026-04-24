from __future__ import annotations

from aura.core.config import Backend
from aura.core.llm.backend.generic import GenericBackend
from aura.core.llm.backend.mistral import MistralBackend
from aura.core.llm.backend.openai import OpenAIBackend

BACKEND_FACTORY = {
    Backend.MISTRAL: MistralBackend,
    Backend.OPENAI: OpenAIBackend,
    Backend.GENERIC: GenericBackend,
    Backend.OLLAMA: GenericBackend,
}
