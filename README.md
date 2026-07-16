![Pipeline Status](https://github.com/Giozanna/bioinformatics-snakemake-pipeline/actions/workflows/pipeline.yml/badge.svg)
# Bioinformatics Snakemake Pipeline

A small, reproducible pipeline for FASTA sequence quality control: filters
sequences by minimum length, computes per-sequence statistics (length, GC
content), and generates a summary plot.

Built to demonstrate a Python + Snakemake workflow — the kind of
reproducible, scalable pipeline structure I use for microbial genomics and
multi-omics data analysis.

## Pipeline steps

1. **filter_sequences** — removes sequences shorter than a configurable
   minimum length
2. **compute_stats** — calculates sequence length and GC content per
   sample, saved as CSV
3. **plot_stats** — generates a bar chart of GC content per sample

## Requirements

- Python 3.12+
- Snakemake
- Biopython, pandas, matplotlib

Install with:

    pip install -r requirements.txt

## Usage

    snakemake --cores 1

Snakemake automatically resolves the step order from each rule's declared
inputs/outputs — see the `Snakefile` for the full pipeline definition.

## Configuration

Minimum sequence length is set in `config.yaml`:

    min_length: 45

## Project structure

    .
    ├── Snakefile          # pipeline definition
    ├── config.yaml         # parameters
    ├── data/                # input FASTA files
    ├── scripts/             # one Python script per pipeline step
    └── results/             # generated outputs (filtered FASTA, stats CSV, plot)

## Amplicon sequencing workflow (extended pipeline)

In addition to the FASTA QC demo above, this repository includes a second
pipeline that mirrors, structurally, a real fungal ITS metabarcoding
workflow — primer trimming, denoising, and taxonomy assignment — the kind
of amplicon sequencing pipeline I run for microbiome research, built here
on entirely synthetic demo data so the repository stays public.

**This is a structural demonstration, not a working microbiome analysis.**
The synthetic data, toy reference database, and small read counts are
deliberately simplified to run quickly on a laptop; conclusions from this
demo pipeline are not biologically meaningful. The point is to show correct
use of each tool's real API and a realistic multi-language pipeline
structure.

### Pipeline steps

1. **generate_demo_reads** — creates small synthetic paired-end FASTQ files
   (45 reads across 3 synthetic amplicon variants), flanked by real
   published fungal ITS primers (ITS3/ITS4; White et al., 1990)
2. **trim_primers** (`cutadapt`; Martin, 2011) — removes primer sequences
   from both read directions
3. **denoise_dada2** (`DADA2`, in R; Callahan, McMurdie & Holmes, 2017) —
   quality filtering, error-rate learning, denoising, paired-end merging,
   and chimera removal. Called from the Snakemake pipeline via `Rscript`,
   so this is a **polyglot pipeline**: Python/Snakemake orchestrates a
   step implemented in R — a realistic pattern in real bioinformatics
   pipelines, where the best tool for a task often lives in a different
   language ecosystem.
4. **build_reference** — builds a small synthetic reference database with
   UNITE-style taxonomy strings, standing in for the real UNITE database
   (Abarenkov et al., 2025), which is several GB and impractical for a
   local demo
5. **classify_taxonomy** — assigns taxonomy using a **Naive Bayes k-mer
   classifier** (`scikit-learn`), the same core algorithm QIIME2's
   `classify-sklearn` method uses under the hood (Bokulich et al., 2018) —
   reimplemented directly in Python rather than through QIIME2 itself.

### What this run actually showed

With only 45 synthetic reads across 3 amplicon variants differing by a few
bases each, DADA2 collapsed all reads into a **single ASV** rather than
recovering 3 — and this is the algorithm working as intended, not a bug.
DADA2's error model is built for real sequencing depth (typically
millions of reads); with this little data, it correctly treats such small
differences as sequencing noise rather than true biological variation,
since it cannot statistically distinguish the two at this scale. The
classifier then assigned that single ASV to `Fusarium_sp1` with full
confidence (1.0), matching the closest reference sequence.

This is a useful result to be upfront about: it shows the pipeline's
components work correctly end-to-end, while also showing a real,
well-understood limitation of denoising algorithms on small datasets —
which is exactly the kind of judgment call that matters when interpreting
real (much larger) sequencing runs.

### Why this structure?

This mirrors the amplicon sequencing pipeline described in my own research
(demultiplexing → primer trimming with cutadapt → DADA2 denoising →
Naive Bayes taxonomy assignment against UNITE, run in QIIME2 on an HPC
cluster), reimplemented here as a lighter, fully public, locally-runnable
version:

| Real pipeline | This demo |
|---|---|
| QIIME2 (Bolyen et al., 2019) on HPC | Individual tools called directly, orchestrated by Snakemake |
| cutadapt via QIIME2 plugin | cutadapt called directly |
| DADA2 via QIIME2 plugin | DADA2 called directly from R |
| UNITE database (100,000+ sequences) | Toy 5-sequence synthetic reference |
| QIIME2 Naive Bayes classifier | Naive Bayes classifier reimplemented directly in scikit-learn |

### Setup

Python dependencies (add to `requirements.txt`):

    cutadapt
    scikit-learn

R dependency (install in R/RStudio, not via pip):

    if (!requireNamespace("BiocManager", quietly = TRUE))
        install.packages("BiocManager")
    BiocManager::install("dada2")

### Run

    snakemake --cores 1

### References

- Bolyen, E. et al. (2019). Reproducible, interactive, scalable and
  extensible microbiome data science using QIIME 2. *Nature
  Biotechnology*.
- Martin, M. (2011). Cutadapt removes adapter sequences from
  high-throughput sequencing reads. *EMBnet.journal*.
- Callahan, B.J., McMurdie, P.J., Holmes, S.P. (2017). Exact sequence
  variants should replace operational taxonomic units in marker-gene data
  analysis. *The ISME Journal*.
- Abarenkov, K. et al. (2025). UNITE general FASTA release for Fungi,
  version 10.
- White, T.J. et al. (1990). Amplification and direct sequencing of fungal
  ribosomal RNA genes for phylogenetics. In *PCR Protocols*.
- Bokulich, N.A. et al. (2018). Optimizing taxonomic classification of
  marker-gene amplicon sequences with QIIME 2's    