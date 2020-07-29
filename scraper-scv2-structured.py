from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import pandas as pd

from src.converter import find_rna_complement


rows_list = list()

f = open("data/db/sars-cov-2-conserved-structured.csv", "r")
file_content_list = f.read().split("\n")

conserved_sequences = list()

length = len(file_content_list)

for i in range(int(length/9)):
	conserved_sequences.append({"name":file_content_list[9*i]+file_content_list[9*i+1],
		"sequence":file_content_list[9*i+2].split()[1]+file_content_list[9*i+3]+file_content_list[9*i+4]})


chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome("static/chromedriver.exe", chrome_options=chrome_options)

start = time.time()

for rna_dict in conserved_sequences:

	rna_sequence_name = rna_dict["name"]
	rna_sequence = find_rna_complement(rna_dict["sequence"])

	driver.get("http://www.mirbase.org/search.shtml")

	print(f"Searching sequence: {rna_sequence_name}")
	sequence_input = driver.find_element_by_css_selector("textarea[name='sequence']")
	sequence_input.send_keys(rna_sequence)

	e_value_cutoff = driver.find_element_by_css_selector("input[name='evalue']")
	e_value_cutoff.clear()
	e_value_cutoff.send_keys(1000)

	driver.find_element_by_css_selector("input[value='hsa'][type='checkbox']").click()

	driver.find_element_by_css_selector("form[name='sequence']").submit()

	elements = driver.find_elements_by_css_selector("pre[class='alignmentString']")
	for element, item in zip(elements, driver.find_elements_by_css_selector("li[class='alignmentItem']")):
		rna_dict = dict()
		rna_dict["sequence_name"] = rna_sequence_name

		value = element.get_attribute('innerHTML')
		match_lines = value.split("<br>")[1].split()[0]
		rna_dict["max_consecutive"] = max([len(item) for item in match_lines.split()])
		rna_dict["name"] = value.split("<br>")[2].split()[0]

		content = item.get_attribute("innerHTML")
		soup = BeautifulSoup(content, "html.parser")

		li_elements = soup.find_all("li")

		rna_dict["score"] = float(li_elements[2].text.strip().split(": ")[1])
		rna_dict["evalue"] = float(li_elements[3].text.strip().split(": ")[1])
		rna_dict["alignments"] = match_lines

		rows_list.append(rna_dict)		



df = pd.DataFrame(rows_list)
df.to_csv("data/results/mirbase_scrape_results.csv", index=False)

print(f"Elapsed:{time.time()-start}")