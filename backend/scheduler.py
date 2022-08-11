from utility import Utility
import schedule
import time

util = Utility(True)

schedule.every().monday.at("05:00").do(util.updateAllUserSolved) # 매주 월요일 5시에 모든 유저 풀이 정보 업데이트 (대회 풀이 목적)
schedule.every(5).minutes.do(util.getRecentSolved)               # 5분마다 최근 해결 내역 업데이트
schedule.every().day.at("03:00").do(util.getProblemInfo)         # 매일 오전 3시마다 새로운 문제 업데이트
schedule.every().day.at("02:00").do(util.updateSchoolUser)       # 매일 오전 2시마다 새로운 유저 업데이트
while True:
    schedule.run_pending()
    time.sleep(1)