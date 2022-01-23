def send_transaction(cleos, key, user_name, contract_account, action, data):
    payload = {
        "account": contract_account,
        "name": action,
        "authorization": [{
            "actor": user_name,
            "permission": "active",
        }],
    }

    data = cleos.abi_json_to_bin(payload['account'], payload['name'], data)
    payload['data'] = data['binargs']
    trx = {"actions": [payload]}

    return cleos.push_transaction(trx, key)

