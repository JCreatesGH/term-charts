"""Command-line interface: render numbers (from args or stdin) as a chart."""
from __future__ import annotations
import argparse
import sys
from typing import List, Optional

from .charts import sparkline, bars, columns, histogram, heatmap, line, scatter, plot

_CHARTS = ["spark", "line", "scatter", "plot", "bars", "columns", "hist", "heatmap"]


def _read_stdin() -> str:
    try:
        if sys.stdin.isatty():
            return ""
        return sys.stdin.read()
    except Exception:                       # noqa: BLE001 — pytest stdin, closed pipe, etc.
        return ""


def _numbers(tokens: List[str]) -> List[float]:
    out: List[float] = []
    for tok in tokens:
        for part in tok.replace(",", " ").split():
            out.append(float(part))
    return out


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="termcharts", description="Render numbers as a terminal chart.")
    p.add_argument("chart", choices=_CHARTS, help="chart type")
    p.add_argument("data", nargs="*",
                   help="numbers (or label=value for bars); rows for heatmap; reads stdin if omitted")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=8)
    p.add_argument("--bins", type=int, default=10)
    args = p.parse_args(argv)

    try:
        if args.chart == "heatmap":
            src = "\n".join(args.data) if args.data else _read_stdin()
            grid = [[float(x) for x in ln.replace(",", " ").split()]
                    for ln in src.splitlines() if ln.strip()]
            if not grid:
                print("termcharts: no numeric data", file=sys.stderr)
                return 2
            out = heatmap(grid)
        elif args.chart == "bars":
            tokens = args.data or _read_stdin().split()
            items = []
            for i, tok in enumerate(tokens):
                if "=" in tok:
                    k, v = tok.split("=", 1)
                    items.append((k, float(v)))
                else:
                    items.append((str(i + 1), float(tok)))
            if not items:
                print("termcharts: no numeric data", file=sys.stderr)
                return 2
            out = bars(items, width=args.width or 20)
        else:
            values = _numbers(args.data or _read_stdin().split())
            if not values:
                print("termcharts: no numeric data", file=sys.stderr)
                return 2
            if args.chart == "spark":
                out = sparkline(values)
            elif args.chart == "line":
                out = line(values, width=args.width or 40, height=args.height)
            elif args.chart == "scatter":
                out = scatter(values, width=args.width or 40, height=args.height)
            elif args.chart == "plot":
                out = plot(values, width=args.width or 40, height=args.height,
                           kind="line", xrange=(0, len(values) - 1))
            elif args.chart == "columns":
                out = columns(values, height=args.height)
            else:  # hist
                out = histogram(values, bins=args.bins, width=args.width or 20)
    except ValueError as e:
        print(f"termcharts: invalid number ({e})", file=sys.stderr)
        return 2

    print(out)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
