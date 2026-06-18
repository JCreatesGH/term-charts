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


# Braille dot bit per (row_in_cell, col_in_cell); a cell is 2 dots wide × 4 tall.
_BRAILLE_DOTS = {
    (0, 0): 0x01, (1, 0): 0x02, (2, 0): 0x04, (3, 0): 0x40,
    (0, 1): 0x08, (1, 1): 0x10, (2, 1): 0x20, (3, 1): 0x80,
}


def _fmt(v: float) -> str:
    """Compact numeric label: ints without a decimal, floats trimmed (8, 0, 5.333)."""
    return f"{v:.4g}"


def _resolve_lohi(values: Sequence[float], lo: Optional[float], hi: Optional[float]) -> tuple[float, float]:
    if lo is None:
        lo = min(values)
    if hi is None:
        hi = max(values)
    return lo, hi


def _braille_rows(values: Sequence[float], width: int, height: int,
                  lo: float, hi: float, connect: bool) -> List[str]:
    """Plot `values` (y) over their index (x) into braille cells (2×4 dots each).

    `connect=True` joins consecutive samples (a line); `connect=False` inks only
    the sample points (a scatter). Returns `height` strings of `width` chars."""
    span = hi - lo
    cols, rows = width * 2, height * 4
    grid = [[0] * width for _ in range(height)]

    def dot(x: int, y: int) -> None:
        if 0 <= x < cols and 0 <= y < rows:
            grid[y // 4][x // 2] |= _BRAILLE_DOTS[(y % 4, x % 2)]

    def to_y(v: float) -> int:
        frac = 0.5 if span == 0 else max(0.0, min(1.0, (v - lo) / span))
        return int(round((1 - frac) * (rows - 1)))   # invert: high value = top row

    n = len(values)
    pts = [(int(round(i / (n - 1) * (cols - 1))) if n > 1 else 0, to_y(v))
           for i, v in enumerate(values)]
    if not connect or n == 1:
        for x, y in pts:
            dot(x, y)
    else:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            steps = max(abs(x1 - x0), abs(y1 - y0))
            if steps == 0:
                dot(x0, y0)
                continue
            for s in range(steps + 1):
                t = s / steps
                dot(int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t)))
    return ["".join(chr(0x2800 + c) for c in row) for row in grid]


def line(values: Sequence[float], width: int = 40, height: int = 8,
         lo: Optional[float] = None, hi: Optional[float] = None) -> str:
    """A high-resolution line plot drawn with braille dots (2×4 per character),
    so a `width`×`height` chart actually resolves `2·width` × `4·height` points.
    Consecutive samples are connected. Pin `lo`/`hi` to fix the y-axis."""
    values = list(values)
    if not values or width < 1 or height < 1:
        return ""
    lo, hi = _resolve_lohi(values, lo, hi)
    return "\n".join(_braille_rows(values, width, height, lo, hi, connect=True))


def scatter(values: Sequence[float], width: int = 40, height: int = 8,
            lo: Optional[float] = None, hi: Optional[float] = None) -> str:
    """Like :func:`line`, but inks only the sample points (no connecting segments)
    — useful for sparse or noisy data where the joins would mislead."""
    values = list(values)
    if not values or width < 1 or height < 1:
        return ""
    lo, hi = _resolve_lohi(values, lo, hi)
    return "\n".join(_braille_rows(values, width, height, lo, hi, connect=False))


def plot(values: Sequence[float], width: int = 40, height: int = 8,
         lo: Optional[float] = None, hi: Optional[float] = None, *,
         kind: str = "line", xrange: Optional[tuple] = None) -> str:
    """A framed braille chart with a labeled y-axis and a baseline border, so the
    values are actually readable. `kind` is "line" (connected) or "scatter" (points).
    Pass `xrange=(x0, x1)` to label the x-axis endpoints.

        8 ┤      ⢀⠤⠒⠉⠑⠢⢄
          │   ⢀⠔⠁
        0 ┤⠤⠊⠁
          └────────────────
    """
    values = list(values)
    if not values or width < 1 or height < 1:
        return ""
    lo, hi = _resolve_lohi(values, lo, hi)
    body = _braille_rows(values, width, height, lo, hi, connect=(kind != "scatter"))
    span = hi - lo

    # y-axis labels for the top, middle, and bottom rows.
    labels = {0: _fmt(hi), height - 1: _fmt(lo)}
    if height >= 3:
        mid = (height - 1) // 2
        labels[mid] = _fmt(hi - (mid / (height - 1)) * span)
    gutter = max(len(s) for s in labels.values())

    out = []
    for r, row in enumerate(body):
        if r in labels:
            out.append(f"{labels[r].rjust(gutter)} ┤{row}")
        else:
            out.append(f"{' ' * gutter} │{row}")
    out.append(f"{' ' * gutter} └{'─' * width}")
    if xrange is not None:
        left, right = _fmt(xrange[0]), _fmt(xrange[1])
        axis = (left + right.rjust(width - len(left))) if len(left) + len(right) <= width else left
        out.append(f"{' ' * gutter}  {axis}")
    return "\n".join(out)


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
