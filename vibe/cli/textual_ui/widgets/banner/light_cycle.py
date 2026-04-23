from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.braille_renderer import render_braille

WIDTH = 50
HEIGHT = 16

# TRON Light Cycle ASCII representation in dots
BIKE_DOT_LIST = [
    set[int](), # Row 0
    set[int](), # Row 1
    {15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25}, # Row 2: Top bar
    {13, 14, 26, 27}, # Row 3
    {11, 12, 28, 29}, # Row 4
    {3, 4, 5, 6, 7, 8, 9, 10, 30, 31, 32, 33, 34, 35, 36}, # Row 5: Side extension
    {2, 7, 10, 31, 37}, # Row 6
    {1, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 38}, # Row 7: Long horizontal
    {1, 7, 31, 39}, # Row 8
    {1, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 39}, # Row 9
    {2, 7, 31, 38}, # Row 10
    {3, 4, 5, 6, 8, 9, 10, 32, 33, 34, 35, 36, 37}, # Row 11
    {11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30}, # Row 12: Bottom bar
]

class LightCycle(Static):
    def __init__(self, animate: bool = True, **kwargs: Any) -> None:
        super().__init__(**kwargs, classes="banner-chat")
        self._base_dots = {1j * y + x for y, row in enumerate(BIKE_DOT_LIST) for x in row}
        self._offset = 0
        self._do_animate = animate
        self._timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Static(render_braille(self._base_dots, WIDTH, HEIGHT), classes="petit-chat")

    def on_mount(self) -> None:
        self._inner = self.query_one(".petit-chat", Static)
        if self._do_animate:
            self._timer = self.set_interval(0.1, self._animate)

    def freeze_animation(self) -> None:
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _animate(self) -> None:
        self._offset = (self._offset + 1) % WIDTH
        # Move the bike and wrap around
        dots = {1j * y + (x + self._offset) % WIDTH for y, x in [(int(d.imag), int(d.real)) for d in self._base_dots]}
        
        # Add a few random "sparks" or light streaks
        import random
        for _ in range(2):
            dots.add(1j * random.randint(2, 12) + random.randint(0, WIDTH - 1))

        # Clamp points to prevent any out-of-bounds just in case
        valid_dots = {d for d in dots if 0 <= d.real < WIDTH and 0 <= d.imag < HEIGHT}
        self._inner.update(render_braille(valid_dots, WIDTH, HEIGHT))
