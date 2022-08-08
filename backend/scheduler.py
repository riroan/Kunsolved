from utility import Utility
import schedule
import time

util = Utility(True)

schedule.every().monday.at("05:00").do(util.updateAllUserSolved)
schedule.every(5).minutes.do(util.getRecentSolved)
schedule.every().day.at("03:00").do(util.getProblemInfo)
schedule.every().day.at("02:00").do(util.updateSchoolUser)
while True:
    schedule.run_pending()
    time.sleep(1)