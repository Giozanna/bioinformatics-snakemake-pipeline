import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from compute_stats import compute_stats


def test_compute_stats_length_and_gc(tmp_path):
    input_fasta = tmp_path / "input.fasta"
    input_fasta.write_text(">all_gc\nGCGC\n>no_gc\nATAT\n")

    df = compute_stats(str(input_fasta))

    assert list(df["sample"]) == ["all_gc", "no_gc"]
    assert list(df["length"]) == [4, 4]

    gc_values = dict(zip(df["sample"], df["gc_percent"]))
    assert gc_values["all_gc"] == 100.0
    assert gc_values["no_gc"] == 0.0