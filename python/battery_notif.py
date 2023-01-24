import psutil
from plyer import notification
import time
# from psutil we will import the
# sensors_battery class and with
# that we have the battery remaining
while(True):
	battery = psutil.sensors_battery()
	percent = battery.percent
	
	notification.notify(
		title="Battery Percentage",
		message=str(percent)+"% Battery remaining",
		timeout=10
	)
	
	# after every 60 mins it will show the
	# battery percentage
	time.sleep(60*60)
	
	continue
