import json
import time
from threading import Thread
from queue import Queue

from eospy.keys import EOSKey
from api.api import Api

from transact import send_transaction



class Account:
    def __init__(self, api, cleos, private_key):
        self.api = api
        self.cleos = cleos
        self.private_key = private_key
        self.key = EOSKey(private_key)
        self.public_key = self.key.to_public()
        self.name = api.get_account(self.public_key)["account"]["account_name"]

        self.assets = None


    def __repr__(self):
        return self.name

    @staticmethod
    def load_accounts(api, cleos, accounts_file):
        accounts = list()
        with open(accounts_file, "r", encoding="UTF-8") as private_keys_file:
            private_keys = json.loads(private_keys_file.read())["private_keys"]
            for key in private_keys:
                accounts.append(Account(api, cleos, key))

        return accounts


    """ Get info """
    def get_drop_balance(self, contract_account):
        data = self.cleos.get_table(code=contract_account,
                                    scope=contract_account,
                                    table="balances",
                                    lower_bound=self.name,
                                    upper_bound=self.name)
        if data["rows"]:
            return float(data["rows"][0]["quantities"][0].split(" ")[0])
        else:
            return 0

    @property
    def full_data(self):
        data = self.api.get_account(self.name)
        data["atomic_drop_balance"] = self.get_drop_balance("atomicdropsx")
        data["nefty_drop_balance"] = self.get_drop_balance("neftyblocksd")
        return data


    def get_assets(self):
        if self.assets is None:
            response = self.cleos.get_table(code="atomicassets",
                                            scope=self.name,
                                            table="assets",
                                            limit=1000
                                            )

            if response["rows"]:
                self.assets = [asset["asset_id"] for asset in response["rows"]]
                return self.assets
        else:
            return self.assets


    """ Actions """
    def deposit_to_drop(self, drop, force=False, sio=None):
        """
        :param drop: AtomicDrop or NeftyDrop instance
        :param force: if force == True: skip balance check proccess
        :param: sio: SocketIo client
        :return: None
        """

        if force:
            current_balance = 0.0
        else:
            current_balance = self.get_drop_balance(drop.contract_account)

        if current_balance < drop.listing_price:
            data = {
                "from": self.name,
                "to": drop.contract_account,
                "quantity": f"{(drop.listing_price - current_balance):.8f} WAX",
                "memo": "deposit"
            }
            response = send_transaction(self.cleos, self.key, self.name, "eosio.token", "transfer", data)
            if response["processed"]["error_code"] is None:
                print(f"Deposit to drop in {drop.listing_price:.8f} WAX for account \"{self.name}\" successful")
                if sio:
                    sio.emit("debug_script", f"Deposit to drop in {drop.listing_price:.8f} WAX for account \"{self.name}\" successful")
            else:
                print(f"Deposit to drop in {drop.listing_price:.8f} WAX for account \"{self.name}\" unsuccessful:"
                      f"{response}")
                if sio:
                    sio.emit("debug_script", f"Deposit to drop in {drop.listing_price:.8f} WAX for account \"{self.name}\" unsuccessful: "
                                             f"{response}")
        else:
            print(f"Current balance of account \"{self.name}\" already equals {drop.listing_price:.8f} WAX")
            if sio:
                sio.emit("debug_script",
                         f"Current balance of account \"{self.name}\" already equals {drop.listing_price:.8f} WAX")
            return 0

    def claim_drop(self, drop):
        data = {
            "claimer": self.name,
            "drop_id": drop.drop_id,
            "amount": 1,
            "intended_delphi_median": 0,
            "referrer": drop.referrer,
            "country": "RU",
            "currency": "8,WAX"
        }
        try:
            response = send_transaction(self.cleos, self.key, self.name, drop.contract_account, "claimdrop", data)
            if response["processed"]["error_code"] is None:
                print(f"Drop claimed for account \"{self.name}\" successful, transaction id: {response['transaction_id']}")
            else:
                print(f"Drop claimed for account \"{self.name}\" unsuccessful: "
                      f"{response}")
        except Exception as ex:
            print(f"Drop claimed for account \"{self.name}\" unsuccessful: "
                  f"{ex}")

    def claim_drop_asset(self, drop):
        data = {
            "claimer": self.name,
            "drop_id": drop.drop_id,
            "amount": 1,
            "intended_delphi_median": 0,
            "asset_ids": self.assets,
            "referrer": drop.referrer,
            "country": "RU",
            "currency": "8,WAX"
        }
        try:
            response = send_transaction(self.cleos, self.key, self.name, drop.contract_account, "claimwproof", data)
            if response["processed"]["error_code"] is None:
                print(f"Drop claimed for account \"{self.name}\" successful, transaction id: {response['transaction_id']}")
            else:
                print(f"Drop claimed for account \"{self.name}\" unsuccessful: "
                      f"{response}")
        except Exception as ex:
            print(f"Drop claimed for account \"{self.name}\" unsuccessful: "
                  f"{ex}")



class Accounts:
    def __init__(self, accounts: list):
        self.accounts = accounts
        self.que = Queue()


    # @staticmethod
    # def get_info_by_names(api, account_names: list):
    #     data = list()
    #     for name in account_names:



    def set_assets_all(self):
        for account in self.accounts:
            thread = Thread(target=account.get_assets)
            thread.start()
        time.sleep(1)


    def deposit_all(self, drop, force=False, sio=None):
        """
        :param drop: AtomicDrop or NeftyDrop instance
        :param force: if force == True: skip balance check proccess
        :param sio: SocketIo client
        :return: None
        """
        for account in self.accounts:
            thread = Thread(target=account.deposit_to_drop, args=(drop, force, sio))
            thread.start()
        time.sleep(1)

    def claim_all(self, drop):
        for account in self.accounts:
            thread = Thread(target=account.claim_drop, args=(drop,))
            thread.start()

    def claim_all_multi(self, drops: list):
        for account in self.accounts:
            thread = Thread(target=account.claim_drop, args=(drops,))
            thread.start()

    def claim_with_assets_all(self, drop):
        for account in self.accounts:
            thread = Thread(target=account.claim_drop_asset, args=(drop,))
            thread.start()
