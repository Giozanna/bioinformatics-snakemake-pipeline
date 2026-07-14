configfile: "config.yaml"

rule all:
    input:
        "results/plot.png"

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