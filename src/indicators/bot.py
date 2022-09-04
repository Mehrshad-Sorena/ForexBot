from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from trader import trader_task
from macd_Trader import trader_task_macd_div
from forex_news import news_task
import threading
import schedule
import time

try:
    import asyncio
except ImportError:
    import trollius as asyncio

scheduler_trader_macd_div = AsyncIOScheduler()
scheduler_news = AsyncIOScheduler()

def trader_threaded():
    job_thread = threading.Thread(target=trader_task)
    job_thread.start()
    job_thread.join()

def trader_macd_div_threaded():
    job_thread = threading.Thread(target=trader_task_macd_div, args = ['XAUUSD_i', 'mohipc'])
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
days = 'sat,sun,mon,tue,wed,thu,fri'

minute_news = '10'
hour_news = '00,12'

trader_macd_div_threaded()
#news_task()

#scheduler_trader.add_job(func=trader_threaded, trigger='cron', day_of_week='mon-fri', hour='00-23', minute=minute_trader, timezone='UTC')
scheduler_trader_macd_div.add_job(func=trader_macd_div_threaded, trigger='cron', day_of_week=days, hour='00-23', minute=minute_trader, timezone='UTC')
#scheduler_news.add_job(func=news_threaded, trigger='cron', day_of_week='mon-fri', hour=hour_news, minute=minute_news, timezone='UTC')
# Start the scheduler
scheduler_trader_macd_div.start()
#scheduler_news.start()

try:
	asyncio.get_event_loop().run_forever()
except (KeyboardInterrupt, SystemExit):
	pass