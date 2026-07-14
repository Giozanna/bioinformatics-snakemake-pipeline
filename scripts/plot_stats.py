import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

input_path = sys.argv[1]
output_path = sys.argv[2]

df = pd.read_csv(input_path)

plt.figure(figsize=(7, 5))
plt.bar(df["sample"], df["gc_percent"], color="#3B6EA5")
plt.axhline(50, color="grey", linestyle="--", linewidth=1)
plt.xlabel("Sample")
plt.ylabel("GC content (%)")
plt.title("GC Content per Sequence (Filtered)")
plt.tight_layout()
plt.savefig(output_path, dpi=150)