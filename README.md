# termcharts

[![CI](https://github.com/JCreatesGH/term-charts/actions/workflows/ci.yml/badge.svg)](https://github.com/JCreatesGH/term-charts/actions)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Tiny, **zero-dependency** Unicode charts for the terminal — sparklines, bar charts, histograms, and heatmaps as plain strings. Perfect for CLIs, dashboards, log output, and status scripts.

![screenshot](assets/screenshot.png)

## Install

```bash
pip install termcharts
```

## Use it

```python
from termcharts import sparkline, bars, histogram, heatmap

sparkline([3, 4, 6, 9, 7, 5, 8, 9, 6])      # "▁▂▅█▆▃▇█▅"

print(bars({"python": 128, "typescript": 92, "go": 41}, width=24))
#     python │████████████████████████ 128
# typescript │█████████████████▎       92
#         go │███████▊                 41

print(histogram(samples, bins=10))
print(heatmap([[0, 1, 2], [1, 3, 5], [2, 4, 8]]))
```

## Why it's nice

- **Smooth bars** — horizontal bars use 1/8th-width block characters, so a value of 4.6/10 renders crisper than whole-block charts.
- **Just strings** — every function returns a `str`, so you can log it, put it in a table, or embed it in a Slack message. No terminal control codes, no dependencies.
- **Auto-scaled** — sparklines and heatmaps normalize to their own min/max.

## API

`sparkline(values)` · `bars(dict_or_pairs, width=20)` · `hbar(value, max, width=20)` · `histogram(values, bins=10)` · `heatmap(2d_grid)`

## Development

```bash
python -m pytest -q   # 6 tests
```

## License

MIT
