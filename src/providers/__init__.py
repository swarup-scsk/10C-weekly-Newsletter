"""Provider registry / factory.

`get_provider("anthropic", "claude-opus-4-8")` returns a ready provider instance.
Register new providers by adding them to `_REGISTRY`.
"""
from __future__ import annotations

from .base import Citation, LLMProvider, LLMResponse

_REGISTRY = {
    "anthropic": ("anthropic_provider", "AnthropicProvider"),
    "openai": ("openai_provider", "OpenAIProvider"),
    "gemini": ("gemini_provider", "GeminiProvider"),
}


def get_provider(name: str, model: str, **options) -> LLMProvider:
    if name not in _REGISTRY:
        raise ValueError(
            f"Unknown provider '{name}'. Available: {', '.join(sorted(_REGISTRY))}"
        )
    module_name, class_name = _REGISTRY[name]
    import importlib
    module = importlib.import_module(f".{module_name}", package=__name__)
    provider_cls = getattr(module, class_name)
    return provider_cls(model, **options)


__all__ = ["get_provider", "LLMProvider", "LLMResponse", "Citation"]
