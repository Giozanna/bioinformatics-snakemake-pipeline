"""
Generate small synthetic paired-end FASTQ files for pipeline demonstration.

These reads are entirely synthetic (not real sequencing data): a handful of
made-up amplicon sequences, each flanked by real, published fungal ITS
primers (ITS3/ITS4, White et al. 1990), with light random sequencing noise
added. This gives the downstream cutadapt and DADA2 steps something
realistic to work with, without using any real (and unpublished) research
data.
"""

import random
import gzip
import os

random.seed(42)

# Real, published fungal ITS primers (White et al. 1990) — commonly used
# to amplify the ITS2 region for fungal community profiling.
ITS3 = "GCATCGATGAAGAACGCAGC"
ITS4 = "TCCTCCGCTTATTGATATGC"

# A handful of synthetic "true" amplicon sequences (NOT real organisms),
# used as templates to simulate reads from 3 distinct ASVs.
TRUE_SEQS = [
    "TTGGTGTGCATCGATGAAGAACGCAGCGAAATGCGATAAGTAATGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACATTGCGCCCTTTGGTATTCCGAAGGGCATGCCTGTTCGAGCGTCATTT",
    "TTGGTGTGCATCGATGAAGAACGCAGCGAAATGCGATACGTAATGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACATTGCGCCCCTTGGTATTCCGAGGGGCATGCCTGTTTGAGCGTCATTA",
    "TTGGTGTGCATCGATGAAGAACGCAGCGAAATGCGATAAGTAACGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACCTTGCGCCCTTTGGTATTCCGAAGGGCATGCCTGTTCGAGCGTCATTC",
]

N_READS_PER_SEQ = 15


def revcomp(seq):
    comp = str.maketrans("ACGT", "TGCA")
    return seq.translate(comp)[::-1]


def add_errors(seq, error_rate=0.005):
    bases = list(seq)
    for i in range(len(bases)):
        if random.random() < error_rate:
            bases[i] = random.choice("ACGT")
    return "".join(bases)


def make_quality(length, base_qual=37):
    # Phred+33 quality string, with a slight realistic drop toward the read end
    quals = []
    for i in range(length):
        q = base_qual - int(8 * (i / length))
        q = max(q, 20)
        quals.append(chr(q + 33))
    return "".join(quals)


def main():
    os.makedirs("data", exist_ok=True)

    r1_records = []
    r2_records = []
    read_id = 0

    for sample_idx, true_seq in enumerate(TRUE_SEQS):
        for _ in range(N_READS_PER_SEQ):
            read_id += 1
            noisy_seq = add_errors(true_seq)
            r1_seq = ITS3 + noisy_seq
            r2_seq = ITS4 + revcomp(noisy_seq)
            header = f"READ_{read_id}_variant{sample_idx + 1}"
            r1_records.append((header, r1_seq, make_quality(len(r1_seq))))
            r2_records.append((header, r2_seq, make_quality(len(r2_seq))))

    r1_path = os.path.join("data", "reads_R1.fastq.gz")
    r2_path = os.path.join("data", "reads_R2.fastq.gz")

    with gzip.open(r1_path, "wt") as f1, gzip.open(r2_path, "wt") as f2:
        for header, seq, qual in r1_records:
            f1.write(f"@{header}/1\n{seq}\n+\n{qual}\n")
        for header, seq, qual in r2_records:
            f2.write(f"@{header}/2\n{seq}\n+\n{qual}\n")

    print(f"Generated {len(r1_records)} synthetic paired-end reads "
          f"across {len(TRUE_SEQS)} amplicon variants")
    print(f"Wrote {r1_path} and {r2_path}")


if __name__ == "__main__":
    main()
