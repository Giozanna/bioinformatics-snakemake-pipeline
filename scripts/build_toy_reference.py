"""
Build a small, synthetic "toy UNITE-style" reference database.

The real UNITE database (Abarenkov et al. 2025) contains 100,000+ curated
fungal ITS reference sequences and is several GB — impractical for a local
portfolio demo. This script instead creates a tiny, structurally realistic
stand-in: a handful of synthetic reference sequences with UNITE-style
taxonomy strings (kingdom to species), used to demonstrate the
classification workflow itself rather than to produce biologically
meaningful taxonomy calls.
"""

import os

# (reference_id, UNITE-style taxonomy string, synthetic sequence)
# 3 of these are close variants of the sequences used to simulate reads in
# generate_demo_reads.py, so the classifier has a real signal to detect;
# 2 additional, more distinct sequences act as "decoy" taxa so the
# classifier has genuine contrast to learn from.
REFERENCE_TAXA = [
    (
        "RefSeq_1",
        "k__Fungi;p__Ascomycota;c__Sordariomycetes;o__Hypocreales;f__Nectriaceae;g__Fusarium;s__Fusarium_sp1",
        "TTGGTGTGCATCGATGAAGAACGCAGCGAAATGCGATAAGTAATGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACATTGCGCCCTTTGGTATTCCGAAGGGCATGCCTGTTCGAGCGTCATTT",
    ),
    (
        "RefSeq_2",
        "k__Fungi;p__Ascomycota;c__Sordariomycetes;o__Hypocreales;f__Nectriaceae;g__Fusarium;s__Fusarium_sp2",
        "TTGGTGTGCATCGATGAAGAACGCAGCGAAATGCGATACGTAATGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACATTGCGCCCCTTGGTATTCCGAGGGGCATGCCTGTTTGAGCGTCATTA",
    ),
    (
        "RefSeq_3",
        "k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Agaricales;f__Marasmiaceae;g__Marasmius;s__Marasmius_sp1",
        "TTGGTGTGCATCGATGAAGAACGCAGCGAAATGCGATAAGTAACGTGAATTGCAGAATTCAGTGAATCATCGAATCTTTGAACGCACCTTGCGCCCTTTGGTATTCCGAAGGGCATGCCTGTTCGAGCGTCATTC",
    ),
    (
        "RefSeq_4",
        "k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Polyporales;f__Polyporaceae;g__Trametes;s__Trametes_sp1",
        "GGAAGTAAAAGTCGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTATTGAATATGAATATCCCTATCCATTGTGAACATACCTAAATGTTGCCTCGGCGGATCAGCCCGCTCCCGGTAAAACGGGA",
    ),
    (
        "RefSeq_5",
        "k__Fungi;p__Mucoromycota;c__Mucoromycetes;o__Mucorales;f__Mucoraceae;g__Mucor;s__Mucor_sp1",
        "GGAAGTAAAAGTCGTAACAAGGTTTCCGTAGGTGAACCTGCGGAAGGATCATTATCGAGTTTTAACTGATTGCAATCTCTTCCCAAATAAAACTTTCCACGTGAACTGTCTGTGATCTTGACGTTGATAATGGCC",
    ),
]


def main():
    os.makedirs("data", exist_ok=True)
    fasta_path = os.path.join("data", "toy_unite_reference.fasta")
    tax_path = os.path.join("data", "toy_unite_taxonomy.tsv")

    with open(fasta_path, "w") as fasta_out, open(tax_path, "w") as tax_out:
        tax_out.write("Feature ID\tTaxon\n")
        for seq_id, taxon, seq in REFERENCE_TAXA:
            fasta_out.write(f">{seq_id}\n{seq}\n")
            tax_out.write(f"{seq_id}\t{taxon}\n")

    print(f"Wrote {len(REFERENCE_TAXA)} toy reference sequences to {fasta_path}")
    print(f"Wrote taxonomy strings to {tax_path}")


if __name__ == "__main__":
    main()
