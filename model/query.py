import MySQLdb

class Query(object):

    def __init__(self):
        self.count = 1
        self.conn = MySQLdb.connect(
            host='182.92.11.96',
            port=3306,
            passwd='newpassd',
            db='epubreadeer',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def get_book_by_bid(self, bid):
        sql = ''
        sql += str('SELECT * FROM BOOK WHERE BID=\'' + bid + '\'')
        print "sql:", sql
        self.cur.execute(sql)
        data = self.cur.fetchone()
        print "Database version: %s" % data
        return data
