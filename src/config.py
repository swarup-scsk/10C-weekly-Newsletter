"""Configuration loader.

Loads a YAML config file and expands ${ENV_VAR} references from the environment.
Keeping config in one place (and out of code) is what lets every stage be swapped
without touching the pipeline.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

_ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")


def _expand(value: Any) -> Any:
    """Recursively expand ${VAR} references in strings."""
    if isinstance(value, str):
        def repl(m: re.Match) -> str:
            return os.environ.get(m.group(1), "")
        return _ENV_PATTERN.sub(repl, value)
    if isinstance(value, dict):
        return {k: _expand(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand(v) for v in value]
    return value


class Config:
    """Thin wrapper around the parsed config dict with dotted-path access."""

    def __init__(self, data: dict, base_dir: Path):
        self._data = data
        self.base_dir = base_dir

    @classmethod
    def load(cls, path: str | Path) -> "Config":
        path = Path(path)
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return cls(_expand(data), base_dir=path.resolve().parent)

    def get(self, dotted: str, default: Any = None) -> Any:
        node: Any = self._data
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def resolve(self, relative: str) -> Path:
        """Resolve a path (e.g. a prompt file) relative to the config location."""
        return (self.base_dir / relative).resolve()

    def __getitem__(self, key: str) -> Any:
        return self._data[key]
