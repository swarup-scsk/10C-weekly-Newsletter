"""Prompt loading and variable substitution.

Prompt files may begin with a meta header (a title and notes) separated from the actual
prompt body by a line containing only '---'. We load the body after that marker. Substitution
uses simple {name} replacement so stray characters in the template never raise errors.
"""
from __future__ import annotations

from pathlib import Path

_MARKER = "\n---\n"


def load_prompt_body(path: str | Path) -> str:
    text = Path(path).read_text(encoding="utf-8")
    idx = text.find(_MARKER)
    if idx != -1:
        return text[idx + len(_MARKER):].strip()
    return text.strip()


def render(template: str, **variables) -> str:
    out = template
    for key, value in variables.items():
        out = out.replace("{" + key + "}", str(value))
    return out
