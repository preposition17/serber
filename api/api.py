import atexit
import pytz
import datetime
import hashlib

import json
import requests

from .chain import Chain




class Api:
    def __init__(self, url):
        if url[-1] != "/":
            url += "/"

        self.api_url = url

        self.v1 = "v1/"
        self.v2 = "v2/"

        self.session = requests.Session()

        self.chain = Chain(self)


    def get_account(self, account):
        """
        Get account summary by account name or account public key
        :param account: account name or pub_key
        :return: account data
        """
        if len(account) < 13:
            response = self.session.get(self.api_url + self.v2 + "state/get_account", params={
                "account": account
            })
        else:
            response = self.session.get(self.api_url + self.v2 + "state/get_key_accounts", params={
                "public_key": account
            })
            account_name = response.json()["account_names"][0]
            response = self.session.get(self.api_url + self.v2 + "state/get_account", params={
                "account": account_name
            })

        return response.json()


    def push_transaction(self, transaction_data):
        if 'expiration' not in transaction_data:
            transaction_data['expiration'] = str((datetime.datetime.utcnow() + datetime.timedelta(seconds=30)).replace(tzinfo=pytz.UTC))
        if 'ref_block_num' not in transaction_data:
            transaction_data['ref_block_num'] = transaction_data['last_irreversible_block_num'] & 0xFFFF
        if 'ref_block_prefix' not in transaction_data:
            transaction_data['ref_block_prefix'] = transaction_data['ref_block_prefix']



if __name__ == '__main__':
    api = Api("https://testnet.waxsweden.org/")
    print(api.chain.chain_info)
    print(api.chain.last_block)



