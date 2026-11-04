# ASCII Art Generator

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

# Save the result to a file
python ascii_art.py "HELLO" --border stars -o hello.txt
```

### Options

| Option | Description | Default |
|---|---|---|
| `TEXT` | Text to render (omit when using `--pattern`) | — |
| `--style` | Letter style for the built-in font: `block`, `hash`, `shadow`, `gradient`, `text` | `block` |
| `--scale N` | Scale factor for the built-in font (must be ≥ 1) | `1` |
| `--font NAME` | Use a pyfiglet font instead of the built-in one (e.g. `standard`, `slant`, `big`) | — |
| `--background` | Surround the text with a pattern (see list below) | — |
| `--border` | Draw a frame: `single`, `double`, `rounded`, `ascii`, `stars` | — |
| `--pattern` | Only generate a pattern, no text | — |
| `--chars` | Custom characters for the pattern/background | pattern-specific |
| `--width N` | Pattern width (with `--pattern`) | `60` |
| `--height N` | Pattern height (with `--pattern`) | `10` |
| `--seed N` | Seed for the `random` pattern | — |
| `-o`, `--output FILE` | Write the result to a file instead of stdout | — |

### Styles

- `block` – solid `█` blocks
- `hash` – `#` characters
- `shadow` – solid blocks with a `░` drop shadow
- `gradient` – vertical shading using `█▓▒░`
- `text` – fills the letters with the characters of the input text

### Patterns

`checkerboard`, `gradient`, `random`, `waves`, `diamonds`, `bricks`, `stripes`, `zigzag`

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
