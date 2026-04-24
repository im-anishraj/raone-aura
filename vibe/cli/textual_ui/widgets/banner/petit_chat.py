from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.braille_renderer import render_braille

WIDTH = 22
HEIGHT = 12
STARTING_DOTS = [
    set[int](),
    {8, 9, 10, 11, 12, 13},
    {8, 9, 14, 7},
    {6, 8, 9, 10, 15},
    {6, 9, 10, 11, 15},
    {6, 9, 10, 11, 12, 13, 14, 15},
    {6, 9, 10, 11, 12, 13, 14, 15},
    {6, 9, 10, 11, 15},
    {6, 8, 9, 10, 15},
    {8, 9, 14, 7},
    {8, 9, 10, 11, 12, 13},
    set[int](),
]
TRANSITIONS = [
    {"remove": {2j + 7, 2j + 8, 3j + 8, 3j + 9, 4j + 9, 4j + 10, 4j + 11, 5j + 9, 5j + 12, 4j + 15, 5j + 13, 5j + 14, 5j + 15, 7j + 10, 7j + 11, 8j + 10, 6j + 9, 9j + 9, 6j + 12, 10j + 9}, "add": {7j + 13, 7j + 14, 8j + 14, 1j + 10, 1j + 11, 2j + 10, 2j + 11, 7j + 7, 7j + 8, 8j + 7}},
    {"remove": {2j + 7, 2j + 8, 2j + 9, 4j + 9, 4j + 10, 4j + 15, 6j + 12, 6j + 13, 6j + 14, 6j + 15, 8j + 8, 8j + 9, 8j + 10, 10j + 9, 1j + 9, 3j + 8, 3j + 9, 3j + 10, 5j + 12, 5j + 13, 5j + 14, 7j + 9, 5j + 15, 7j + 10, 9j + 7, 9j + 8, 7j + 15, 9j + 9}, "add": {6j + 12, 1j + 10, 1j + 11, 1j + 12, 2j + 10, 2j + 11, 2j + 12, 5j + 9, 3j + 11, 4j + 10, 4j + 11, 6j + 6, 6j + 7, 6j + 8, 6j + 9, 7j + 6, 7j + 7, 7j + 8, 8j + 7, 7j + 11, 7j + 12, 7j + 13, 7j + 14, 8j + 12, 8j + 13, 8j + 14, 5j + 12, 9j + 13, 9j + 14, 7j + 10}},
    {"remove": {1j + 9, 2j + 7, 2j + 8, 2j + 9, 3j + 8, 3j + 9, 3j + 10, 7j + 11, 4j + 9, 4j + 10, 4j + 11, 5j + 9, 4j + 15, 5j + 12, 5j + 13, 6j + 12, 6j + 13, 6j + 14, 6j + 15, 8j + 8, 8j + 9, 8j + 10, 5j + 14, 7j + 9, 10j + 9, 7j + 10, 9j + 7, 9j + 8, 7j + 15, 9j + 9, 5j + 15, 6j + 9}, "add": {2j + 12, 2j + 13, 2j + 14, 4j + 6, 4j + 11, 6j + 6, 4j + 12, 6j + 7, 6j + 8, 6j + 9, 8j + 11, 8j + 12, 8j + 13, 10j + 12, 1j + 12, 3j + 11, 3j + 12, 3j + 13, 5j + 8, 5j + 6, 5j + 7, 5j + 9, 7j + 6, 7j + 11, 7j + 12, 9j + 12, 9j + 13, 9j + 14}},
    {"remove": {2j + 7, 2j + 8, 2j + 9, 4j + 9, 4j + 10, 4j + 15, 6j + 12, 6j + 13, 6j + 14, 6j + 15, 8j + 8, 8j + 9, 8j + 10, 10j + 9, 1j + 9, 3j + 8, 3j + 9, 3j + 10, 5j + 12, 5j + 13, 5j + 14, 7j + 9, 5j + 15, 7j + 10, 9j + 7, 9j + 8, 7j + 15, 9j + 9}, "add": {5j + 6, 3j + 7, 4j + 6, 4j + 7, 2j + 13, 2j + 14, 4j + 8, 3j + 12, 4j + 12, 4j + 13, 4j + 14, 3j + 13, 3j + 14, 5j + 8, 5j + 9, 5j + 7, 7j + 11, 6j + 9, 5j + 12, 8j + 11, 6j + 12, 9j + 10, 9j + 11, 9j + 12, 10j + 10, 10j + 11, 10j + 12, 7j + 10, 4j + 10, 4j + 11}},
    {"remove": {1j + 9, 2j + 9, 3j + 10, 4j + 10, 4j + 11, 5j + 9, 7j + 10, 6j + 9, 5j + 12, 7j + 9, 6j + 12, 6j + 14, 6j + 15, 8j + 8, 8j + 9, 9j + 7, 9j + 8, 7j + 15, 6j + 13, 7j + 11}, "add": {9j + 10, 9j + 11, 10j + 10, 10j + 11, 3j + 7, 4j + 7, 4j + 8, 3j + 14, 4j + 13, 4j + 14}},
    {"remove": set[int](), "add": {7j + 11, 6j + 9, 4j + 10, 4j + 11, 5j + 9, 5j + 12, 6j + 12, 7j + 10}},
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
