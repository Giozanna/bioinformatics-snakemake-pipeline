import sys
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import pandas as pd


def compute_stats(input_path):
    """Compute length and GC content per sequence. Returns a DataFrame."""
    names, lengths, gc_contents = [], [], []
    for record in SeqIO.parse(input_path, "fasta"):
        names.append(record.id)
        lengths.append(len(record.seq))
        gc_contents.append(gc_fraction(record.seq) * 100)

    return pd.DataFrame({"sample": names, "length": lengths, "gc_percent": gc_contents})


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    df = compute_stats(input_path)
    df.to_csv(output_path, index=False)
    print(df)