#!/usr/bin/env python3
"""ASCII art generator: turn text into banners and decorate them with patterns.

Examples:
    python ascii_art.py "ASCII PATTERNS"
    python ascii_art.py "HELLO" --style shadow --background diamonds
    python ascii_art.py "HI" --style gradient --scale 2 --border double
    python ascii_art.py "ASCII Patterns" --font standard   # needs `pip install pyfiglet`
    python ascii_art.py --pattern waves --width 60 --height 8
"""

from __future__ import annotations

import argparse
import math
import random
import sys

# 5-row bitmap font. '#' marks a filled pixel.
FONT: dict[str, list[str]] = {
    "A": [" ### ", "#   #", "#####", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#### ", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#### ", "#    ", "#####"],
    "F": ["#####", "#    ", "#### ", "#    ", "#    "],
    "G": [" ####", "#    ", "#  ##", "#   #", " ####"],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "I": ["###", " # ", " # ", " # ", "###"],
    "J": ["  ###", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    "S": [" ####", "#    ", " ### ", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "# # #", "## ##", "#   #"],
    "X": ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "   # ", "  #  ", " #   ", "#####"],
    "0": [" ### ", "#  ##", "# # #", "##  #", " ### "],
    "1": [" # ", "## ", " # ", " # ", "###"],
    "2": [" ### ", "#   #", "  ## ", " #   ", "#####"],
    "3": ["#### ", "    #", " ### ", "    #", "#### "],
    "4": ["#   #", "#   #", "#####", "    #", "    #"],
    "5": ["#####", "#    ", "#### ", "    #", "#### "],
    "6": [" ### ", "#    ", "#### ", "#   #", " ### "],
    "7": ["#####", "   # ", "  #  ", " #   ", "#    "],
    "8": [" ### ", "#   #", " ### ", "#   #", " ### "],
    "9": [" ### ", "#   #", " ####", "    #", " ### "],
    " ": ["   ", "   ", "   ", "   ", "   "],
    "!": ["#", "#", "#", " ", "#"],
    "?": [" ### ", "#   #", "  ## ", "     ", "  #  "],
    ".": [" ", " ", " ", " ", "#"],
    ",": ["  ", "  ", "  ", " #", "# "],
    ":": [" ", "#", " ", "#", " "],
    ";": ["  ", " #", "  ", " #", "# "],
    "-": ["    ", "    ", "####", "    ", "    "],
    "+": ["   ", " # ", "###", " # ", "   "],
    "=": ["    ", "####", "    ", "####", "    "],
    "_": ["    ", "    ", "    ", "    ", "####"],
    "'": ["#", "#", " ", " ", " "],
    '"': ["# #", "# #", "   ", "   ", "   "],
    "/": ["    #", "   # ", "  #  ", " #   ", "#    "],
    "(": [" #", "# ", "# ", "# ", " #"],
    ")": ["# ", " #", " #", " #", "# "],
    "*": ["     ", " # # ", "  #  ", " # # ", "     "],
    "#": [" # # ", "#####", " # # ", "#####", " # # "],
    "&": [" ##  ", "#  # ", " ## #", "#  # ", " ## #"],
    "@": [" ### ", "# ###", "# # #", "# ###", " ### "],
}

STYLES = ("block", "hash", "shadow", "gradient", "text")
PATTERNS = ("checkerboard", "gradient", "random", "waves", "diamonds", "bricks", "stripes", "zigzag")
BORDERS = {
    "single": "┌┐└┘─│",
    "double": "╔╗╚╝═║",
    "rounded": "╭╮╰╯─│",
    "ascii": "++++-|",
    "stars": "******",
}

Grid = list[list[str]]


def render_bitmap(text: str, scale: int = 1, spacing: int = 1) -> list[str]:
    """Render text into rows of '#'/' ' using the built-in font."""
    rows = [""] * 5
    unknown = FONT["?"]
    for i, ch in enumerate(text.upper()):
        glyph = FONT.get(ch, unknown)
        gap = " " * spacing if i < len(text) - 1 else ""
        for r in range(5):
            rows[r] += glyph[r] + gap
    scaled = []
    for row in rows:
        wide = "".join(c * scale for c in row)
        scaled.extend([wide] * scale)
    return scaled


def _to_grid(lines: list[str], pad_right: int = 0, pad_bottom: int = 0) -> Grid:
    width = max((len(line) for line in lines), default=0) + pad_right
    grid = [list(line.ljust(width)) for line in lines]
    grid += [[" "] * width for _ in range(pad_bottom)]
    return grid


def stylize(bitmap: list[str], style: str = "block", text: str = "") -> Grid:
    """Convert a '#' bitmap into a styled character grid."""
    if style == "shadow":
        grid = _to_grid(bitmap, pad_right=1, pad_bottom=1)
        for r, row in enumerate(bitmap):
            for c, ch in enumerate(row):
                if ch == "#" and grid[r + 1][c + 1] == " ":
                    grid[r + 1][c + 1] = "░"
        for r, row in enumerate(bitmap):
            for c, ch in enumerate(row):
                if ch == "#":
                    grid[r][c] = "█"
        return grid

    grid = _to_grid(bitmap)
    letters = [c for c in text if not c.isspace()] or ["#"]
    ramp = "█▓▒░"
    height = len(bitmap)
    k = 0
    for r, row in enumerate(bitmap):
        for c, ch in enumerate(row):
            if ch != "#":
                continue
            if style == "hash":
                grid[r][c] = "#"
            elif style == "gradient":
                grid[r][c] = ramp[min(len(ramp) - 1, r * len(ramp) // max(height, 1))]
            elif style == "text":
                grid[r][c] = letters[k % len(letters)]
                k += 1
            else:
                grid[r][c] = "█"
    return grid


def render_figlet(text: str, font: str) -> Grid:
    """Render with pyfiglet (e.g. the 'standard' font used by asciiart.eu)."""
    try:
        import pyfiglet
    except ImportError as exc:
        raise SystemExit("The --font option requires pyfiglet: pip install pyfiglet") from exc
    lines = pyfiglet.figlet_format(text, font=font, width=10_000).rstrip("\n").split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    return _to_grid(lines)


def pattern(name: str, width: int, height: int, chars: str | None = None, seed: int | None = None) -> Grid:
    """Generate a background pattern grid."""
    rng = random.Random(seed)
    defaults = {
        "checkerboard": "█ ",
        "gradient": " .:-=+*#%@",
        "random": " .:░▒",
        "waves": "~-",
        "diamonds": "/\\",
        "bricks": "_|",
        "stripes": "/ ",
        "zigzag": "/\\",
    }
    if name not in defaults:
        raise ValueError(f"Unknown pattern {name!r}. Choose from: {', '.join(PATTERNS)}")
    ch = chars or defaults[name]
    grid: Grid = []
    for y in range(height):
        row = []
        for x in range(width):
            if name == "checkerboard":
                c = ch[((x // 2) + y) % len(ch)]
            elif name == "gradient":
                c = ch[min(len(ch) - 1, x * len(ch) // max(width, 1))]
            elif name == "random":
                c = rng.choice(ch)
            elif name == "waves":
                wave = math.sin((x + y * 3) / 3.0)
                c = ch[0] if wave > 0.3 else (ch[1 % len(ch)] if wave > -0.3 else " ")
            elif name == "diamonds":
                m = (x + y) % 4
                n = (x - y) % 4
                c = ch[0] if m == 0 else (ch[1 % len(ch)] if n == 0 else " ")
            elif name == "bricks":
                offset = 0 if (y // 2) % 2 == 0 else 3
                if y % 2 == 1:
                    c = ch[0]
                else:
                    c = ch[1 % len(ch)] if (x + offset) % 6 == 0 else " "
            elif name == "stripes":
                c = ch[((x + y) // 2) % len(ch)]
            else:  # zigzag
                c = ch[0] if (x + y) % 4 == 0 and (x // 4) % 2 == 0 else (
                    ch[1 % len(ch)] if (x - y) % 4 == 0 and (x // 4) % 2 == 1 else " ")
            row.append(c)
        grid.append(row)
    return grid


def place_on_background(art: Grid, bg_name: str, margin: int = 3, padding: int = 1,
                        chars: str | None = None, seed: int | None = None) -> Grid:
    """Center the art inside a patterned background with a clear area around it."""
    ah, aw = len(art), len(art[0]) if art else 0
    height = ah + 2 * (margin + padding)
    width = aw + 2 * (margin * 2 + padding * 2)
    bg = pattern(bg_name, width, height, chars, seed)
    top = margin + padding
    left = (width - aw) // 2
    for r in range(top - padding, top + ah + padding):
        for c in range(left - padding * 2, left + aw + padding * 2):
            bg[r][c] = " "
    for r in range(ah):
        for c in range(aw):
            if art[r][c] != " ":
                bg[top + r][left + c] = art[r][c]
    return bg


def add_border(art: Grid, kind: str = "single", padding: int = 1) -> Grid:
    tl, tr, bl, br, hz, vt = BORDERS[kind]
    width = len(art[0]) if art else 0
    inner = [[" "] * (width + 2 * padding) for _ in range(padding)]
    body = inner + [[" "] * padding + row + [" "] * padding for row in art] + [r[:] for r in inner]
    full = width + 2 * padding
    return [[tl] + [hz] * full + [tr]] + [[vt] + row + [vt] for row in body] + [[bl] + [hz] * full + [br]]


def to_text(grid: Grid) -> str:
    return "\n".join("".join(row).rstrip() for row in grid)


def generate(text: str, style: str = "block", scale: int = 1, font: str | None = None,
             background: str | None = None, border: str | None = None,
             bg_chars: str | None = None, seed: int | None = None) -> str:
    """High-level helper: text -> finished ASCII art string."""
    if font:
        art = render_figlet(text, font)
    else:
        art = stylize(render_bitmap(text, scale=scale), style, text)
    if background:
        art = place_on_background(art, background, chars=bg_chars, seed=seed)
    if border:
        art = add_border(art, border)
    return to_text(art)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate ASCII art banners and patterns.")
    parser.add_argument("text", nargs="?", help="Text to render (omit with --pattern)")
    parser.add_argument("--style", choices=STYLES, default="block", help="Letter style (built-in font)")
    parser.add_argument("--scale", type=int, default=1, help="Scale factor for the built-in font")
    parser.add_argument("--font", help="Use a pyfiglet font instead, e.g. standard, slant, big")
    parser.add_argument("--background", choices=PATTERNS, help="Surround the text with a pattern")
    parser.add_argument("--border", choices=list(BORDERS), help="Draw a frame around the result")
    parser.add_argument("--pattern", choices=PATTERNS, help="Only generate a pattern (no text)")
    parser.add_argument("--chars", help="Custom characters for the pattern/background")
    parser.add_argument("--width", type=int, default=60, help="Pattern width (with --pattern)")
    parser.add_argument("--height", type=int, default=10, help="Pattern height (with --pattern)")
    parser.add_argument("--seed", type=int, help="Seed for the random pattern")
    parser.add_argument("-o", "--output", help="Write the result to a file")
    args = parser.parse_args(argv)

    if args.scale < 1:
        parser.error("--scale must be >= 1")
    if args.pattern:
        result = to_text(pattern(args.pattern, args.width, args.height, args.chars, args.seed))
        if args.border:
            result = to_text(add_border([list(line.ljust(args.width)) for line in result.split("\n")],
                                        args.border, padding=0))
    elif args.text:
        result = generate(args.text, args.style, args.scale, args.font, args.background,
                          args.border, args.chars, args.seed)
    else:
        parser.error("provide TEXT or --pattern")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(result + "\n")
    else:
        sys.stdout.write(result + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
