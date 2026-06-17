"""Pure functions that turn numbers into strings. No dependencies."""
from __future__ import annotations
from typing import Iterable, List, Optional, Sequence

_SPARK = "▁▂▃▄▅▆▇█"
_BLOCKS = " ▏▎▍▌▋▊▉█"      # 1/8th-width blocks for smooth horizontal bars
_VBLOCKS = " ▁▂▃▄▅▆▇█"     # 1/8th-height blocks for smooth vertical columns
_HEAT = " ░▒▓█"


def _minmax(values: Sequence[float]) -> tuple[float, float]:
    lo, hi = min(values), max(values)
    return lo, hi


def sparkline(values: Sequence[float], lo: Optional[float] = None, hi: Optional[float] = None) -> str:
    """Compact inline trend, e.g. ▁▃▅█▆▃▁

    Pass `lo`/`hi` to pin the scale (values are clamped into it) so several
    sparklines can be compared on the same axis; otherwise it auto-scales.
    """
    values = list(values)
    if not values:
        return ""
    if lo is None:
        lo = min(values)
    if hi is None:
        hi = max(values)
    span = hi - lo
    out = []
    for v in values:
        if span == 0:
            idx = 0
        else:
            frac = max(0.0, min(1.0, (v - lo) / span))
            idx = round(frac * (len(_SPARK) - 1))
        out.append(_SPARK[idx])
    return "".join(out)


def hbar(value: float, max_value: float, width: int = 20) -> str:
    """A single smooth horizontal bar using 1/8th block resolution."""
    if max_value <= 0:
        return " " * width
    frac = max(0.0, min(1.0, value / max_value))
    full_eighths = round(frac * width * 8)
    full = full_eighths // 8
    rem = full_eighths % 8
    bar = "█" * full
    if rem:
        bar += _BLOCKS[rem]
    return bar.ljust(width)


def bars(data, width: int = 20, *, label_width: int | None = None) -> str:
    """Labeled horizontal bar chart from a dict or list of (label, value)."""
    items = list(data.items()) if isinstance(data, dict) else list(data)
    if not items:
        return ""
    max_v = max(v for _, v in items)
    lw = label_width or max(len(str(k)) for k, _ in items)
    lines = []
    for label, value in items:
        lines.append(f"{str(label).rjust(lw)} │{hbar(value, max_v, width)} {value:g}")
    return "\n".join(lines)


def histogram(values: Sequence[float], bins: int = 10, width: int = 20) -> str:
    values = list(values)
    if not values:
        return ""
    lo, hi = _minmax(values)
    span = (hi - lo) or 1.0
    counts = [0] * bins
    for v in values:
        idx = min(bins - 1, int((v - lo) / span * bins))
        counts[idx] += 1
    rows = []
    for i, c in enumerate(counts):
        edge = lo + span * i / bins
        rows.append(f"{edge:8.2f} │{hbar(c, max(counts), width)} {c}")
    return "\n".join(rows)


def columns(values: Sequence[float], height: int = 8) -> str:
    """A vertical bar chart `height` rows tall, using 1/8th-height blocks.

    Bars are scaled to the max value; one character per value, top row first.
    """
    values = list(values)
    if not values or height < 1:
        return ""
    hi = max(values)
    if hi <= 0:
        return "\n".join(" " * len(values) for _ in range(height))
    eighths = [round(max(0.0, min(1.0, v / hi)) * height * 8) for v in values]
    rows = []
    for r in range(height):
        level = height - 1 - r          # full-block rows remaining below this one
        line = []
        for e in eighths:
            full, rem = divmod(e, 8)
            if full > level:
                line.append("█")
            elif full == level and rem:
                line.append(_VBLOCKS[rem])
            else:
                line.append(" ")
        rows.append("".join(line))
    return "\n".join(rows)


def heatmap(grid: Sequence[Sequence[float]]) -> str:
    """Render a 2D matrix as shaded blocks (each cell = 2 chars wide)."""
    flat = [v for row in grid for v in row]
    if not flat:
        return ""
    lo, hi = _minmax(flat)
    span = (hi - lo) or 1.0
    lines = []
    for row in grid:
        cells = []
        for v in row:
            idx = round((v - lo) / span * (len(_HEAT) - 1))
            cells.append(_HEAT[idx] * 2)
        lines.append("".join(cells))
    return "\n".join(lines)
