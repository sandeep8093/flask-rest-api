from pymongo import MongoClient

class ConnectDB:
    def __init__(self):
        self.connection = None
        self.collection = None

    def connect_db(self,  db='', collection=''):   # Fetchs the MongoDB, by making use of Request Body
        connection = MongoClient("mongodb+srv://root:root@cluster0.omm8pms.mongodb.net/?retryWrites=true&w=majority")
        return connection