from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import job_remove_temp, job_cancel_proforma

def start_jobs():
    scheduler = BackgroundScheduler()
    
    #Set cron to runs every 1 min.
    
    #Add our task to scheduler.
    # cron_job = {'month': '*', 'day': '*', 'hour': '*/6', 'minute':'*'}
    # scheduler.add_job(job_remove_temp, 'cron', **cron_job)
    
    # cron_job = {'month': '*', 'day': '*/1', 'hour': '*', 'minute':'*'}
    # scheduler.add_job(job_cancel_proforma, 'cron', **cron_job)
    scheduler.add_job(job_cancel_proforma, 'cron', hour=12)
    scheduler.add_job(job_remove_temp, 'cron', hour=12)
#And finally start.    
    scheduler.start()