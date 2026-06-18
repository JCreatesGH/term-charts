import subprocess, sys, os
from pathlib import Path
from termcharts.cli import main

SRC = str(Path(__file__).resolve().parents[1] / "src")


def test_cli_spark(capsys):
    assert main(["spark", "1", "2", "3", "4"]) == 0
    out = capsys.readouterr().out.strip()
    assert out[0] == "▁" and out[-1] == "█"


def test_cli_line_shape(capsys):
    assert main(["line", "0", "1", "2", "3", "--width", "10", "--height", "3"]) == 0
    rows = capsys.readouterr().out.splitlines()
    assert len(rows) == 3 and all(len(r) == 10 for r in rows)


def test_cli_bars_labels_and_positional(capsys):
    assert main(["bars", "py=8", "ts=4"]) == 0
    out = capsys.readouterr().out
    assert "py" in out and "ts" in out


def test_cli_hist_and_columns(capsys):
    assert main(["hist", "1", "1", "2", "9", "--bins", "2"]) == 0
    assert main(["columns", "3", "1", "4", "1", "5", "--height", "3"]) == 0


def test_cli_heatmap_rows_from_args(capsys):
    assert main(["heatmap", "0 1", "2 3"]) == 0
    rows = capsys.readouterr().out.splitlines()
    assert len(rows) == 2 and len(rows[0]) == 4


def test_cli_comma_separated_numbers(capsys):
    assert main(["spark", "1,2,3,4"]) == 0
    assert len(capsys.readouterr().out.strip()) == 4


def test_cli_rejects_non_numeric():
    assert main(["spark", "abc"]) == 2


def test_cli_reads_stdin():
    env = {**os.environ, "PYTHONPATH": SRC}
    r = subprocess.run([sys.executable, "-m", "termcharts.cli", "line", "--width", "8", "--height", "2"],
                       input="0 1 2 3 4 5", capture_output=True, text=True, env=env)
    assert r.returncode == 0
    assert len(r.stdout.splitlines()) == 2
