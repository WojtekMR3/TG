from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import schedule_api
from .tbapi import get_hs_as

def start():
  scheduler = BackgroundScheduler()
  #scheduler.add_job(schedule_api, 'cron', second=0)
  #scheduler.add_job(get_hs_as, 'cron', second=5)
  #scheduler.add_job(get_hs_as, 'cron', minute=50)
  scheduler.add_job(get_hs_as, 'cron', hour=16)
  scheduler.start()