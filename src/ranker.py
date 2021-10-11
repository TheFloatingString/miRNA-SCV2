"""
Data to visualize ranked results
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df_sars_related = pd.read_csv("data/results/mirbase_scrape_results-sars-related-complement-final.csv")
df_scv2_conserved = pd.read_csv("data/results/mirbase_scrape_results-scv2-conserved-complement.csv")
df_scv2_conserved = df_scv2_conserved[df_scv2_conserved.name.str[0:3]=="hsa"]

df_sars_related.sort_values("score", ascending=False)

# VALUE = 12

# for index, row in df_sars_related.loc[df_sars_related["score"] >= VALUE].iterrows():
# 	print(row["name"])

# frequency_dict = dict()
# for value in np.unique(df_sars_related["max_consecutive"].values):

X = df_sars_related["max_consecutive"].value_counts().index.values
Y = df_sars_related["max_consecutive"].value_counts().values

Y_sorted = [x for _, x in sorted(zip(X,Y))]

total = sum(Y)
count = 0
counter = 1
for item in Y_sorted:
	count += item
	print(counter, count/total)
	counter += 1

print()

plt.bar(sorted(X), Y_sorted)
plt.xlabel("Consecutive alignments")
plt.ylabel("Count")
plt.title("miRNA Alignment Distribution of SARS Related Sequences in SARS-CoV-2")
plt.savefig("data/results/sars_related.png", dpi=200)
plt.close()

X = df_scv2_conserved["score"].value_counts().index.values
Y = df_scv2_conserved["score"].value_counts().values

Y_sorted = [x for _, x in sorted(zip(X,Y))]

total = sum(Y)
count = 0
counter = 1

for item in Y_sorted:
	count += item
	print(counter, count/total)
	counter += 1

plt.bar(sorted(X), Y_sorted)
plt.xlabel("Consecutive alignments")
plt.ylabel("Count")
plt.title("miRNA Alignment Distribution of Sars-Cov-2 Conserved Sequences")
plt.savefig("data/results/score_scv2_conserved.png", dpi=200)
plt.close()

# VALUE = 13
# for index, row in df_scv2_conserved.loc[df_scv2_conserved["max_consecutive"] >= VALUE].iterrows():
# 	print(row["name"])


# plt.bar(df_sars_related["max_consecutive"].values)
# plt.show()

# for index, row in df_scv2_conserved.loc[df_scv2_conserved["max_consecutive"] >= VALUE].iterrows():
# 	print(row["name"])