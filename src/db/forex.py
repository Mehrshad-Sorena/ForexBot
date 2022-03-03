from src.config import mongoConfig
from pymongo import MongoClient
from datetime import datetime
from src.utils import logs
from uuid import uuid4


class ForexMongo(object):
    params = mongoConfig()
    host = params.get('hostname')
    port = int(params.get('port'))
    dbname = 'forex'
    collection_name = 'forex'
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
            self.forex = self.db[self.collection_name]
        except Exception as ex:
            logs('warning', ex)

    def create(self, data):
        job_id = str(uuid4())
        created_time = datetime.now()
        status = 'CREATED'
        values = {
                'job_id': job_id,
                'created_time': created_time,
                'status': status,
                'data': data
            }
        self.forex.insert_one(values)
        return job_id

    def setData(self, job_id, data):
        key = {'job_id': job_id}
        values = {
                '$push': {
                    'data': data
                }}
        self.forex.update_one(key, values)

    def getData(self, job_id):
        key = {'job_id': job_id}
        filters = {'_id': 0, 'data': 1}

        return self.forex.find_one(key, filters)
