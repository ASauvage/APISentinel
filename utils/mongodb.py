import pymongo


MONGO_HOST = "mongodb://localhost:27017/"


class MongoCon(pymongo.MongoClient):
    def __init__(self):
        super().__init__(MONGO_HOST)

    def save_results(self, results: list):
        self["api_tester"]["tests"].insert_many(results)
