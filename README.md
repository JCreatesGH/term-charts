# termcharts

[![CI](https://github.com/JCreatesGH/term-charts/actions/workflows/ci.yml/badge.svg)](https://github.com/JCreatesGH/term-charts/actions)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Tiny, **zero-dependency** Unicode charts for the terminal — sparklines, bar charts, **braille line plots**, histograms, and heatmaps as plain strings. Perfect for CLIs, dashboards, log output, and status scripts.

![screenshot](assets/screenshot.png)

## Install

```bash
pip install termcharts
```

## Use it

```python
from termcharts import sparkline, bars, columns, histogram, heatmap, line

sparkline([3, 4, 6, 9, 7, 5, 8, 9, 6])      # "▁▂▅█▆▃▇█▅"
sparkline(week, lo=0, hi=100)               # pin the scale to compare sparklines

print(bars({"python": 128, "typescript": 92, "go": 41}, width=24))
#     python │████████████████████████ 128
# typescript │█████████████████▎       92
#         go │███████▊                 41

print(columns([2, 5, 8, 6, 9, 4], height=4))   # vertical bar chart, top row first

# A high-resolution line plot in braille — a width×height chart resolves
# (2·width)×(4·height) points, with samples connected:
print(line([0, 2, 4, 6, 7, 8, 7, 6, 4, 2, 0, -2, -4, -6, -8, -6, -4, -2, 0], width=24, height=5))
# ⢀⠤⠒⠉⠑⠢⢄⠀ …

print(histogram(samples, bins=10))
print(heatmap([[0, 1, 2], [1, 3, 5], [2, 4, 8]]))
```

## CLI

Installing the package adds a `termcharts` command — pipe numbers in, or pass them as arguments:

```bash
termcharts spark 3 4 6 9 7 5 8 9 6
echo "12 19 23 31 28 35" | termcharts line --width 40 --height 8
termcharts bars python=128 typescript=92 go=41 --width 24
termcharts hist 1 1 2 3 5 8 13 --bins 6
printf "0 1 2\n1 3 5\n2 4 8\n" | termcharts heatmap     # one row per line
```

Chart types: `spark · line · bars · columns · hist · heatmap`. Numbers may be space- or comma-separated; `bars` accepts `label=value` pairs. Exit code is `2` on non-numeric input.

## Why it's nice

- **Smooth bars** — horizontal `bars`/`hbar` use 1/8th-width blocks and vertical `columns` use 1/8th-height blocks, so fractional values render crisper than whole-block charts.
- **Braille line plots** — `line` packs 2×4 dots into every character cell, so even a small chart resolves a lot of points and the curve actually connects.
- **Just strings** — every function returns a `str`, so you can log it, put it in a table, or embed it in a Slack message. No terminal control codes, no dependencies.
- **Auto-scaled, or pinned** — sparklines/lines/heatmaps normalize to their own min/max, and the `lo`/`hi` arguments let you fix the axis to compare series.

## API

`sparkline(values, lo=None, hi=None)` · `bars(dict_or_pairs, width=20)` · `hbar(value, max, width=20)` · `columns(values, height=8)` · `line(values, width=40, height=8, lo=None, hi=None)` · `histogram(values, bins=10)` · `heatmap(2d_grid)`

## Development

```bash
pip install -e .[dev] && python -m pytest -q   # 19 tests
```

## License

MIT
