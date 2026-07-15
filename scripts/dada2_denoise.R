#!/usr/bin/env Rscript
#
# Denoise paired-end amplicon reads with DADA2 (Callahan, McMurdie & Holmes,
# 2016), following the standard DADA2 workflow: quality filtering, error-rate
# learning, denoising, paired-end merging, and chimera removal.
#
# This script is called from the Snakemake pipeline via Rscript, so a single
# Python-orchestrated pipeline combines a Python step (cutadapt primer
# trimming) with this R step — a "polyglot" pipeline, which is a realistic
# pattern in bioinformatics workflows where the best tool for each step
# lives in a different language ecosystem.
#
# NOTE: this runs on a small synthetic demo dataset (a few dozen reads),
# built for portfolio purposes. DADA2's error-learning step is designed for
# real sequencing runs with far more reads (typically millions); with this
# little data it is statistically underpowered. This script demonstrates
# the correct workflow structure and API usage, not publication-grade
# denoising — see the repository README for details.

suppressMessages(library(dada2))

args <- commandArgs(trailingOnly = TRUE)
r1_path <- args[1]
r2_path <- args[2]
output_table <- args[3]
output_fasta <- args[4]

filt_dir <- file.path(dirname(output_table), "filtered")
dir.create(filt_dir, showWarnings = FALSE, recursive = TRUE)

filt_r1 <- file.path(filt_dir, "filt_R1.fastq.gz")
filt_r2 <- file.path(filt_dir, "filt_R2.fastq.gz")

cat("Step 1/5: filtering and trimming...\n")
filterAndTrim(
  r1_path, filt_r1, r2_path, filt_r2,
  truncLen = 0, maxEE = c(2, 2), truncQ = 2, rm.phix = TRUE,
  compress = TRUE, multithread = FALSE
)

cat("Step 2/5: learning error rates...\n")
err_r1 <- learnErrors(filt_r1, multithread = FALSE)
err_r2 <- learnErrors(filt_r2, multithread = FALSE)

cat("Step 3/5: denoising...\n")
dada_r1 <- dada(filt_r1, err = err_r1, multithread = FALSE)
dada_r2 <- dada(filt_r2, err = err_r2, multithread = FALSE)

cat("Step 4/5: merging paired-end reads...\n")
merged <- mergePairs(dada_r1, filt_r1, dada_r2, filt_r2)

cat("Step 5/5: building sequence table and removing chimeras...\n")
seqtab <- makeSequenceTable(merged)
seqtab_nochim <- removeBimeraDenovo(
  seqtab, method = "consensus", multithread = FALSE, verbose = TRUE
)

cat(sprintf("ASVs before chimera removal: %d\n", ncol(seqtab)))
cat(sprintf("ASVs after chimera removal: %d\n", ncol(seqtab_nochim)))

write.csv(t(seqtab_nochim), output_table)

asv_seqs <- colnames(seqtab_nochim)
asv_ids <- paste0("ASV_", seq_along(asv_seqs))
fasta_lines <- character(length(asv_seqs) * 2)
fasta_lines[c(TRUE, FALSE)] <- paste0(">", asv_ids)
fasta_lines[c(FALSE, TRUE)] <- asv_seqs
writeLines(fasta_lines, output_fasta)

cat("Done — ASV table and representative sequences written.\n")
