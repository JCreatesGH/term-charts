# Changelog

All notable changes are documented here, following
[Keep a Changelog](https://keepachangelog.com/) and [SemVer](https://semver.org/).

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
