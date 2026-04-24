from __future__ import annotations

from collections.abc import Callable
import os
from pathlib import Path

from aura import AURA_ROOT


class GlobalPath:
    def __init__(self, resolver: Callable[[], Path]) -> None:
        self._resolver = resolver

    @property
    def path(self) -> Path:
        return self._resolver()


_DEFAULT_AURA_HOME = Path.home() / ".terminal_mind"


def _get_aura_home() -> Path:
    if aura_home := os.getenv("AURA_HOME"):
        return Path(aura_home).expanduser().resolve()
    return _DEFAULT_AURA_HOME


AURA_HOME = GlobalPath(_get_aura_home)
GLOBAL_CONFIG_FILE = GlobalPath(lambda: AURA_HOME.path / "config.toml")
GLOBAL_ENV_FILE = GlobalPath(lambda: AURA_HOME.path / ".env")
GLOBAL_TOOLS_DIR = GlobalPath(lambda: AURA_HOME.path / "tools")
GLOBAL_SKILLS_DIR = GlobalPath(lambda: AURA_HOME.path / "skills")
GLOBAL_AGENTS_DIR = GlobalPath(lambda: AURA_HOME.path / "agents")
GLOBAL_PROMPTS_DIR = GlobalPath(lambda: AURA_HOME.path / "prompts")
SESSION_LOG_DIR = GlobalPath(lambda: AURA_HOME.path / "logs" / "session")
TRUSTED_FOLDERS_FILE = GlobalPath(lambda: AURA_HOME.path / "trusted_folders.toml")
LOG_DIR = GlobalPath(lambda: AURA_HOME.path / "logs")
LOG_FILE = GlobalPath(lambda: AURA_HOME.path / "aura.log")

DEFAULT_TOOL_DIR = GlobalPath(lambda: AURA_ROOT / "core" / "tools" / "builtins")
