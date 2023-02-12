from django.core.management.base import BaseCommand
from teams.utils.scrapers import get_team_records
from sqlalchemy import create_engine
import pandas as pd

from stats.management.commands.add_data import current_date, season_dates, get_search_year

from teams.models import Team, Record

def manipulate_record(df):
    wins = []
    losses = []
    ties = []

    for record in list(df):
        x = record.split('-')
        if len(x) < 3:
            ties.append('0')
        else:
            ties.append(x[2])
        wins.append(x[0])
        losses.append(x[1])

    return(wins, losses, ties)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('stat_year', type=str, nargs='?', default=get_search_year(current_date))

    def handle(self, *args, **options):
        stat_year = options.get('stat_year', None)

        print('Running the update_records management command...')
        print('Getting team records for '+stat_year+'...')

        try:
            records = get_team_records(stat_year)
            
            print('Manipulating the dataframes...')

            column_names = records.iloc[0]
            records  = pd.DataFrame(records.values[1:], columns=column_names)

            wins_overall,losses_overall,ties_overall = manipulate_record(records['Overall'])
            wins_conf,losses_conf,ties_conf = manipulate_record(records['Record'])

            records['wins_overall'] = [int(i) for i in wins_overall]
            records['losses_overall'] = [int(i) for i in losses_overall]
            records['ties_overall'] = [int(i) for i in ties_overall]

            records['wins_conf'] = [int(i) for i in wins_conf]
            records['losses_conf'] = [int(i) for i in losses_conf]
            records['ties_conf'] = [int(i) for i in ties_conf]

            records['year'] = stat_year

            team_id = []
            for x in list(records['Team']):
                for team in Team.objects.all():
                    if x == team.name:
                        team_id.append(team.id)

            records['team_id'] = team_id

            records = records.drop(['Team','Record','Win %','GB','Overall','Overall %','Streak'], axis=1)

            print('Uploading the data to the database...')

            '''Set up the SQLite create engine.'''
            engine = create_engine('sqlite:///db.sqlite3')

            Record.objects.filter(year=stat_year).delete()

            records.to_sql(Record._meta.db_table, if_exists='append', con=engine, index=False)

            print('\033[92m\033[1mAll team records successfully updated!\033[0m')
        except TypeError:
            print('\033[93m\033[1mRecords could not be updated at this time. Please try again later.\033[0m')
            