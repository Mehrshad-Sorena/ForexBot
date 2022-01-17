import time
import os
from datetime import date
import datetime

def time_func():
	hour = 0
	minute = 0
	second = 0
	x = datetime.datetime.now()

	time_now = (x.hour*60) + x.minute
	alpari_time = time_now - ((2 * 60) + 30)
	#print(int(alpari_time/60),':',alpari_time%60,':',x.second)
	hour = int(alpari_time/60)
	minute = alpari_time%60
	second = x.second

	return x.hour,x.minute,x.second,x.strftime("%A")

