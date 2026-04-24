import math
from aura.cli.textual_ui.widgets.braille_renderer import render_braille

cx, cy = 10.5, 5.5
grid_w, grid_h = 22, 12

def get_circle(r_inner, r_outer):
    dots = set()
    for y in range(grid_h):
        for x in range(grid_w):
            d = math.hypot((x - cx), y - cy)
            if r_inner <= d <= r_outer:
                dots.add(x + y*1j)
    return set(dots)

def get_spokes(angle_offset):
    dots = set()
    for y in range(grid_h):
        for x in range(grid_w):
            d = math.hypot((x - cx), y - cy)
            if 2.0 <= d <= 5.0:
                angle = math.degrees(math.atan2(y - cy, (x - cx))) % 360
                for i in range(3):
                    target = (angle_offset + i * 120) % 360
                    diff = abs(angle - target)
                    if diff > 180: diff = 360 - diff
                    if diff < 15:
                        dots.add(x + y*1j)
    return set(dots)

outer = get_circle(4.5, 5.5)
core = get_circle(0, 2.0)
spokes = get_spokes(0)

base = outer | core | spokes
print("BRAILLE:")
print(render_braille(base, grid_w, grid_h))
