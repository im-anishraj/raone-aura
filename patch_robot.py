import re

grid = [
  "        XXXX          ",
  "         XX           ",
  "   XXXXXXXXXXXXXXXX   ",
  "  XX              XX  ",
  "  X OOOO           X  ",
  "  X OOOO           X  ",
  "  XX              XX  ",
  "   X  X X X X X   X   ",
  "   X              X   ",
  "  XX              XX  ",
  "   XXXXXXXXXXXXXXXX   ",
  "     XXX      XXX     ",
]

starting_dots = []
for y, row in enumerate(grid):
    s = set()
    for x, char in enumerate(row):
        if char == 'X' or char == 'O':
            s.add(x)
    starting_dots.append(s)

def get_scanner(start_x):
    return {x + y*1j for x in range(start_x, start_x+4) for y in (4,5)}

scanner_xs = [3, 5, 7, 9, 11, 13, 15, 13, 11, 9, 7, 5]
curr_scanner = get_scanner(3)
transitions_code = []

for i in range(len(scanner_xs)):
    next_x = scanner_xs[(i+1) % len(scanner_xs)]
    next_scanner = get_scanner(next_x)
    
    mouth_toggle = {x + 8*1j for x in [6,8,10,12,14]}
    
    remove = curr_scanner - next_scanner
    add = next_scanner - curr_scanner
    
    if i % 2 == 0:
        add |= mouth_toggle
    else:
        remove |= mouth_toggle
        
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
