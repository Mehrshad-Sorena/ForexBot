from apscheduler.schedulers.asyncio import AsyncIOScheduler
from trader import trader_task
from forex_news import news_task
import threading
import schedule
import time

try:
    import asyncio
except ImportError:
    import trollius as asyncio

scheduler_trader = AsyncIOScheduler()
scheduler_news = AsyncIOScheduler()

def trader_threaded():
    job_thread = threading.Thread(target=trader_task)
    job_thread.start()
    job_thread.join()

def news_threaded():
	job_thread = threading.Thread(target=news_task)
	job_thread.start()
	job_thread.join()

#schedule.every(1).minutes.do(run_threaded, trader_task)
#schedule.every(60).minutes.at(":00").do(run_threaded, news)

# Schedules the job_function to be executed Monday through Friday at between 12-16 at specific times. 
minute_trader = '0,5,10,15,20,25,30,35,40,45,50,55'
minute_news = '0'
scheduler_trader.add_job(func=trader_threaded, trigger='cron', day_of_week='mon-fri', hour='00-23', minute=minute_trader, timezone='UTC')
scheduler_news.add_job(func=news_threaded, trigger='cron', day_of_week='mon-fri', hour='00-23', minute=minute_news, timezone='UTC')
# Start the scheduler
scheduler_trader.start()
scheduler_news.start()

try:
	asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
	pass