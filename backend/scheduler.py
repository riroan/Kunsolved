from utility import Utility
import schedule
import time

util = Utility(True)

# schedule.every().monday.at("05:00").do(util.updateAllUserSolved) # 모든 유저 풀이 정보 업데이트 (대회 풀이 목적)
schedule.every().day.at("05:00").do(util.updateAllUserSolved)
schedule.every(5).minutes.do(util.addRecentSolved)               # 최근 해결 내역 업데이트
schedule.every().day.at("03:00").do(util.getProblemInfo)         # 새로운 문제 업데이트
schedule.every().day.at("02:00").do(util.updateSchoolUser)       # 새로운 유저 업데이트
while True:
    schedule.run_pending()
    time.sleep(1)