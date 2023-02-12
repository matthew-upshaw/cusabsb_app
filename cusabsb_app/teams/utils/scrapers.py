import requests
import time
import json
import re
import pandas as pd
from bs4 import BeautifulSoup as bs

def get_team_records(year):
    try:
        page = requests.get(f'https://d1baseball.com/conference/conference-usa/{year}')
        print(f'\033[92m\033[1mSuccessfully connected to https://d1baseball.com/conference/conference-usa/{year}\033[0m')
    except requests.exceptions.ConnectionError:
        print(f'\033[91m\033[1mCould not connect to https://d1baseball.com/conference/conference-usa/{year}\033[0m')
        return None
    
    soup = bs(page.content, 'html.parser')

    if soup is not None:
        success = True
        target_table = soup.findAll('table')[0]
        table_rows = target_table.find_all('tr')

        res = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text.strip() for tr in td if tr.text.strip()]
            if row:
                res.append(row)
    
        df_temp = pd.DataFrame(res)

    else:
        success = False

    if success:
        return(df_temp)
