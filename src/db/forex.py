from pymongo import MongoClient
from src.config import mongoConfig
from src.utils import logs


class ForexMongo(object):
    params = mongoConfig()
    host = params.get('hostname')
    port = int(params.get('port'))
    dbname = 'forex'
    username = params.get('username')
    password = params.get('password')

    def __init__(self):
        try:
            self.client = MongoClient(
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password)
            self.db = self.client[self.dbname]
            self.queue = self.db['queue']
        except Exception as ex:
            logs('warning', ex)
