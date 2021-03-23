from pymongo import MongoClient
from env_vars import MONGO_URI


class StepManager:

    def __init__(self):
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        self.step_collection = db['step']

    def count_steps(self):
        return self.step_collection.count()

    def insert_one(self, step):
        return self.step_collection.insert_one(step)

    def insert_many(self, steps):
        return self.step_collection.insert_many(steps)

    def get_by_id(self, step_id):
        return self.step_collection.find_one({'id': step_id})

    def clear_collection(self):
        return self.step_collection.remove()
