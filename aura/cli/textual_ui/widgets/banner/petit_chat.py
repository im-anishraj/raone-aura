from __future__ import annotations

import math
from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from aura.cli.textual_ui.widgets.braille_renderer import render_braille

class PetitChat(Static):
    """
    A premium 3D animated "Cybernetic Core" (double rotating cube / tesseract) 
    rendered using braille dots.
    """
    def __init__(self, animate: bool = True, **kwargs: Any) -> None:
        super().__init__(**kwargs, classes="banner-chat")
        self._transition_index = 0
        self._do_animate = animate
        self._freeze_requested = False
        self._timer: Timer | None = None
        self.WIDTH = 34
        self.HEIGHT = 20

    def compose(self) -> ComposeResult:
        yield Static(
            render_braille(self._generate_dots(0), self.WIDTH, self.HEIGHT), 
            classes="petit-chat"
        )

    def on_mount(self) -> None:
        self._inner = self.query_one(".petit-chat", Static)
        if self._do_animate:
            self._timer = self.set_interval(0.08, self._apply_next_transition)

    def freeze_animation(self) -> None:
        self._freeze_requested = True

    def _apply_next_transition(self) -> None:
        if self._freeze_requested and self._transition_index == 0:
            if self._timer:
                self._timer.stop()
            self._timer = None
            return

        self._transition_index += 1
        dots = self._generate_dots(self._transition_index)
        self._inner.update(render_braille(dots, self.WIDTH, self.HEIGHT))
        
    def _generate_dots(self, t: int) -> set[complex]:
        dots = set()
        cx, cy = self.WIDTH / 2 - 0.5, self.HEIGHT / 2 - 0.5
        
        pulse = math.sin(t * 0.05) * 0.1 + 1.0
        
        rx1, ry1, rz1 = t * 0.03, t * 0.05, t * 0.02
        rx2, ry2, rz2 = -t * 0.04, -t * 0.03, t * 0.06
        
        v_base = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]
        
        edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        
        projected = []
        
        for x, y, z in v_base:
            px, py, pz = self._rotate_3d(x, y, z, rx1, ry1, rz1)
            scale = 8 * pulse
            projected.append((cx + px * scale, cy + py * scale))
            
        for x, y, z in v_base:
            px, py, pz = self._rotate_3d(x, y, z, rx2, ry2, rz2)
            scale = 3.5 * (2.0 - pulse)
            projected.append((cx + px * scale, cy + py * scale))
            
        for e1, e2 in edges:
            dots.update(self._bresenham(projected[e1][0], projected[e1][1], projected[e2][0], projected[e2][1]))
            
        for e1, e2 in edges:
            o = 8
            dots.update(self._bresenham(projected[e1+o][0], projected[e1+o][1], projected[e2+o][0], projected[e2+o][1]))
            
        for i in range(8):
            dots.update(self._bresenham(projected[i][0], projected[i][1], projected[i+8][0], projected[i+8][1]))
            
        return {d for d in dots if 0 <= d.real < self.WIDTH and 0 <= d.imag < self.HEIGHT}
        
    def _rotate_3d(self, x: float, y: float, z: float, rx: float, ry: float, rz: float) -> tuple[float, float, float]:
        y1 = y * math.cos(rx) - z * math.sin(rx)
        z1 = y * math.sin(rx) + z * math.cos(rx)
        
        x2 = x * math.cos(ry) + z1 * math.sin(ry)
        z2 = -x * math.sin(ry) + z1 * math.cos(ry)
        
        x3 = x2 * math.cos(rz) - y1 * math.sin(rz)
        y3 = x2 * math.sin(rz) + y1 * math.cos(rz)
        
        return x3, y3, z2
        
    def _bresenham(self, x0: float, y0: float, x1: float, y1: float) -> set[complex]:
        points = set()
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            points.add(x0 + y0 * 1j)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return points
