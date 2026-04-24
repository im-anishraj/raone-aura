import math
from aura.cli.textual_ui.widgets.braille_renderer import render_braille

cx, cy = 10.5, 5.5
grid_w, grid_h = 22, 12

def get_circle(r_inner, r_outer):
    dots = set()
    for y in range(grid_h):
        for x in range(grid_w):
            d = math.hypot((x - cx)*0.8, y - cy) # adjusted for aspect ratio
            if r_inner <= d <= r_outer:
                dots.add(x + y*1j)
    return dots

def get_spokes(angle_offset):
    dots = set()
    for y in range(grid_h):
        for x in range(grid_w):
            d = math.hypot((x - cx)*0.8, y - cy)
            if 1.5 <= d <= 4.5:
                angle = math.degrees(math.atan2(y - cy, (x - cx)*0.8)) % 360
                for i in range(3):
                    target = (angle_offset + i * 120) % 360
                    diff = abs(angle - target)
                    if diff > 180: diff = 360 - diff
                    if diff < 20:
                        dots.add(x + y*1j)
    return dots

outer = get_circle(4.5, 5.5)
core = get_circle(0, 1.5)
spokes0 = get_spokes(0)

base = outer | core | spokes0
print("BRAILLE:")
print(render_braille(base, grid_w, grid_h))
