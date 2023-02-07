from django.core.management import call_command
import datetime
import pytz

def update_db():
    print('~'*50+'\n'+str(datetime.datetime.now(pytz.timezone('US/Central')))+'\nRunning the update_db cron job...')
    call_command('add_data')