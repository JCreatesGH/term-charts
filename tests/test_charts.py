from termcharts import sparkline, bars, hbar, columns, histogram, heatmap, line, scatter, plot

_BLANK = "⠀"   # empty braille cell (not a regular space)


def test_line_shape():
    out = line([0, 1, 2, 3, 4, 5, 6, 7], width=10, height=4)
    rows = out.splitlines()
    assert len(rows) == 4
    assert all(len(r) == 10 for r in rows)
    assert all(ch == _BLANK or 0x2800 <= ord(ch) <= 0x28FF for r in rows for ch in r)


def test_line_rising_inks_low_left_and_high_right():
    out = line(range(40), width=12, height=4).splitlines()
    assert out[-1][0] != _BLANK     # rising line starts low-left
    assert out[0][-1] != _BLANK     # …and ends high-right


def test_line_empty_and_single():
    assert line([]) == ""
    assert len(line([5], width=4, height=2).splitlines()) == 2


def test_scatter_inks_fewer_dots_than_line():
    # a steep series: a connected line fills the climb; scatter inks only samples
    data = [0, 8, 0, 8, 0, 8]
    def ink(s):
        return sum(1 for ch in s.replace("\n", "") if ch != _BLANK)
    assert ink(scatter(data, width=12, height=4)) < ink(line(data, width=12, height=4))


def test_scatter_shape_and_empty():
    rows = scatter([0, 1, 2, 3], width=8, height=3).splitlines()
    assert len(rows) == 3 and all(len(r) == 8 for r in rows)
    assert scatter([]) == ""


def test_plot_frames_with_axis_and_labels():
    out = plot([0, 4, 8, 4, 0], width=12, height=4)
    rows = out.splitlines()
    # one row per chart row, plus a baseline border row
    assert len(rows) == 5
    assert "┤" in rows[0] and rows[0].lstrip().startswith("8")   # top label = hi
    assert "┤" in rows[-2] and "0" in rows[-2]                   # bottom label = lo
    assert rows[-1].strip().startswith("└")                     # baseline corner
    assert "─" in rows[-1]


def test_plot_xrange_adds_axis_labels():
    out = plot([1, 2, 3], width=20, height=3, xrange=(0, 100))
    last = out.splitlines()[-1]
    assert "0" in last and "100" in last


def test_plot_empty():
    assert plot([]) == ""


def test_sparkline_endpoints():
    s = sparkline([0, 1, 2, 3, 4, 5, 6, 7])
    assert s[0] == "▁" and s[-1] == "█" and len(s) == 8


def test_sparkline_flat_and_empty():
    assert sparkline([5, 5, 5]) == "▁▁▁"
    assert sparkline([]) == ""


def test_sparkline_fixed_scale_clamps():
    # With a pinned [0,10] scale, 5 is mid and out-of-range values clamp to the ends.
    s = sparkline([0, 5, 10, 20], lo=0, hi=10)
    assert s[0] == "▁" and s[2] == "█" and s[-1] == "█"
    assert len(s) == 4


def test_columns_shape_and_scaling():
    out = columns([0, 4, 8], height=4)
    rows = out.splitlines()
    assert len(rows) == 4
    assert all(len(r) == 3 for r in rows)        # one char per value
    assert rows[0][0] == " "                      # zero column is empty at the top
    assert rows[-1][-1] == "█"                    # max column is full at the bottom
    assert columns([], height=4) == ""


def test_hbar_fraction_and_bounds():
    assert hbar(10, 10, width=10).rstrip() == "█" * 10
    assert hbar(0, 10, width=10) == " " * 10
    half = hbar(5, 10, width=10)
    assert half.startswith("█████") and len(half) == 10
    # clamps over-max
    assert hbar(20, 10, width=4).rstrip() == "████"


def test_bars_from_dict_aligns_labels():
    out = bars({"py": 8, "ts": 4, "go": 2}, width=10)
    lines = out.splitlines()
    assert len(lines) == 3
    assert "py │" in lines[0] and lines[0].rstrip().endswith("8")
    # equal label width (right-justified)
    assert all("│" in ln for ln in lines)


def test_histogram_bins():
    out = histogram([1, 1, 1, 9, 9], bins=2, width=10)
    rows = out.splitlines()
    assert len(rows) == 2
    assert rows[0].rstrip().endswith("3")   # three values in low bin
    assert rows[1].rstrip().endswith("2")


def test_heatmap_shape():
    out = heatmap([[0, 1], [2, 3]])
    rows = out.splitlines()
    assert len(rows) == 2
    assert len(rows[0]) == 4   # 2 cells * 2 chars
    assert out.replace("\n", "")[0] == " "   # min value -> lightest
