import time
import schedule

from apps.event import jobs


schedule.every(5).minutes.do(jobs.sync_event_data)

while True:
    schedule.run_pending()
    time.sleep(1)
