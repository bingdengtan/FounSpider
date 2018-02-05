from pymongo import MongoClient

settings = {
    "ip": '127.0.0.1',
    'port': 27017,
    'db_name': 'foundation'
}

class DB(object):
    def __init__(self, col):
        try:
            self.conn = MongoClient(settings["ip"],settings["port"])
        except Exception as e:
            print(e)
        self.db = self.conn[settings["db_name"]]
        self.col = self.db[col]

    def insert(self, dic):
        self.col.insert(dic)

    def update(self, dic, newdic):
        self.col.update(dic, newdic)

    def delete(self, dic):
        self.col.remove(dic)

    def find(self, dic):
        return self.col.find(dic)