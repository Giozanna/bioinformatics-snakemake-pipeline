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

Install with:pip install -r requirements.txt
## Usage 
snakemake --cores 1
Snakemake automatically resolves the step order from each rule's declared
inputs/outputs — see the `Snakefile` for the full pipeline definition.

## Configuration

Minimum sequence length is set in `config.yaml`:
```yaml
min_length: 45
```

## Project structure
.
├── Snakefile          # pipeline definition
├── config.yaml         # parameters
├── data/                # input FASTA files
├── scripts/             # one Python script per pipeline step
└── results/             # generated outputs (filtered FASTA, stats CSV, plot)