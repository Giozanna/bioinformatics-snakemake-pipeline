import sys
from Bio import SeqIO


def filter_sequences(input_path, output_path, min_length):
    """Filter FASTA sequences by minimum length. Returns number kept."""
    kept = [record for record in SeqIO.parse(input_path, "fasta") if len(record.seq) >= min_length]
    SeqIO.write(kept, output_path, "fasta")
    return len(kept)


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    min_length = int(sys.argv[3])
    n_kept = filter_sequences(input_path, output_path, min_length)
    print(f"Kept {n_kept} sequences (minimum length: {min_length})")