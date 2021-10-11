from src import scv2_genome
from src import variants

import csv

scv2_refseq_sequence = scv2_genome.return_scv2(0,-1)

mutation_dict = dict()

with open("data/variants/501.V2_changes.csv", newline='\n') as csvfile:
	filereader = csv.reader(csvfile, delimiter=',')
	mutation_dict["501.V2"] = [row[0] for row in filereader]



with open("data/variants/B.1.1.7_changes.csv", newline='\n') as csvfile:
	filereader = csv.reader(csvfile, delimiter=',')
	mutation_dict["B.1.1.7"] = [row[0] for row in filereader]



print(mutation_dict["B.1.1.7"])

mutation_obj = variants.Variant()
mutation_obj.upload(scv2_refseq_sequence)
mutation_obj.generate(mutation_dict["B.1.1.7"], "B.1.1.7 mutation sequence")
mutation_obj.save_to_txt("data/variant_seq/B.1.1.7.txt")
