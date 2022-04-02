from utility import Utility
import schedule
import time

util = Utility(True)

schedule.every().monday.at("05:00").do(util.updateAllUserSolved)
while True:
    schedule.run_pending()
    time.sleep(1)