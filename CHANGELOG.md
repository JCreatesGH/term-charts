# Changelog

All notable changes are documented here, following
[Keep a Changelog](https://keepachangelog.com/) and [SemVer](https://semver.org/).

## [0.3.0]

### Added
- `plot()` — a **framed** braille chart with a labeled y-axis (top/middle/bottom values) and
  a baseline border, plus optional `xrange=(x0, x1)` axis labels, so the values are actually
  readable instead of a floating squiggle. `kind="line"` (default) or `kind="scatter"`.
- `scatter()` — inks only the sample points (no connecting segments), for sparse/noisy data.
- CLI gains `plot` and `scatter` chart types.

### Changed
- Refactored the braille rasterizer into a shared helper behind `line`/`scatter`/`plot`
  (identical `line()` output).

## [0.2.0]

### Added
- `line()` — a high-resolution braille line plot (2×4 dots per character, so a
  `width`×`height` chart resolves `2·width`×`4·height` points; samples are
  connected).
- A `termcharts` CLI (`spark | line | bars | columns | hist | heatmap`) reading
  numbers from arguments or stdin.

## [0.1.0]

### Added
- Zero-dependency Unicode charts: `sparkline`, `bars`, `hbar`, `columns`,
  `histogram`, and `heatmap`, all returning plain strings.
