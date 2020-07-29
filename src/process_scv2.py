import pandas as pd
from src.scv2_genome import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

df_processed = pd.read_csv("scv2-mirna-bindings-noncomplementary-full-genome.csv")
df_locations = pd.read_csv("data/db/scv2-annotated-simple.csv")

coordinates = list()

# for index, row in df_processed.iterrows():
# 	sites_dict = return_sites(row["seed_locations"])
# 	visualize_matrix.append(row["seed_locations"])

for i in range(df_processed.shape[0]):
	coordinates.append((i,eval(df_processed.iloc[i]["seed_locations"])))

x_coords = list()
y_coords = list()

for coord in coordinates:
	print(coord)
	for coord_ in coord[1]:
		x_coords.append(coord_)
		y_coords.append(coord[0])


fig, ax = plt.subplots(1,1)
ax.scatter(x_coords, y_coords, s=0.1)
plt.ylim(0,1600)
plt.xlim(0,30000)
for index, row in df_locations.iterrows():
	ax.plot((row["start"],row["start"],row["end"],row["end"],row["start"]),(0,900,900,0,0), label=row["name"])

plt.legend()

plt.xlabel("Sars-Cov-2 Genome Position")
plt.ylabel("miRNAs picked up by MirDB")
plt.title("Visual Scatter Plot of Predicted miRNA binding sites on the SCV2 genome")

plt.savefig("data/results/seed_locations_heatmap.png")
