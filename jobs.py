from apscheduler.schedulers.blocking import BlockingScheduler
#from jobs.tbapi import get_hs_as

def print_data():
	print("Have a good day!")

sched = BlockingScheduler()
scheduler.add_job(print_data, 'cron', second=30)

sched.start()