from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import job_remove_temp

def start_jobs():
    scheduler = BackgroundScheduler()
    
    #Set cron to runs every 1 min.
    cron_job = {'month': '*', 'day': '*', 'hour': '*/6', 'minute':'*'}
    
    #Add our task to scheduler.
    scheduler.add_job(job_remove_temp, 'cron', **cron_job)
#And finally start.    
    scheduler.start()