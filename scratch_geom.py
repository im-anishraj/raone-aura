from aura.cli.textual_ui.widgets.braille_renderer import render_braille

grid = [
  "        XXXXXX        ",
  "      XX      XX      ",
  "     X    XX    X     ",
  "    X    X  X    X    ",
  "    X   XXXXXX   X    ",
  "    X    X  X    X    ",
  "    X     XX     X    ",
  "    X  X      X  X    ",
  "     X   X  X   X     ",
  "      XX  XX  XX      ",
  "       X      X       ",
  "      X        X      ",
]

dots = set()
starting_dots = []

for y, row in enumerate(grid):
    s = set()
    for x, char in enumerate(row):
        if char == 'X':
            dots.add(x + y * 1j)
            s.add(x)
    starting_dots.append(s)

print("BRAILLE:")
print(render_braille(dots, 22, 12))
print("\nSTARTING_DOTS = [")
for s in starting_dots:
    if len(s) == 0:
        print("    set[int](),")
    else:
        print(f"    {s},")
print("]")
