# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 18:09:49 2021

@author: Ng Wai Ching and fed
v2: scrapes every day and stores in a dataframe
to do:  count days instead of hardcored the i = 20
"""

from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import os
import csv
import pandas as pd
import matplotlib as plt


scrap_date_format = "%B %d, %Y"
save_date_format = "%d %b %Y"

# getting the latest issue text
fda_domain = "https://fsapps.fiscal.treasury.gov" 

fda_issues_link = f"{fda_domain}/dts/issues"

r = requests.get(fda_issues_link)

html_soup = BeautifulSoup(r.text, features="html.parser")

main_soup = html_soup.find("main")

latest_fy_soup = main_soup.find_all("h-box")[2]

latest_quarter_soup = latest_fy_soup.select('div[data-margin^="top-small"]')[-1] 

dates = []# pd.Series()
treas_account = []#pd.Series()
 
 
for i in range(20):
    latest_issue_soup = latest_quarter_soup.select('ul[data-margin^="top-small"]')[i] #latest issue date found: 29 Mar 2021
    #1019013
    
    
    latest_issue_date = latest_issue_soup.find("span").text
    latest_issue_date = datetime.strptime(latest_issue_date, scrap_date_format)
    
    print(f"latest issue date found: {latest_issue_date.strftime(save_date_format)}")
    dates.append(latest_issue_date)
    
    
    # check_latest_scrapped(csv_filepath, latest_issue_date)
    
    # text is middle
    latest_issue_text_link_path = latest_issue_soup.find_all("a")[1]["href"]
    
    latest_issue_text_link = f"{fda_domain}/{latest_issue_text_link_path}"
    
    latest_issue_text = requests.get(latest_issue_text_link).text
    
    keyword = "Federal Reserve Account"
    
    # extracting the values of the `keyword` from latest_issue_text as string
    # e.g. $  1,089,501 $  1,361,274 $  1,414,465 $   1,781,679'
    
    start = latest_issue_text.find(keyword) + len(keyword)
    end = latest_issue_text.find("\n", start)
    values = latest_issue_text[start:end].strip()
    
    # Removes excess space from the extracted string
    account_value = values[: values.find(" $  ")]
    account_value = re.sub("[^0-9]", "", account_value)
    
    print(account_value)
    treas_account.append(account_value)



container = pd.DataFrame({'dates':  dates,
                          'treasury_account':  treas_account})
container.set_index('dates', inplace = True)
    
container.sort_values('dates', inplace = True)

container['treasury_account'] = pd.to_numeric(container['treasury_account'])
container.plot()#container['treasury_account'].plot()
