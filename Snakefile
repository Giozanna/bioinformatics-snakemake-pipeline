configfile: "config.yaml"

rule all:
    input:
        "results/plot.png",
        "results/taxonomy_assignments.tsv"


# ============================================================
# Part 1: original FASTA QC demo (length filter, stats, plot)
# ============================================================

rule filter_sequences:
    input:
        "data/sample_sequences.fasta"
    output:
        "results/filtered.fasta"
    params:
        min_length=config["min_length"]
    shell:
        "python scripts/filter_sequences.py {input} {output} {params.min_length}"

rule compute_stats:
    input:
        "results/filtered.fasta"
    output:
        "results/stats.csv"
    shell:
        "python scripts/compute_stats.py {input} {output}"

rule plot_stats:
    input:
        "results/stats.csv"
    output:
        "results/plot.png"
    shell:
        "python scripts/plot_stats.py {input} {output}"


# ============================================================
# Part 2: amplicon sequencing workflow (synthetic demo data)
# Mirrors, structurally, a real ITS metabarcoding pipeline:
# primer trimming (cutadapt) -> denoising (DADA2, in R) ->
# taxonomy assignment (Naive Bayes classifier, scikit-learn)
# ============================================================

rule generate_demo_reads:
    output:
        r1="data/reads_R1.fastq.gz",
        r2="data/reads_R2.fastq.gz"
    shell:
        "python scripts/generate_demo_reads.py"

rule trim_primers:
    input:
        r1="data/reads_R1.fastq.gz",
        r2="data/reads_R2.fastq.gz"
    output:
        r1="results/trimmed_R1.fastq.gz",
        r2="results/trimmed_R2.fastq.gz"
    params:
        fwd_primer=config["its3_primer"],
        rev_primer=config["its4_primer"]
    shell:
        "cutadapt -g {params.fwd_primer} -G {params.rev_primer} "
        "--discard-untrimmed -e 0.1 "
        "-o {output.r1} -p {output.r2} "
        "{input.r1} {input.r2}"

rule denoise_dada2:
    input:
        r1="results/trimmed_R1.fastq.gz",
        r2="results/trimmed_R2.fastq.gz"
    output:
        table="results/asv_table.csv",
        fasta="results/asv_sequences.fasta"
    shell:
        "Rscript scripts/dada2_denoise.R {input.r1} {input.r2} {output.table} {output.fasta}"

rule build_reference:
    output:
        fasta="data/toy_unite_reference.fasta",
        taxonomy="data/toy_unite_taxonomy.tsv"
    shell:
        "python scripts/build_toy_reference.py"

rule classify_taxonomy:
    input:
        query="results/asv_sequences.fasta",
        ref_fasta="data/toy_unite_reference.fasta",
        ref_tax="data/toy_unite_taxonomy.tsv"
    output:
        "results/taxonomy_assignments.tsv"
    shell:
        "python scripts/classify_taxonomy.py {input.query} {input.ref_fasta} {input.ref_tax} {output}"
