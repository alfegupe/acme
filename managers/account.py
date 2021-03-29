from pymongo import MongoClient
from env_vars import MONGO_URI

from utils.trm import get_trm


class AccountBalanceManager:

    def __init__(self):
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        self.account_collection = db['account_balance']

    def create_account(self, user_id, pin):
        """
        Creates a new account with default information.
        :param user_id: str, the id of the account owner.
        :param pin: int, the secure account pin.
        :return: dict, the inserted account information.
        """
        new_account = {
            'balance': 250000,
            'is_valid': True,
            'pin': pin,
            'user_id': user_id,
        }
        return self.account_collection.insert_one(new_account)

    def validate_account(self, params):
        """
        Check if an account is valid or not.
        :param params: dict, the account information.
        :return: bool, the validation result.
        """
        account = self.account_collection.find_one(params)
        return account.get('is_valid', False)

    def get_account_balance(self, params):
        """
        Get the account balance.
        :param params: dict, the account information.
        :return: number, the account balance.
        """
        account = self.account_collection.find_one(params)
        return account.get('balance', 0) if account else None

    def _set_balance(self, user_id, new_balance):
        """
        Set a new balance value for the user id given.
        :param user_id: str, the user id to filter.
        :param balance: number, the new balance amount.
        """
        self.account_collection.update_one(
            filter={'user_id': user_id},
            update={'$set': {'balance': new_balance}}
        )

    def withdraw_in_dollars(self, params):
        """
        Withdraw from the account in dollars.
        :param params: dict, the transaction information.
        :return: number, the new account balance.
        """
        trm = get_trm()
        account = self.account_collection.find_one({'user_id': params.get('user_id')})
        if account:
            withdraw_amount = trm * params.get('money', 0)
            new_balance = account.get('balance', 0) - withdraw_amount
            self._set_balance(
                user_id=params.get('user_id'),
                new_balance=new_balance
            )
            return True
        return False

    def deposit_money(self, params):
        """
        Make a deposit to the account.
        :param params: dict, the user id and the money to deposit.
        :return: bool, transaction result
        """
        account = self.account_collection.find_one({'user_id': params.get('user_id')})
        if account:
            new_balance = account.get('balance', 0) + params.get('money', 0)
            self._set_balance(
                user_id=params.get('user_id'),
                new_balance=new_balance
            )
            return True
        return False

    def clear_collection(self):
        """
        Delete all rows from collection
        """
        return self.account_collection.remove()
