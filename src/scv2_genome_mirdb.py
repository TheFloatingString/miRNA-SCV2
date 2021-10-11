"""
miRBD search
"""

from src.scv2_genome import return_scv2
from src.converter import find_rna_complement

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup

import pandas as pd

import time

chrome_options = Options()

rows_list = list()

driver = webdriver.Chrome("static/chromedriver.exe", chrome_options=chrome_options)

rna_sequence = return_scv2(0,-1).replace('T','U')

driver.get("http://mirdb.org/custom.html")

select_species = Select(driver.find_element_by_css_selector("select[name='searchSpecies']"))
select_species.select_by_value("hsa")

select_choice = Select(driver.find_element_by_css_selector("select[name='subChoice']"))
select_choice.select_by_value("mRNATarget")

sequence_input = driver.find_element_by_css_selector("textarea[name='customSub']")
sequence_input.send_keys(rna_sequence)

driver.find_element_by_css_selector("form[name='mirSeq']").submit()

time.sleep(30)

driver.find_element_by_css_selector("input[type='submit']").click()

for score, rna_name in zip(driver.find_elements_by_css_selector("td[width='65']"), driver.find_elements_by_css_selector("td[width='125']")):
	if score.text != "Target Score":
		temp_dict = dict()
		print(score.text, rna_name.text)
		temp_dict["score"] = score.text 
		temp_dict["name"] = rna_name.text 
		rows_list.append(temp_dict)

buttons = driver.find_elements_by_css_selector("input[value='Details']")

for i in range(len(buttons)):
	buttons = driver.find_elements_by_css_selector("input[value='Details']")
	print(len(buttons))
	temp_dict = dict()
	buttons[i].click()
	try:
		temp_dict["name"] = driver.find_elements_by_css_selector("td[width='123']")[0].text
		temp_dict["sequence"] = driver.find_elements_by_css_selector("td[width='258']")[0].text
		temp_dict["seed_locations"] = [int(x.strip()) for x in driver.find_elements_by_css_selector("td[width='258']")[1].text.split(",")]
		temp_dict["n_seed_locations"] = len(temp_dict["seed_locations"])
		temp_dict["score"] = float(driver.find_elements_by_css_selector("td[width='123']")[1].text)
		print(temp_dict)
		rows_list.append(temp_dict)
	except:
		print(f"Error at : {i}th element")
	driver.execute_script("window.history.go(-1)")

df = pd.DataFrame(rows_list)
print(f"DataFrame shape: {df.shape}")
df.to_csv("scv2-mirna-bindings.csv", index=False)

