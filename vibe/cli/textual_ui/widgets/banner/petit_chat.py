from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.braille_renderer import render_braille

WIDTH = 22
HEIGHT = 12
STARTING_DOTS = [
    {5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
    {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17},
    {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18},
    {2, 3, 4, 5, 6, 14, 15, 16, 17, 18},
    {1, 2, 3, 4, 5, 6, 14, 15, 16, 17, 18, 19},
    {2, 3, 4, 5, 9, 10, 11, 15, 16, 17, 18},
    {2, 3, 4, 9, 10, 11, 16, 17, 18},
    {3, 4, 5, 9, 10, 11, 15, 16, 17},
    {4, 5, 8, 9, 10, 11, 12, 15, 16},
    {16, 4, 5, 15},
    {6, 8, 10, 12, 14},
    {13, 7},
]
TRANSITIONS = [
    {"remove": set[int](), "add": set[int]()},
]
# cf render_braille() docstring for coordinates convention


class PetitChat(Static):
    def __init__(self, animate: bool = True, **kwargs: Any) -> None:
        super().__init__(**kwargs, classes="banner-chat")
        self._dots = {1j * y + x for y, row in enumerate(STARTING_DOTS) for x in row}
        self._transition_index = 0
        self._do_animate = animate
        self._freeze_requested = False
        self._timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Static(render_braille(self._dots, WIDTH, HEIGHT), classes="petit-chat")

    def on_mount(self) -> None:
        self._inner = self.query_one(".petit-chat", Static)
        if self._do_animate:
            self._timer = self.set_interval(0.16, self._apply_next_transition)

    def freeze_animation(self) -> None:
        self._freeze_requested = True

    def _apply_next_transition(self) -> None:
        if self._freeze_requested and self._transition_index == 0:
            if self._timer:
                self._timer.stop()
            self._timer = None
            return

        transition = TRANSITIONS[self._transition_index]
        self._dots -= transition["remove"]
        self._dots |= transition["add"]
        self._transition_index = (self._transition_index + 1) % len(TRANSITIONS)
        self._inner.update(render_braille(self._dots, WIDTH, HEIGHT))
