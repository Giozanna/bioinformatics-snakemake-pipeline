import sys
from Bio import SeqIO

input_path = sys.argv[1]
output_path = sys.argv[2]
min_length = int(sys.argv[3])

kept = [record for record in SeqIO.parse(input_path, "fasta") if len(record.seq) >= min_length]

SeqIO.write(kept, output_path, "fasta")
print(f"Kept {len(kept)} sequences (minimum length: {min_length})")