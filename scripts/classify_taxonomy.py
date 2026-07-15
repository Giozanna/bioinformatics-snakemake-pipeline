"""
Assign taxonomy to ASVs using a Naive Bayes k-mer classifier.

This implements the same core algorithm used by QIIME2's classify-sklearn
method (Bokulich et al. 2018): sequences are represented as k-mer frequency
vectors, and a multinomial Naive Bayes classifier — trained on a reference
database of sequences with known taxonomy — predicts the taxonomy of each
query sequence.

Here the "reference database" is the small synthetic toy_unite_reference
built by build_toy_reference.py, standing in for the real UNITE database,
so the workflow can run quickly and locally for demonstration purposes.
"""

import sys
from Bio import SeqIO
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd


def kmerize(seq, k=7):
    seq = str(seq).upper()
    if len(seq) < k:
        return seq
    return " ".join(seq[i:i + k] for i in range(len(seq) - k + 1))


def main():
    query_fasta = sys.argv[1]
    ref_fasta = sys.argv[2]
    ref_taxonomy_tsv = sys.argv[3]
    output_tsv = sys.argv[4]

    ref_records = list(SeqIO.parse(ref_fasta, "fasta"))
    ref_tax = pd.read_csv(ref_taxonomy_tsv, sep="\t").set_index("Feature ID")["Taxon"]

    ref_ids = [r.id for r in ref_records]
    ref_kmers = [kmerize(r.seq) for r in ref_records]
    ref_labels = [ref_tax[i] for i in ref_ids]

    vectorizer = CountVectorizer(analyzer=lambda x: x.split())
    x_ref = vectorizer.fit_transform(ref_kmers)

    clf = MultinomialNB()
    clf.fit(x_ref, ref_labels)

    query_records = list(SeqIO.parse(query_fasta, "fasta"))
    if not query_records:
        raise ValueError(f"No sequences found in {query_fasta}")

    query_kmers = [kmerize(r.seq) for r in query_records]
    x_query = vectorizer.transform(query_kmers)

    predictions = clf.predict(x_query)
    probabilities = clf.predict_proba(x_query).max(axis=1)

    results = pd.DataFrame({
        "Feature ID": [r.id for r in query_records],
        "Taxon": predictions,
        "Confidence": probabilities.round(3)
    })
    results.to_csv(output_tsv, sep="\t", index=False)
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
