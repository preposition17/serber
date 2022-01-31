import random
import string
from eosjs_python import Eos


class KeyPair:
    def __init__(self):
        key_pair_owner = Eos.generate_key_pair()
        key_pair_active = Eos.generate_key_pair()

        self.private_key_owner = key_pair_owner["private"]
        self.public_key_owner = key_pair_owner["public"]

        self.private_key_active = key_pair_active["private"]
        self.public_key_active = key_pair_active["public"]


def random_user_name(prefix):
    letters = string.ascii_lowercase
    randomise = prefix + ''.join(random.choice(letters) for i in range(12 - len(prefix)))
    return randomise
