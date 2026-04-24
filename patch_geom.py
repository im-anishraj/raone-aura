import re

with open("aura/cli/textual_ui/widgets/banner/petit_chat.py", "r", encoding="utf-8") as f:
    content = f.read()

pattern = r"STARTING_DOTS = \[.*?\]"
replacement = """STARTING_DOTS = [
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
]"""
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("aura/cli/textual_ui/widgets/banner/petit_chat.py", "w", encoding="utf-8") as f:
    f.write(new_content)
