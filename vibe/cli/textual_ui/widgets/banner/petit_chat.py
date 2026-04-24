from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.braille_renderer import render_braille

WIDTH = 22
HEIGHT = 12
STARTING_DOTS = [
    {8, 9, 10, 11, 12, 13},
    {14, 15, 6, 7},
    {16, 10, 11, 5},
    {9, 4, 12, 17},
    {4, 8, 9, 10, 11, 12, 13, 17},
    {9, 4, 12, 17},
    {17, 10, 11, 4},
    {17, 4, 14, 7},
    {16, 9, 12, 5},
    {6, 7, 10, 11, 14, 15},
    {14, 7},
    {6, 15},
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
