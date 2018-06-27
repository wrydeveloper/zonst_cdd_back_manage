import time
import schedule

from apps.analysis import jobs


schedule.every().day.at("0:10").do(jobs.channel_data_analysis)
schedule.every().day.at("0:30").do(jobs.number_bet_data_analysis)
schedule.every().day.at("0:50").do(jobs.sports_bet_data_analysis)
schedule.every().day.at("1:10").do(jobs.pay_data_analysis)
schedule.every().day.at("1:30").do(jobs.user_data_analysis)
schedule.every().day.at("1:50").do(jobs.proxy_data_analysis)

while True:
    schedule.run_pending()
    time.sleep(1)
