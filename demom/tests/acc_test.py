from eospy.cleos import Cleos
from api.api import Api

from account import Account


# cleos = Cleos(url="https://testnet.wax.eosdetroit.io")
# api = Api(url="https://testnet.wax.eosdetroit.io")

cleos = Cleos(url="https://testnet.waxsweden.org")
api = Api(url="https://testnet.waxsweden.org")

acc = Account(api, cleos, "5JWBoukx5cbE2f8FEKGdgcacGESwPeVgUVe6ipdoqnCbx3HYyjF")
print(acc.get_drop_balance("atomicdropsx"))

# print(cleos.get_table(code="atomicdropsx",
#                                     scope="atomicdropsx",
#                                     table="balances",
#                                     lower_bound="mandytestnet",
#                                     upper_bound="mandytestnet"))