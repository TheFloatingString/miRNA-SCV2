"""
Pubmed scraper
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import pickle

df = pd.read_csv("scv2-mirna-bindings.csv")

gene_names = df["name"].values

gene_litterature_dict = dict()

for gene_name in gene_names:

	gene_name = gene_name.replace("-3p","").replace("-5p","").replace("hsa-","")

	URL = f"https://www.ncbi.nlm.nih.gov/pmc/?term=({gene_name})+AND+pneumonia%5BAbstract%5D"
	soup = BeautifulSoup(requests.get(URL).content, "html.parser")

	list_of_titles = soup.find_all("div", attrs={"class":"title"})
	gene_litterature_dict[gene_name] = [title.get_text() for title in list_of_titles]

	print(f"{gene_name}:\t{len(list_of_titles)}")

with open('mirna_litterature.pickle', 'wb') as handle:
    pickle.dump(gene_litterature_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)