from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.braille_renderer import render_braille

WIDTH = 22
HEIGHT = 12
STARTING_DOTS = [
    {8, 9, 10, 11},
    {9, 10},
    {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18},
    {18, 19, 2, 3},
    {2, 4, 5, 6, 7, 19},
    {2, 4, 5, 6, 7, 19},
    {18, 19, 2, 3},
    {3, 6, 8, 10, 12, 14, 18},
    {18, 3},
    {18, 19, 2, 3},
    {3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18},
    {5, 6, 7, 14, 15, 16},
]
TRANSITIONS = [
    {"remove": {4j + 4, 5j + 3, 5j + 4, 4j + 3}, "add": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 4j + 7, 4j + 8, 5j + 7, 5j + 8, 8j + 6}},
    {"remove": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6, 8j + 6}, "add": {4j + 7, 4j + 8, 4j + 9, 5j + 7, 5j + 8, 5j + 9, 5j + 10, 4j + 10}},
    {"remove": {4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6}, "add": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 5j + 9, 4j + 9, 4j + 10, 4j + 11, 4j + 12, 5j + 10, 5j + 11, 5j + 12, 8j + 6}},
    {"remove": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6, 8j + 6}, "add": {5j + 14, 4j + 11, 4j + 12, 4j + 13, 4j + 14, 5j + 12, 5j + 13, 5j + 11}},
    {"remove": {4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6}, "add": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 5j + 13, 8j + 6, 4j + 13, 4j + 14, 4j + 15, 4j + 16, 5j + 14, 5j + 15, 5j + 16}},
    {"remove": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6, 8j + 6}, "add": {5j + 17, 5j + 18, 5j + 15, 4j + 15, 4j + 16, 4j + 17, 4j + 18, 5j + 16}},
    {"remove": {4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6}, "add": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 5j + 13, 8j + 6, 4j + 13, 4j + 14, 4j + 15, 4j + 16, 5j + 14, 5j + 15, 5j + 16}},
    {"remove": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6, 8j + 6}, "add": {5j + 14, 4j + 11, 4j + 12, 4j + 13, 4j + 14, 5j + 12, 5j + 13, 5j + 11}},
    {"remove": {4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6}, "add": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 5j + 9, 4j + 9, 4j + 10, 4j + 11, 4j + 12, 5j + 10, 5j + 11, 5j + 12, 8j + 6}},
    {"remove": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 4j + 3, 4j + 4, 4j + 5, 5j + 3, 5j + 4, 5j + 5, 4j + 6, 5j + 6, 8j + 6}, "add": {4j + 7, 4j + 8, 4j + 9, 5j + 7, 5j + 8, 5j + 9, 5j + 10, 4j + 10}},
    {"remove": {4j + 4, 5j + 3, 5j + 4, 4j + 3}, "add": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 4j + 7, 4j + 8, 5j + 7, 5j + 8, 8j + 6}},
    {"remove": {8j + 8, 8j + 10, 8j + 12, 8j + 14, 8j + 6}, "add": set[int]()},
](), "add": set[int]()},
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
