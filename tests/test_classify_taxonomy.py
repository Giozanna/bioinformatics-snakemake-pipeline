import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from classify_taxonomy import train_classifier, classify_sequences


def test_classifier_recovers_exact_match(tmp_path):
    ref_fasta = tmp_path / "ref.fasta"
    ref_fasta.write_text(
        ">RefA\nATGCATGCATGCATGCATGCATGC\n>RefB\nTTTTGGGGCCCCAAAATTTTGGGG\n"
    )

    ref_tax = tmp_path / "ref_tax.tsv"
    ref_tax.write_text(
        "Feature ID\tTaxon\nRefA\tk__Fungi;g__Alpha;s__Alpha_sp1\n"
        "RefB\tk__Fungi;g__Beta;s__Beta_sp1\n"
    )

    query_fasta = tmp_path / "query.fasta"
    query_fasta.write_text(">Query1\nATGCATGCATGCATGCATGCATGC\n")

    vectorizer, clf = train_classifier(str(ref_fasta), str(ref_tax))
    results = classify_sequences(str(query_fasta), vectorizer, clf)

    assert results.loc[0, "Taxon"] == "k__Fungi;g__Alpha;s__Alpha_sp1"
    assert results.loc[0, "Confidence"] > 0.5