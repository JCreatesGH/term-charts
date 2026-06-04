from termcharts import sparkline, bars, hbar, histogram, heatmap


def test_sparkline_endpoints():
    s = sparkline([0, 1, 2, 3, 4, 5, 6, 7])
    assert s[0] == "▁" and s[-1] == "█" and len(s) == 8


def test_sparkline_flat_and_empty():
    assert sparkline([5, 5, 5]) == "▁▁▁"
    assert sparkline([]) == ""


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
