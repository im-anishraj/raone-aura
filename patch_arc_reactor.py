import re

grid_w, grid_h = 22, 12
cx, cy = 10.5, 5.5

def get_circle(r_inner, r_outer):
    import math
    dots = set()
    for y in range(grid_h):
        for x in range(grid_w):
            d = math.hypot((x - cx), y - cy)
            if r_inner <= d <= r_outer:
                dots.add(x + y*1j)
    return dots

def get_spokes(angle_offset):
    import math
    dots = set()
    for y in range(grid_h):
        for x in range(grid_w):
            d = math.hypot((x - cx), y - cy)
            if 1.5 <= d <= 5.0:
                angle = math.degrees(math.atan2(y - cy, (x - cx))) % 360
                for i in range(3):
                    target = (angle_offset + i * 120) % 360
                    diff = abs(angle - target)
                    if diff > 180: diff = 360 - diff
                    if diff < 20:
                        dots.add(x + y*1j)
    return dots

outer = get_circle(4.5, 5.5)
core = get_circle(0, 2.0)

num_frames = 6
frames = []
for i in range(num_frames):
    offset = i * (120 / num_frames)
    frames.append(get_spokes(offset))

starting_dots_set = outer | core | frames[0]

starting_dots = []
for y in range(grid_h):
    s = set()
    for x in range(grid_w):
        if (x + y*1j) in starting_dots_set:
            s.add(x)
    starting_dots.append(s)

transitions_code = []
curr_spokes = frames[0]
for i in range(num_frames):
    next_spokes = frames[(i+1) % num_frames]
    
    if i % 2 == 0:
        core_diff = get_circle(1.5, 2.0)
        remove = (curr_spokes - next_spokes) | core_diff
        add = (next_spokes - curr_spokes)
    else:
        core_diff = get_circle(1.5, 2.0)
        remove = (curr_spokes - next_spokes)
        add = (next_spokes - curr_spokes) | core_diff

    remove_str = "{" + ", ".join(f"{int(c.imag)}j + {int(c.real)}" for c in remove) + "}" if remove else "set[int]()"
    add_str = "{" + ", ".join(f"{int(c.imag)}j + {int(c.real)}" for c in add) + "}" if add else "set[int]()"
    transitions_code.append(f"    {{\"remove\": {remove_str}, \"add\": {add_str}}},")

with open("aura/cli/textual_ui/widgets/banner/petit_chat.py", "r", encoding="utf-8") as f:
    content = f.read()

sd_str = "STARTING_DOTS = [\n"
for s in starting_dots:
    if len(s) == 0:
        sd_str += "    set[int](),\n"
    else:
        sd_str += f"    {s},\n"
sd_str += "]"

tr_str = "TRANSITIONS = [\n" + "\n".join(transitions_code) + "\n]"

content = re.sub(r"STARTING_DOTS = \[.*?\]", sd_str, content, flags=re.DOTALL)
content = re.sub(r"TRANSITIONS = \[.*?\]", tr_str, content, flags=re.DOTALL)

with open("aura/cli/textual_ui/widgets/banner/petit_chat.py", "w", encoding="utf-8") as f:
    f.write(content)
