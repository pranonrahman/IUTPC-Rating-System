import cx_Oracle as Cx

class database:
    def __init__(self):
        self.conn = Cx.connect('iutpc/iutpcadmin@localhost/orcl')
        self.cur = self.conn.cursor()
    def getCur(self):
        return self.cur


