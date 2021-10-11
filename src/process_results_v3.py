"""
Program to assign a score to miRNA sequences
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt 
import statistics

import src.scv2_genome as scv2_genome

with open("mirna_litterature.pickle", "rb") as handle:
	litterature_dict = pickle.load(handle)

df = pd.read_csv("scv2-mirna-bindings-noncomplementary-full-genome.csv")

print(f"Inital number: {df.shape[0]}")
print(f"Number of literature: {sum([1 for i in list(litterature_dict.keys())])}")

non_null_names = list()


# filtering results with PubMed literature results
for key in list(litterature_dict.keys()):
	if len(litterature_dict[key]) != 0:
		non_null_names.append(key.replace("-3p",'').replace("-5p", '').replace("hsa-",''))


rows_list = list()
counter = 0


for index, row in df.iterrows():
	if row["name"].replace("-3p",'').replace("-5p", '').replace("hsa-",'') in non_null_names:
		dict_scores = dict()
		pos_dict = scv2_genome.return_sites(row)
		n_protein_encode = 0
		for key in pos_dict.keys():
			if pos_dict[key] != '':
				n_protein_encode += scv2_genome.check_conserved(int(key))
		dict_scores["name"] = row["name"]
		dict_scores["score"] = row["score"]*n_protein_encode
		dict_scores["n_protein"] = n_protein_encode
		dict_scores["n_seed_locations"] = row["n_seed_locations"]
		if dict_scores["score"]>0: 
			rows_list.append(dict_scores) 
			# print(counter)
			counter += 1

print(f"Number of final: {len(rows_list)}")

df_final = pd.DataFrame(rows_list)
df_final = df_final.sort_values(by="n_protein", ascending=False)
print(df_final.to_string())

y_data = list(df_final["n_protein"].values) + [0]*(900-len(rows_list))
x_data = list(range(len(y_data)))
plt.plot(x_data, y_data)
plt.fill_between(x_data, y_data, y2=0, where=None)
plt.title("Pareto Chart of the Number of Binding Sites")
plt.xlabel("Number of initial miRNAs")
plt.ylabel("Number of binding sites")
plt.savefig("data/results/n_protein_pareto_ranked.png")
plt.close()

df_final = df_final.sort_values(by="score", ascending=False)
for index, row in df_final.iterrows():
	print(row["name"])

print(df_final.shape)

y_data = list(df_final["score"].values) + [0]*(900-len(rows_list))
x_data = list(range(len(y_data)))
plt.plot(x_data, y_data)
plt.fill_between(x_data, y_data, y2=0, where=None)
plt.title("Pareto Chart of the miRNA Scores")
plt.xlabel("Number of initial miRNAs")
plt.ylabel("Score")
plt.savefig("data/results/score_pareto_ranked.png")


complete_data = y_data + [0]*(2656-900)

print(f"mean: {statistics.mean(complete_data)}")
print(f"stdev: {statistics.stdev(complete_data)}")
print(f"max: {statistics.stdev(complete_data)}")
print(f"min: {statistics.stdev(complete_data)}")

print(f"mean: {statistics.mean(df_final['score'].values)}")
print(f"stdev: {statistics.stdev(df_final['score'].values)}")
print(f"max: {max(df_final['score'].values)}")
print(f"min: {min(df_final['score'].values)}")

print(f"mean: {statistics.mean(df_final['n_protein'].values)}")
print(f"stdev: {statistics.stdev(df_final['n_protein'].values)}")
print(f"max: {max(df_final['n_protein'].values)}")
print(f"max: {min(df_final['n_protein'].values)}")

df_final = df_final.sort_values(by="score", ascending=False)
df_final.to_csv("data/results/scv2-full-genome-mirna-ranked-original.csv", index=False)