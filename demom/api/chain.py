class Chain:
    def __init__(self, api):
        self.api = api

    @property
    def chain_info(self):
        return self.api.session.get(self.api.api_url + self.api.v1 + "chain/get_info").json()



    @property
    def last_block(self):
        """
        Get last block details
        """
        last_block_num = self.chain_info["last_irreversible_block_id"]
        response = self.api.session.post(self.api.api_url + self.api.v1 + "chain/get_block",
                                         json={
                                             "block_num_or_id": str(last_block_num)
                                         })
        return response.json()

    def block_info(self, block_num_or_id):
        response = self.api.session.post(self.api.api_url + self.api.v1 + "chain/get_block",
                                         json={
                                             "block_num_or_id": str(block_num_or_id)
                                         })
        return response

