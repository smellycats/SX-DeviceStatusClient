import sqlite3


class KakouDB(object):
    def __init__(self):
        self.conn = sqlite3.connect('kakou.db')
        #print "Opened database successfully";

    def __del__(self):
        self.conn.close()

    def get_device_by_ip(self, ip):
        sql = "SELECT * FROM DEVICE WHERE ip='{0}'".format(ip)
        r = self.conn.execute(sql)
        return r.fetchone()

    def get_device(self, banned=0):
        sql = "SELECT * FROM DEVICE WHERE banned={0}".format(banned)
        r = self.conn.execute(sql)
        return r.fetchall()

if __name__ == "__main__":
    s = KakouDB()
    ip = "10.47.202.30"
    print s.get_device_by_ip(ip)
    print s.get_device(banned=0)
    #s.del_idflag(1)
