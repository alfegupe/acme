from pymongo import MongoClient
from env_vars import MONGO_URI


class BalanceManager:

    def __init__(self):
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        self.balance_collection = db['balance']

    def count_balances(self):
        return self.balance_collection.count()

    def insert_one(self, balance):
        return self.balance_collection.insert_one(balance)

    def insert_many(self, balances):
        return self.balance_collection.insert_many(balances)

    def validate_balance_account(self, user_id, pin):
        return self.balance_collection.find_one({'user_id': user_id, 'pin': pin})

    def get_by_user_id(self, user_id):
        return self.balance_collection.find_one({'user_id': user_id})

    def get_balance_amount(self, user_id):
        balance = self.get_by_user_id(user_id)
        return balance['balance'] if balance else None

    def clear_collection(self):
        return self.balance_collection.remove()
