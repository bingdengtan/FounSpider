from pymongo import MongoClient

settings = {
    "ip": '127.0.0.1',
    'port': 27017,
    'db_name': 'foundation'
}

global db
db = None

class DB(object):
    def __init__(self, col):
        if db is None:
            try:
                self.conn = MongoClient(settings["ip"],settings["port"])
            except Exception as e:
                print(e)
            cur_db = self.conn[settings["db_name"]]
            self.db = cur_db
        self.col = self.db[col]

    def insert(self, dic):
        self.col.insert(dic)

    def update(self, dic, newdic):
        self.col.update(dic, newdic)

    def delete(self, dic):
        self.col.remove(dic)

    def find(self, dic):
        return self.col.find(dic,no_cursor_timeout = True)

    def close(self):
        self.conn.close();