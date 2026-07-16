import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from filter_sequences import filter_sequences


def test_filter_keeps_long_sequences(tmp_path):
    input_fasta = tmp_path / "input.fasta"
    input_fasta.write_text(">short\nATGC\n>long\nATGCATGCATGCATGCATGC\n")
    output_fasta = tmp_path / "output.fasta"

    n_kept = filter_sequences(str(input_fasta), str(output_fasta), min_length=10)

    assert n_kept == 1
    output_content = output_fasta.read_text()
    assert "long" in output_content
    assert "short" not in output_content


def test_filter_keeps_all_when_threshold_low(tmp_path):
    input_fasta = tmp_path / "input.fasta"
    input_fasta.write_text(">seq1\nATGC\n>seq2\nATGCATGC\n")
    output_fasta = tmp_path / "output.fasta"

    n_kept = filter_sequences(str(input_fasta), str(output_fasta), min_length=1)

    assert n_kept == 2