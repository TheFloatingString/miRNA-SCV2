import pandas as pd 
import numpy as np

df_start = pd.read_csv("data/results/scv2-mirna-bindings-0-15500.csv")
df_end = pd.read_csv("data/results/scv2-mirna-bindings-15000-end.csv")

print(type(df_start["name"].values))

unique_names = np.unique(df_start["name"].values.tolist() + df_end["name"].values.tolist())

final_dict = dict()
for name in unique_names:
	final_dict[name] = 0

for index, row in df_start.iterrows():
	final_dict[row["name"]] += row["score"]

for index, row in df_end.iterrows():
	final_dict[row["name"]] += row["score"]

rows_list = list()
for key in final_dict.keys():
	temp_dict = dict()
	temp_dict["name"] = key
	temp_dict["score"] = final_dict[key]
	rows_list.append(temp_dict)


df_final = pd.DataFrame(rows_list)
df_final = df_final.sort_values("score", ascending=False)
print(df_final.head())
df_final.to_csv("data/results/mirna-bindings-final.csv", index=False)