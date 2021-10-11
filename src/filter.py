"""
Take literature results and print scores
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt 

from src.scv2_genome import *

with open("mirna_litterature.pickle", "rb") as handle:
	litterature_dict = pickle.load(handle)

df = pd.read_csv("scv2-mirna-bindings-noncomplementary-full-genome.csv")

# print(litterature_dict.keys())
# print(litterature_dict[list(litterature_dict.keys())[1]])

non_null_names = list()

for key in list(litterature_dict.keys()):
	if len(litterature_dict[key]) != 0:
		non_null_names.append(key.replace("-3p",'').replace("-5p", '').replace("hsa-",''))

print("length:!")
print(len(non_null_names))
# print(non_null_names)

values_list = [0]*100

for index, row in df.iterrows():
	if row["name"].replace("-3p",'').replace("-5p", '').replace("hsa-",'') in non_null_names:
		# print(row["name"])
		values_list[int(row["score"])] += 1


# plt.plot(range(50,100), values_list[50:])
# plt.title("Frequency of miRNA strands in function of their MirDB scores")
# plt.xlabel("score")
# plt.ylabel("frequency")
# plt.savefig("data/results/mirdb_score_distribution.png")

rows_list = list()

counter = 0

for index, row in df.iterrows():
	if row["name"].replace("-3p",'').replace("-5p", '').replace("hsa-",'') in non_null_names:
		dict_scores = dict()
		pos_dict = return_sites(eval(row["seed_locations"]))
		n_protein_encode = 0
		for key in pos_dict.keys():
			if pos_dict[key] != '':
				n_protein_encode += check_conserved(int(key))
		dict_scores["name"] = row["name"]
		dict_scores["score"] = row["score"]*n_protein_encode
		dict_scores["n_protein"] = n_protein_encode
		dict_scores["n_seed_locations"] = row["n_seed_locations"]
		if dict_scores["score"]>0: 
			rows_list.append(dict_scores) 
			# print(counter)
			counter += 1

df_filtered = pd.DataFrame(rows_list)
df_filtered	= df_filtered.sort_values("score", ascending=False)
print(df_filtered.shape)
counter = 1
for index, row in df_filtered.iterrows():
	print(counter, row["name"])
	counter += 1
	# print(row.values)
	# print(litterature_dict[row["name"].replace("-3p",'').replace("-5p", '').replace("hsa-",'')])

plt.close()
plt.plot(range(len(df_filtered["score"].values)), df_filtered["score"].values)
plt.savefig("data/results/filtered_distribution.png")

list_of_locations = df_filtered["n_seed_locations"].values.tolist()
print("Average: ", sum(list_of_locations)/len(list_of_locations))
print("Max:     ", max(list_of_locations))
