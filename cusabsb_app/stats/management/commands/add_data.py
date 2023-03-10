from django.core.management.base import BaseCommand
from stats.utils.scrapers import get_all_teams_overall_stats
from sqlalchemy import create_engine
from datetime import datetime
import pytz

from stats.models import Batter, Pitcher, Fielder

current_date = datetime.now(pytz.timezone('US/Central')).date()
season_dates = {
        '2023':[datetime(2023, 2, 17).date(), datetime(2023, 6, 27).date()],
        '2024':[datetime(2024, 2, 16).date(), datetime(2024, 6, 25).date()],
    }

def get_search_year(date):
    for year_key in season_dates:
        if date < season_dates[year_key][0]:
            year = str(int(year_key)-1)
            return(year)
        elif date > season_dates[year_key][0] and date < season_dates[year_key][1]:
            year = year_key
            return(year)

BATTING_COLUMNS = [
    'first_name',
    'last_name',
    'number',
    'team_id',
    'avg',
    'obp',
    'slg',
    'ops',
    'ab',
    'runs',
    'hits',
    'doubles',
    'triples',
    'homeruns',
    'rbi',
    'tb',
    'bb',
    'hbp',
    'so',
    'gdp',
    'sf',
    'sh',
    'games_played',
    'games_started',
    'stolen_bases',
    'stolen_bases_attempted',
    'updated_at',
    'is_latest',
    'year',
    'team_games',
]

PITCHING_COLUMNS = [
    'first_name',
    'last_name',
    'number',
    'team_id',
    'games_appeared',
    'games_started',
    'era',
    'ip',
    'wins',
    'losses',
    'whip',
    'cg',
    'sho',
    'sv',
    'hits',
    'runs',
    'earned_runs',
    'bb',
    'so',
    'doubles',
    'triples',
    'homeruns',
    'ab',
    'b_avg',
    'wp',
    'hbp',
    'bk',
    'sfa',
    'sha',
    'updated_at',
    'is_latest',
    'year',
    'team_games',
]

FIELDING_COLUMNS = [
    'first_name',
    'last_name',
    'number',
    'team_id',
    'catches',
    'putouts',
    'assists',
    'errors',
    'fld',
    'dp',
    'sba',
    'csb',
    'pb',
    'ci',
    'updated_at',
    'is_latest',
    'year',
    'team_games',
]

def manipulate_names(df):
    first_name = []
    last_name = []
    for name in list(df['Name']):
        x = name.split(',')
        if len(x) == 2:
            first_name.append(x[1])
            last_name.append(x[0])
        else:
            first_name.append('')
            last_name.append(x[0])

    df['first_name'] = first_name
    df['last_name'] = last_name
    df = df.drop('Name',axis=1)
    
    return(df)

def manipulate_games_batting(df):
    games_played = []
    games_started = []
    for pair in list(df['GP-GS']):
        x = pair.split('-')
        games_played.append(x[0])
        games_started.append(x[1])

    df['games_played'] = games_played
    df['games_started'] = games_started
    df = df.drop('GP-GS',axis=1)

    return(df)

def manipulate_games_pitching(df):
    games_appeared = []
    games_started = []
    for pair in list(df['APP-GS']):
        x = pair.split('-')
        games_appeared.append(x[0])
        games_started.append(x[1])

    df['games_appeared'] = games_appeared
    df['games_started'] = games_started
    df = df.drop('APP-GS',axis=1)

    return(df)

def manipulate_stolen_bases(df):
    stolen_bases_attempted = []
    stolen_bases = []
    for pair in list(df['SB-ATT']):
        x = pair.split('-')
        stolen_bases_attempted.append(x[1])
        stolen_bases.append(x[0])

    df['stolen_bases_attempted'] = stolen_bases_attempted
    df['stolen_bases'] = stolen_bases
    df = df.drop('SB-ATT',axis=1)

    return(df)

def manipulate_wins_losses(df):
    wins = []
    losses = []
    for pair in list(df['W-L']):
        x = pair.split('-')
        wins.append(x[1])
        losses.append(x[0])

    df['wins'] = wins
    df['losses'] = losses
    df = df.drop('W-L',axis=1)

    return(df)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('stat_year', type=str, nargs='?', default=get_search_year(current_date))

    def handle(self, *args, **options):
        stat_year = options.get('stat_year', None)
        print('Running the add_data management command...')
        print('Getting stats for '+stat_year+'...')

        '''Bring in the latest stats from each team's website.'''
        try:
            batting_stats,pitching_stats,fielding_stats = get_all_teams_overall_stats(stat_year)
            
            print('Manipulating the dataframes...')
            '''Add a datetime field to each dataframe documenting the time it was updated.'''
            batting_stats['updated_at'] = datetime.now(pytz.timezone('US/Central'))
            pitching_stats['updated_at'] = datetime.now(pytz.timezone('US/Central'))
            fielding_stats['updated_at'] = datetime.now(pytz.timezone('US/Central'))

            '''Add is_latest boolean field to each dataframe.'''
            batting_stats['is_latest'] = True
            pitching_stats['is_latest'] = True
            fielding_stats['is_latest'] = True

            '''Split first and last names into separate columns.'''
            batting_stats = manipulate_names(batting_stats)
            pitching_stats = manipulate_names(pitching_stats)
            fielding_stats = manipulate_names(fielding_stats)

            '''Remove any columns with no first name.'''
            batting_stats = batting_stats[batting_stats['first_name'] != '']
            pitching_stats = pitching_stats[pitching_stats['first_name'] != '']
            fielding_stats = fielding_stats[fielding_stats['first_name'] != '']

            '''Split games played and games started into separate columns.'''
            batting_stats = manipulate_games_batting(batting_stats)
            pitching_stats = manipulate_games_pitching(pitching_stats)

            '''Split stolen bases and attempted stolen bases into separate columns.'''
            batting_stats = manipulate_stolen_bases(batting_stats)

            '''Split pitcher wins and losses into separate columns.'''
            pitching_stats = manipulate_wins_losses(pitching_stats)

            '''Make all column names lowercase.'''
            batting_stats.columns = batting_stats.columns.str.lower()
            pitching_stats.columns = pitching_stats.columns.str.lower()
            fielding_stats.columns = fielding_stats.columns.str.lower()

            '''Rename columns to match model field names.'''
            batting_stats.rename({'slg%':'slg','ob%':'obp','r':'runs','h':'hits','2b':'doubles','3b':'triples','hr':'homeruns'}, axis=1, inplace=True)
            pitching_stats.rename({'b/avg':'b_avg','r':'runs','er':'earned_runs','h':'hits','2b':'doubles','3b':'triples','hr':'homeruns'}, axis=1, inplace=True)
            fielding_stats.rename({'fld%':'fld','c':'catches','po':'putouts','a':'assists','e':'errors'}, axis=1, inplace=True)

            '''Reorder the columns.'''
            batting_stats = batting_stats.reindex(columns=BATTING_COLUMNS)
            pitching_stats = pitching_stats.reindex(columns=PITCHING_COLUMNS)
            fielding_stats = fielding_stats.reindex(columns=FIELDING_COLUMNS)

            print('Uploading the data to the database...')

            '''Change all existing is_latest fields to False.'''
            Batter.objects.all().filter(year=stat_year).update(is_latest=False)
            Pitcher.objects.all().filter(year=stat_year).update(is_latest=False)
            Fielder.objects.all().filter(year=stat_year).update(is_latest=False)

            '''Set up the SQLite create engine.'''
            engine = create_engine('sqlite:///db.sqlite3')

            '''Upload the data to the SQLite database.'''
            batting_stats.to_sql(Batter._meta.db_table, if_exists='append', con=engine, index=False)
            pitching_stats.to_sql(Pitcher._meta.db_table, if_exists='append', con=engine, index=False)
            fielding_stats.to_sql(Fielder._meta.db_table, if_exists='append', con=engine, index=False)

            print('\033[92m\033[1mAll stats successfully updated!\033[0m')
        except TypeError:
            print('\033[93m\033[1mStats could not be updated at this time. Please try again later.\033[0m')
