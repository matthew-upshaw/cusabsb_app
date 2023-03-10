import requests
import time
import json
import re
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from django.conf import settings
from django.db.models import Prefetch

from teams.models import Team

BATTING_COLUMNS = [
        'Name',
        'Number',
        'AVG',
        'OPS',
        'GP-GS',
        'AB',
        'R',
        'H',
        '2B',
        '3B',
        'HR',
        'RBI',
        'TB',
        'SLG%',
        'BB',
        'HBP',
        'SO',
        'GDP',
        'OB%',
        'SF',
        'SH',
        'SB-ATT',
    ]

PITCHING_COLUMNS = [
        'Name',
        'Number',
        'ERA',
        'WHIP',
        'W-L',
        'APP-GS',
        'CG',
        'SHO',
        'SV',
        'IP',
        'H',
        'R',
        'ER',
        'BB',
        'SO',
        '2B',
        '3B',
        'HR',
        'AB',
        'B/AVG',
        'WP',
        'HBP',
        'BK',
        'SFA',
        'SHA',
    ]


FIELDING_COLUMNS = [
        'Name',
        'Number',
        'C',
        'PO',
        'A',
        'E',
        'FLD%',
        'DP',
        'SBA',
        'CSB',
        'PB',
        'CI',
    ]

regex = "\d{4}"

def find_table(soup,text_match):
    for count, table in enumerate(soup.findAll('table')):
        if type(soup.findAll('table')[count].findAll('caption')) != None:
            for caption in soup.findAll('table')[count].findAll('caption'):
                if type(caption.string) != None:
                    if text_match in caption.string:
                        target_table = soup.findAll('table')[count]
                        return(target_table)

def get_team_stats(team,year=""):
    """
    Return a BeatifulSoup object for selected team and year cumulative stats
    """
    try:
        page = requests.get(f'{team.bsb_page}/stats/{year}')
        print(f'\033[92m\033[1mSuccessfully connected to {team.bsb_page}/stats/{year}\033[0m')
    except requests.exceptions.ConnectionError:
        print(f'\033[91m\033[1mCould not connect to {team.bsb_page}/stats/{year}\033[0m')
        return None

    soup = bs(page.content, "html.parser")

    return(soup)

def get_team_stats_sel(team,year=""):
    """
    Return a BeautifulSoup object for selected team and year cumulative stats when selenium is required
    """
    try:
        options = Options()
        options.headless = True
        options.add_argument('--window-size=1920,1200')

        driver = webdriver.Chrome(options=options, executable_path=settings.DRIVER_PATH)
        page = f'{team.bsb_page}/stats/{year}'
        driver.get(page)
        print(f'\033[92m\033[1mSuccessfully connected to {team.bsb_page}/stats/{year}\033[0m')

        buttons = driver.find_elements(By.TAG_NAME,'button')
        for button in buttons:
            if button.text == 'Pitching' or button.text == 'Fielding':
                button.click()

        time.sleep(20)

        page_source = driver.page_source
        soup = bs(page_source,'lxml')

        driver.quit()
    except WebDriverException:
        print(f'\033[91m\033[1mCould not connect to {team.bsb_page}/stats/{year}\033[0m')
        return None

    return(soup)

def get_overall_batting_stats(soup):
    """
    Return a pandas dataframe containing a team's overall batting stats
    """
    text_match = 'Individual Overall Batting Statistics'
    target_table = find_table(soup,text_match)
    table_rows = target_table.find_all('tr')

    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        a = tr.find_all('a')
        row = [tr.text.strip() for tr in a if tr.text.strip()]+[tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)
    
    df_temp = pd.DataFrame(res)
    df = df_temp.drop(df_temp.tail(2).index).drop(1,axis=1).drop(23,axis=1)
    df.columns = BATTING_COLUMNS

    for tag in soup.findAll('h1'):
        if re.match(regex, tag.string):
            year = re.findall(regex, tag.string)[0]

    if 'year' not in locals():
        for tag in soup.findAll('title'):
            if re.match(regex, tag.string):
                year = re.findall(regex, tag.string)[0]

    df['year'] = year

    return(df)

def get_overall_pitching_stats(soup):
    """
    Return a pandas dataframe containing a team's overall pitching stats
    """
    text_match = 'Individual Overall Pitching Statistics'
    target_table = find_table(soup,text_match)
    table_rows = target_table.find_all('tr')

    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        a = tr.find_all('a')
        row = [tr.text.strip() for tr in a if tr.text.strip()]+[tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)
    
    df_temp = pd.DataFrame(res)
    df = df_temp.drop(df_temp.tail(2).index).drop(1,axis=1).drop(26,axis=1)
    df.columns = PITCHING_COLUMNS

    for tag in soup.findAll('h1'):
        if re.match(regex, tag.string):
            year = re.findall(regex, tag.string)[0]

    if 'year' not in locals():
        for tag in soup.findAll('title'):
            if re.match(regex, tag.string):
                year = re.findall(regex, tag.string)[0]

    df['year'] = year

    return(df)

def get_overall_fielding_stats(soup):
    """
    Return a pandas dataframe containing a team's overall fielding stats
    """
    text_match = 'Individual Overall Fielding Statistics'
    target_table = find_table(soup,text_match)
    table_rows = target_table.find_all('tr')

    res = []
    for tr in table_rows:
        td = tr.find_all('td')
        a = tr.find_all('a')
        row = [tr.text.strip() for tr in a if tr.text.strip()]+[tr.text.strip() for tr in td if tr.text.strip()]
        if row:
            res.append(row)
    
    df_temp = pd.DataFrame(res)
    df = df_temp.drop(df_temp.tail(2).index).drop(1,axis=1).drop(13,axis=1)
    df.columns = FIELDING_COLUMNS

    for tag in soup.findAll('h1'):
        if re.match(regex, tag.string):
            year = re.findall(regex, tag.string)[0]

    if 'year' not in locals():
        for tag in soup.findAll('title'):
            if re.match(regex, tag.string):
                year = re.findall(regex, tag.string)[0]

    df['year'] = year

    return(df)

def get_all_teams_overall_stats(year):
    SEL_REQUIRED = [
        'MAR',
        'UAB',
        'WKU',
    ]
    
    batting_stats = pd.DataFrame(columns=BATTING_COLUMNS)
    pitching_stats = pd.DataFrame(columns=PITCHING_COLUMNS)
    fielding_stats = pd.DataFrame(columns=FIELDING_COLUMNS)

    for team in list(Team.objects.all()):
        if year >= team.year_joined and year <= team.year_left:
            print('Collecting stats for '+team.abbreviation+'...')

            if team.abbreviation not in SEL_REQUIRED:
                soup = get_team_stats(team,year)
            else:
                soup = get_team_stats_sel(team,year)

            if soup is not None:
                success = True

                record = Team.objects.all().prefetch_related(Prefetch('record_set')).filter(id=team.id)[0].record_set.filter(year=year)[0]
                team_games = record.wins_overall+record.losses_overall+record.ties_overall

                temp_batting_df = get_overall_batting_stats(soup)
                temp_pitching_df = get_overall_pitching_stats(soup)
                temp_fielding_df = get_overall_fielding_stats(soup)

                temp_batting_df['team_id']=team.id
                temp_pitching_df['team_id']=team.id
                temp_fielding_df['team_id']=team.id

                temp_batting_df['team_games']=team_games
                temp_pitching_df['team_games']=team_games
                temp_fielding_df['team_games']=team_games

                batting_stats = pd.concat([batting_stats,temp_batting_df])
                pitching_stats = pd.concat([pitching_stats,temp_pitching_df])
                fielding_stats = pd.concat([fielding_stats,temp_fielding_df])
            else:
                success = False
    
    if success:
        return((batting_stats.reset_index(drop=True),pitching_stats.reset_index(drop=True),fielding_stats.reset_index(drop=True)))
        