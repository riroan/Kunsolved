from utility import Utility
import schedule
import time

util = Utility(True)
print("Scheduling start")
# schedule.every().monday.at("05:00").do(util.updateAllUserSolved) # 모든 유저 풀이 정보 업데이트 (대회 풀이 목적)
schedule.every().day.at("05:00").do(util.update_all_user_solved)
schedule.every(5).minutes.do(
    util.add_recent_solved)               # 최근 해결 내역 업데이트
schedule.every().day.at("03:00").do(util.get_problem_info)         # 새로운 문제 업데이트
schedule.every().day.at("02:00").do(util.update_school_user)       # 새로운 유저 업데이트
while True:
    schedule.run_pending()
    time.sleep(1)
