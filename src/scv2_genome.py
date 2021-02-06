"""
Functions to process SCV2 data
"""

from Bio import SeqIO
import pandas as pd

scv2_sequence = ''

for seq_record in SeqIO.parse("data/db/sars-cov-2-wuhan-1.fasta", "fasta"):
	scv2_sequence = seq_record
	break

df = pd.read_csv("data/db/scv2-annotated-simple.csv")

df_conserved = pd.read_csv("data/db/scv-scv2-align-simplified.csv")

def return_scv2(start, end):
	print(len(scv2_sequence[start:end].seq))
	return str(scv2_sequence[start:end].seq)

def return_sites(list_of_start_indexes):
	temp_dict = dict()
	for start_index in list_of_start_indexes:
		temp_dict[start_index] = ""
		for df_index, row in df.iterrows():
			if row["start"] <= start_index <= row["end"]:
				temp_dict[start_index] = row["name"]

	return temp_dict

def check_conserved(start_index):
	for index, row in df_conserved.iterrows():
		if row["start"] <= start_index <= row["end"]:
			return 1
	return 0