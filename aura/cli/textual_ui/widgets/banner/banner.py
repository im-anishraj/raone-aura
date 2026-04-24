from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Static

from aura import __version__
from aura.cli.textual_ui.widgets.banner.petit_chat import PetitChat
from aura.cli.textual_ui.widgets.no_markup_static import NoMarkupStatic
from aura.core.config import AuraConfig
from aura.core.skills.manager import SkillManager


@dataclass
class BannerState:
    active_model: str = ""
    models_count: int = 0
    mcp_servers_count: int = 0
    skills_count: int = 0


class Banner(Static):
    state = reactive(BannerState(), init=False)

    def __init__(
        self, config: AuraConfig, skill_manager: SkillManager, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.can_focus = False
        self._initial_state = BannerState(
            active_model=config.active_model,
            models_count=len(config.models),
            mcp_servers_count=len(config.mcp_servers),
            skills_count=len(skill_manager.available_skills),
        )
        self._animated = not config.disable_welcome_banner_animation

    def compose(self) -> ComposeResult:
        with Horizontal(id="banner-container"):
            yield PetitChat(animate=self._animated)

            with Vertical(id="banner-info"):
                with Horizontal(classes="banner-line"):
                    yield NoMarkupStatic(f"RaOne Aura v{__version__}", id="banner-brand")
                    yield NoMarkupStatic(" ━━ Autonomous AI Terminal Agent", id="banner-description")

                with Horizontal(classes="banner-line"):
                    yield NoMarkupStatic("Built by Anish Raj", id="banner-author")

                with Horizontal(classes="banner-line"):
                    yield NoMarkupStatic("", classes="banner-meta")  # Spacer

                with Horizontal(classes="banner-line"):
                    yield NoMarkupStatic("Shell: Git Bash │ CMD │ PowerShell", classes="banner-meta")

                with Horizontal(classes="banner-line"):
                    yield NoMarkupStatic("Type /help to begin ─ /settings to configure", classes="banner-meta")

    def on_mount(self) -> None:
        self.state = self._initial_state

    def freeze_animation(self) -> None:
        if self._animated:
            self.query_one(PetitChat).freeze_animation()

    def set_state(self, config: AuraConfig, skill_manager: SkillManager) -> None:
        self.state = BannerState(
            active_model=config.active_model,
            models_count=len(config.models),
            mcp_servers_count=len(config.mcp_servers),
            skills_count=len(skill_manager.available_skills),
        )

    def watch_state(self, state: BannerState) -> None:
        if not self.is_mounted:
            return

        try:
            self.query_one("#banner-model", NoMarkupStatic).update(state.active_model)
            self.query_one("#banner-meta-counts", NoMarkupStatic).update(
                f"{state.models_count} models · "
                f"{state.mcp_servers_count} MCP servers · "
                f"{state.skills_count} skills"
            )
        except Exception:
            pass
