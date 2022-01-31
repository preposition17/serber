from eospy.keys import EOSKey
from api.api import Api
from account import Account
from eospy.cleos import Cleos
from utils import KeyPair
from utils import random_user_name


class Admin:
    def __init__(self, private_key, url):
        self.ce = Cleos(url=url)
        self.api = Api(url=url)
        self.private_key = private_key
        self.url = url
        self.key_manager = EOSKey(private_key)
        self.account = Account(self.api, self.ce, private_key)

    def create_user(self, name_prefix, stake_amount_net, stake_amount_cpu, purchase_amount_ram):
        stake_amount_net = f'{stake_amount_net:.8f} WAX'
        stake_amount_cpu = f'{stake_amount_cpu:.8f} WAX'
        user_name = random_user_name(name_prefix)
        keypair = KeyPair()
        response = self.ce.create_account(self.account.name, self.key_manager, user_name,
                                          keypair.public_key_owner,
                                          keypair.public_key_active,
                                          stake_net=stake_amount_net, stake_cpu=stake_amount_cpu, ramkb=purchase_amount_ram,
                                          permission='active', transfer=False, broadcast=True)
        data = {
            'private_key_owner': keypair.private_key_owner,
            'public_key_owner': keypair.public_key_owner,
            'private_key_active': keypair.private_key_active,
            'public_key_active': keypair.public_key_active,
            'user_name': user_name,
            'txn': response['transaction_id']
        }
        return data

    def create_few_users(self, num, name_prefix, stake_amount_net, stake_amount_cpu, purchase_amount_ram):
        datas = []
        for user in range(num):
            new_user_info = self.create_user(name_prefix, stake_amount_net, stake_amount_cpu, purchase_amount_ram)
            datas.append(new_user_info)
        return datas
