"""
Functions to process SCV2 data
"""

from Bio import SeqIO
import pandas as pd

import csv

scv2_sequence = ''

for seq_record in SeqIO.parse("data/db/sars-cov-2-wuhan-1.fasta", "fasta"):
	scv2_sequence = seq_record
	break

df = pd.read_csv("data/db/scv2-annotated-simple.csv")

df_conserved = pd.read_csv("data/db/scv-scv2-align-simplified.csv")

def generate_mutation_list(file_list):
	for filename in file_list:
		file = open(filename, "r")
		instruction_list = [name for name in file.read().split("\n")]

def return_scv2(start, end):
	print(len(scv2_sequence[start:end].seq))
	return str(scv2_sequence[start:end].seq)

def return_sites(row):
	temp_dict = dict()
	for start_index in eval(row["seed_locations"]):
		temp_dict[start_index] = ""
		for df_index, row in df.iterrows():
			# check if conserved with SARS/SCV2
			if row["start"] <= start_index <= row["end"]:

				# check if not in mutation region with B117 and 501.V2
				if True:
					temp_dict[start_index] = row["name"]

	return temp_dict

def check_conserved_sars(start_index):
	for index, row in df_conserved.iterrows():
		if row["start"] <= start_index <= row["end"]:
			return True
	return False

def check_inside_mutation(start_index, sequence_length):
	return False

def check_conserved(start_index):
	# ???
	for index, row in df_conserved.iterrows():
		if row["start"] <= start_index <= row["end"]:
			return 1
	return 0