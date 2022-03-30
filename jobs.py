from apscheduler.schedulers.blocking import BlockingScheduler
#from jobs.tbapi import get_hs_as

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes='30')
def print_data():
	print("Have a good day!")

sched.start()