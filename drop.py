


class Drop:
    def __init__(self, cleos, contract_account, drop_id):
        self.drop_info = cleos.get_table(code=contract_account,
                                         scope=contract_account,
                                         table="drops",
                                         lower_bound=str(drop_id),
                                         upper_bound=str(drop_id))


        self.drop_id = drop_id
        self.listing_price = float(self.drop_info["rows"][0]["listing_price"].split(" ")[0])
        self.start_time = self.drop_info["rows"][0]["start_time"]
        self.auth_required = self.drop_info["rows"][0]["auth_required"]


    def print_info(self):
        print(f"Drop info: \n"
              f"Id: {self.drop_id}\n"
              f"Price: {self.listing_price}\n"
              f"Start time: {self.start_time}\n"
              f"Auth required: {self.auth_required}\n")


class AtomicDrop(Drop):
    def __init__(self, cleos, drop_id):
        super().__init__(cleos=cleos, contract_account="atomicdropsx", drop_id=drop_id)
        self.contract_account = "atomicdropsx"
        self.referrer = "atomichub"


class NeftyDrop(Drop):
    def __init__(self, cleos, drop_id):
        super().__init__(cleos=cleos, contract_account="neftyblocksd", drop_id=drop_id)
        self.contract_account = "neftyblocksd"
        self.referrer = "neftyblocks"


