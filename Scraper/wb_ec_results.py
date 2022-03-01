import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd

#get the input values from wbec website
df_list = []

browser = webdriver.Chrome("/Users/suhairkilliyath/Downloads/chromedriver")
url = ('http://wbsec.gov.in/results/panchayat_election_detailed_result?election_year=2013')
browser.get(url)
time.sleep(5)
#select gp results option
browser.find_element_by_css_selector("input[type='radio'][value='GRAM PANCHAYAT']").click()
#select district dropdown
select_district = Select(browser.find_element_by_id('zilla_parishad'))
#getting the options
district_options = [x for x in select_district.options]
for element in district_options[1:]:
    district_value=element.get_attribute("value")
    select_district.select_by_value(district_value)
    time.sleep(5)
    select_block = Select(browser.find_element_by_id('panchayat_samity'))
    block_options = [x for x in select_block.options]
    for element in block_options[1:]:
        block_value=element.get_attribute("value")
        select_block.select_by_value(block_value)
        time.sleep(5)
        select_gp = Select(browser.find_element_by_id('gram_panchayat'))
        gp_options = [x for x in select_gp.options]
        for element in gp_options[1:]:
            gp_value=element.get_attribute("value")
            select_gp.select_by_value(gp_value)
            time.sleep(5)
            select_date = Select(browser.find_element_by_id('election_date'))
            date_options = [x for x in select_date.options]
            for element in date_options[1:]:
                date_value=element.get_attribute("value")
                # select_date.select_by_value(date_value)
                # time.sleep(5)
                # browser.find_element_by_css_selector("input[type='submit'][value='Get Result']").click()
                # time.sleep(10)
                #browser.find_element_by_css_selector('[value="Get Result"]')
                #browser.find_element_by_xpath("//input[@type='submit' and @value='Get Result']").click()
                # browser.find_element_by_xpath('//*[@title="Excel"]').click()

                item = {
                    "district_value": district_value,
                    "block_value": block_value,
                    "gp_value": gp_value,
                    "date_value": date_value
                }

                df_list.append(item)

df = pd.DataFrame(df_list)
print(df.head())
df.to_csv("/Users/suhairkilliyath/Downloads/df.csv",index=False)

#define a function to do the scraping

def get_results(district_value,block_value,gp_value,date_value):
    select_district = Select(browser.find_element_by_id('zilla_parishad'))
    time.sleep(3)
    select_district.select_by_value(str(district_value))
    time.sleep(3)
    select_block = Select(browser.find_element_by_id('panchayat_samity'))
    select_block.select_by_value(str(block_value))
    time.sleep(3)
    select_gp = Select(browser.find_element_by_id('gram_panchayat'))
    select_gp.select_by_value(str(gp_value))
    time.sleep(3)
    select_date = Select(browser.find_element_by_id('election_date'))
    select_date.select_by_value(str(date_value))
    time.sleep(5)
    browser.find_element_by_css_selector("input[type='submit'][value='Get Result']").click()
    time.sleep(5)
    browser.find_element_by_xpath('//*[@title="Excel"]').click()

# define a function to get the param values from csv

def params(df):
    #create a list representing the dataframe row
    district_value,block_value,gp_value,date_value = [row['district_value'], row['block_value'], row['gp_value'], row['date_value']]
    #row_ls = [row['district_value'], row['block_value'], row['gp_value'], row['date_value']]
    #district_value,block_value,gp_value,date_value = row_ls
    return(district_value,block_value,gp_value,date_value)

#load the csv with param values

df = pd.read_csv("/Users/suhairkilliyath/Downloads/df.csv")

# now call the functions to start the scraping
browser = webdriver.Chrome("/Users/suhairkilliyath/Downloads/chromedriver")
url = ('http://wbsec.gov.in/results/panchayat_election_detailed_result?election_year=2013')
browser.get(url)
browser.find_element_by_css_selector("input[type='radio'][value='GRAM PANCHAYAT']").click()
time.sleep(3)
for i, row in df.iterrows():
    district_value,block_value,gp_value,date_value = params(df)
    print(district_value,block_value,gp_value,date_value)
    try:
        get_results(district_value,block_value,gp_value,date_value)
    except:
        print("Not found:",district_value,block_value,gp_value,date_value)
        browser = webdriver.Chrome("/Users/suhairkilliyath/Downloads/chromedriver")
        url = ('http://wbsec.gov.in/results/panchayat_election_detailed_result?election_year=2013')
        browser.get(url)
        time.sleep(3)
        browser.find_element_by_css_selector("input[type='radio'][value='GRAM PANCHAYAT']").click()
        time.sleep(3)
