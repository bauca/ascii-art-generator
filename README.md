# ASCII Art Generator

```text

 ███   ████  ████ ███ ███      ███  ████  █████      ████ █████ █   █ █████ ████   ███  █████  ███  ████
█   █ █     █      █   █      █   █ █   █   █       █     █     ██  █ █     █   █ █   █   █   █   █ █   █
▓▓▓▓▓  ▓▓▓  ▓      ▓   ▓      ▓▓▓▓▓ ▓▓▓▓    ▓       ▓  ▓▓ ▓▓▓▓  ▓ ▓ ▓ ▓▓▓▓  ▓▓▓▓  ▓▓▓▓▓   ▓   ▓   ▓ ▓▓▓▓
▒   ▒     ▒ ▒      ▒   ▒      ▒   ▒ ▒  ▒    ▒       ▒   ▒ ▒     ▒  ▒▒ ▒     ▒  ▒  ▒   ▒   ▒   ▒   ▒ ▒  ▒
░   ░ ░░░░   ░░░░ ░░░ ░░░     ░   ░ ░   ░   ░        ░░░░ ░░░░░ ░   ░ ░░░░░ ░   ░ ░   ░   ░    ░░░  ░   ░

```
A small, dependency-free Python script that turns text into ASCII art banners and decorates them with background patterns and borders.

```text
╭────────────╮
│            │
│ █   █ ███  │
│ █░  █░ █░░ │
│ █████░ █░  │
│ █░░░█░ █░  │
│ █░  █░███  │
│  ░   ░ ░░░ │
│            │
╰────────────╯
```

## Requirements

- Python 3.9+
- Optional: [pyfiglet](https://pypi.org/project/pyfiglet/) to use FIGlet fonts with `--font`

```bash
pip install pyfiglet  # only needed for --font
```

## Usage

```bash
python ascii_art.py [TEXT] [options]
```

Either `TEXT` or `--pattern` must be provided.

### Examples

```bash
# Basic banner with the built-in font
python ascii_art.py "ASCII PATTERNS"

# Shadowed letters on a diamond background
python ascii_art.py "HELLO" --style shadow --background diamonds

# Gradient letters, doubled in size, with a double-line frame
python ascii_art.py "HI" --style gradient --scale 2 --border double

# Use a FIGlet font (requires pyfiglet)
python ascii_art.py "ASCII Patterns" --font standard

# Generate only a pattern
python ascii_art.py --pattern waves --width 60 --height 8

# Reproducible random pattern with custom characters
python ascii_art.py --pattern random --chars " .*" --seed 42

# Compact half-height letters on a starfield
python ascii_art.py "COMPACT" --style half --background stars --seed 7

# Draw letters with a custom character
python ascii_art.py "LED" --style block --fill "*"

# Save the result to a file
python ascii_art.py "HELLO" --border stars -o hello.txt
```

### Options

| Option | Description | Default |
|---|---|---|
| `TEXT` | Text to render (omit when using `--pattern`) | — |
| `--style` | Letter style for the built-in font (see list below) | `block` |
| `--scale N` | Scale factor for the built-in font (must be ≥ 1) | `1` |
| `--fill CHAR` | Single character used to draw the letters (`block`, `hash`, `shadow`, `inverse`, `3d`, `dots` styles; not with `--font`) | style-specific |
| `--font NAME` | Use a pyfiglet font instead of the built-in one (e.g. `standard`, `slant`, `big`) | — |
| `--background` | Surround the text with a pattern (see list below) | — |
| `--border` | Draw a frame: `single`, `double`, `rounded`, `ascii`, `stars` | — |
| `--pattern` | Only generate a pattern, no text | — |
| `--chars` | Custom characters for the pattern/background | pattern-specific |
| `--width N` | Pattern width (with `--pattern`) | `60` |
| `--height N` | Pattern height (with `--pattern`) | `10` |
| `--seed N` | Seed for the `random`, `maze` and `stars` patterns | — |
| `-o`, `--output FILE` | Write the result to a file instead of stdout | — |

### Styles

- `block` – solid `█` blocks
- `hash` – `#` characters
- `shadow` – solid blocks with a `░` drop shadow
- `gradient` – vertical shading using `█▓▒░`
- `text` – fills the letters with the characters of the input text
- `half` – packs two pixel rows into one using `▀▄█`, for banners half as tall
- `inverse` – letters cut out of a solid block
- `3d` – solid blocks with a thick `▒` extrusion
- `dots` – LED-style `●` dots

```text
█   █ ▀█▀     █   █ ▄▀▀▀▄
█▀▀▀█  █      ▀▀▀▀█  ▄▀▀
▀   ▀ ▀▀▀         ▀ ▀▀▀▀▀
```

### Patterns

| Pattern | Default chars | Pattern | Default chars |
|---|---|---|---|
| `checkerboard` | `█ ` | `maze` | `/\` (random, seedable) |
| `gradient` | ` .:-=+*#%@` | `grid` | `+-\|` |
| `random` | ` .:░▒` (seedable) | `dots` | `o` |
| `waves` | `~-` | `crosshatch` | `X/\` |
| `diamonds` | `/\` | `scales` | `(_)` |
| `bricks` | `_\|` | `hexagons` | `/\_` |
| `stripes` | `/ ` | `ripples` | ` .oO` |
| `zigzag` | `/\` | `stars` | `*.+` (random, seedable) |

Override the defaults with `--chars`, e.g. `--pattern grid --chars "#=:"`.

Example (`--pattern hexagons --width 30 --height 4`):

```text
/ \__/ \__/ \__/ \__/ \__/ \__
\__/ \__/ \__/ \__/ \__/ \__/
/ \__/ \__/ \__/ \__/ \__/ \__
\__/ \__/ \__/ \__/ \__/ \__/
```

Example (`--pattern waves --width 40 --height 4`):

```text
-~~~~~~~~--       --~~~~~~~~--       --~
~~~~~~--       --~~~~~~~~--       --~~~~
~~~--       --~~~~~~~~--       --~~~~~~~
--       --~~~~~~~~--       --~~~~~~~~--
```

### Supported characters

The built-in font supports `A–Z` (case-insensitive), `0–9`, space, and `! ? . , : ; - + = _ ' " / ( ) * # & @`. Unsupported characters are rendered as `?`.

## Using as a module

```python
from ascii_art import generate, pattern, to_text

print(generate("HELLO", style="shadow", border="rounded"))
print(to_text(pattern("checkerboard", 20, 5)))
```

## License

[MIT](LICENSE)
