from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pullFromBloombergAPI import bloombergAPI

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(bloombergAPI.update_articles, 'interval', hours=1)
    scheduler.start()
    print(bloombergAPI.update_articles())