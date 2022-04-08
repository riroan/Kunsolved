import pymysql
from secret import SECRET


class Database:
    def __init__(self):
        self.db = pymysql.connect(host=SECRET.host, user=SECRET.user,
                                  password=SECRET.password, db=SECRET.db, charset=SECRET.charset)
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    def __del__(self):
        self.db.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
