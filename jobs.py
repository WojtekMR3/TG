from apscheduler.schedulers.blocking import BlockingScheduler
from helper import your_function_a, your_function_b

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes='30')
def print_data():
	print("Have a good day!")

sched.start()