from django.core.management import call_command
from datetime import datetime
import pytz
from cusabsb_app.stats.management.commands.add_data import current_date, season_dates

def update_db():
    in_season = False
    print('~'*100+'\n'+str(datetime.now(pytz.timezone('US/Central')))+'\nRunning the update_db cron job...')
    for year_key in season_dates:
        print('Checking to see if '+year_key+' season is ongoing...')
        if current_date > season_dates[year_key][0] and current_date < season_dates[year_key][1]:
            print(year_key+' season is ongoing!')
            in_season=True
            break
        else:
            print(year_key+' season is not ongoing.')

    if in_season:
        call_command('update_records')
        call_command('add_data')
        pass
    else:
        print('No season is currently active. The database will not be updated.')

    print('~'*100+'\n')
