def create_one_account(abstract):
    new_user_info = abstract.admin.create_user(abstract.name_prefix, abstract.stake_amount_net, abstract.stake_amount_cpu, abstract.purchase_amount_ram)
    answer = f'Successfully created 1 WAX user account: {new_user_info["user_name"]} \n\n\n' \
             f'Private Key Owner: {new_user_info["private_key_owner"]}\n\n' \
             f'Public Key Owner: {new_user_info["public_key_owner"]}\n\n' \
             f'Private Key Active: {new_user_info["private_key_active"]}\n\n' \
             f'Public Key Active: {new_user_info["public_key_active"]}\n\n\n' \
             f'Txn: {new_user_info["txn"]}'
    return answer


def get_resources_info(admin_info):
    account_info = admin_info["account"]
    answer = f'Ram quota: {account_info["ram_quota"] / 1000} KB\n' \
             f'Ram usage: {account_info["ram_usage"] / 1000} KB\n\n' \
             f'Net used: {account_info["net_limit"]["used"] / 1000} KB\n' \
             f'Net available: {account_info["net_limit"]["available"] / 1000} KB\n' \
             f'Net max: {account_info["net_limit"]["max"] / 1000} KB\n\n' \
             f'Cpu used: {account_info["cpu_limit"]["used"] / 1000} ms\n' \
             f'Cpu available: {account_info["cpu_limit"]["available"] / 1000} ms\n' \
             f'Cpu max: {account_info["cpu_limit"]["max"] / 1000} ms'
    return answer


class Abs:
    def __init__(self):
        self.admin = None
        self.tb = None
        self.name_prefix = None
        self.stake_amount_net = None
        self.stake_amount_cpu = None
        self.purchase_amount_ram = None
        self.msg = None
        self.run_now = None


def stake_resources_one(message, tb, admin, name_prefix):
    abstract = Abs()
    msg = tb.reply_to(message, 'Write amount of WAX to stake in NET')
    abstract.tb = tb
    abstract.admin = admin
    abstract.name_prefix = name_prefix
    abstract.msg = msg
    abstract.tb.register_next_step_handler(msg, stake_net_one, abstract)


def stake_net_one(message, abstract):
    abstract.run_now = True
    try:
        stake_amount_net = float(message.text)
        msg = abstract.tb.reply_to(message, f'{stake_amount_net} Wax to NET\n'
                                       f'______________________________________\n'
                                       f'Write amount of WAX to stake in CPU')
        abstract.stake_amount_net = stake_amount_net
        abstract.tb.register_next_step_handler(msg, stake_cpu_one, abstract)
    except ValueError:
        abstract.tb.reply_to(message, f'Please write only stake amount (Example : 10)')
        abstract.tb.register_next_step_handler(abstract.msg, stake_net_one, abstract)


def stake_cpu_one(message, abstract):
    try:
        abstract.stake_amount_cpu = float(message.text)
        msg = abstract.tb.reply_to(message, f'{abstract.stake_amount_cpu} Wax to CPU\n'
                                       f'________________________________________\n'
                                       f'Write amount of WAX to purchase RAM')
        abstract.tb.register_next_step_handler(msg, purchase_ram_one, abstract)
    except ValueError:
        abstract.tb.reply_to(message, f'Please write only stake amount (Example : 10)')
        abstract.tb.register_next_step_handler(abstract.msg, stake_cpu_one, abstract)


def purchase_ram_one(message, abstract):
    try:
        abstract.purchase_amount_ram = float(message.text)
        if abstract.purchase_amount_ram >= 2.0:
            abstract.tb.reply_to(message, f'{abstract.purchase_amount_ram} Wax to RAM\n' 
                                     f'__________________________________________\n'
                                     f'CPU: {abstract.stake_amount_cpu} WAX, NET: {abstract.stake_amount_net} WAX, '
                                     f'RAM: {abstract.purchase_amount_ram} WAX\n'
                                     f'__________________________________________\n'
                                     f'Creating in process')
            response = create_one_account(abstract)
            abstract.tb.send_message(message.chat.id, response)
        else:
            abstract.tb.send_message(message.chat.id, "Purchasing amount of RAM couldn't be less than 2 WAX")
            abstract.tb.register_next_step_handler(abstract.msg, purchase_ram_one, abstract)
    except ValueError:
        abstract.tb.reply_to(message, f'Please write only stake amount (Example : 10)')
        abstract.tb.register_next_step_handler(abstract.msg, purchase_ram_one, abstract)


def create_few_accounts(abstract):
    open('accounts_info.txt', 'w').close()
    new_users_info = abstract.admin.create_few_users(abstract.num, abstract.name_prefix, abstract.stake_amount_net,
                                                     abstract.stake_amount_cpu, abstract.purchase_amount_ram)
    for new_user_info in new_users_info:
        text_data = f'Username: {new_user_info["user_name"]}\n\n\n' \
                    f'Private Key Owner: {new_user_info["private_key_owner"]}\n\n' \
                    f'Public Key Owner: {new_user_info["public_key_owner"]}\n\n' \
                    f'Private Key Active: {new_user_info["private_key_active"]}\n\n' \
                    f'Public Key Active: {new_user_info["public_key_active"]}\n\n\n' \
                    f'Txn: {new_user_info["txn"]}\n' \
                    f'______________________________________________________________________________\n\n\n'
        with open("accounts_info.txt", "a") as file:
            file.write(text_data)
    answer = f'Successfully created {abstract.num} WAX user accounts'
    return answer


def stake_resources_few(message, tb, admin, name_prefix, num):
    abstract = Abs()
    msg = tb.reply_to(message, 'Write amount of WAX to stake in NET')
    abstract.num = num
    abstract.tb = tb
    abstract.admin = admin
    abstract.name_prefix = name_prefix
    abstract.msg = msg
    abstract.tb.register_next_step_handler(msg, stake_net_few, abstract)


def stake_net_few(message, abstract):
    try:
        stake_amount_net = float(message.text)
        msg = abstract.tb.reply_to(message, f'{stake_amount_net} Wax to NET\n'
                                       f'______________________________________\n'
                                       f'Write amount of WAX to stake in CPU')
        abstract.stake_amount_net = stake_amount_net
        abstract.tb.register_next_step_handler(msg, stake_cpu_few, abstract)
    except ValueError:
        abstract.tb.reply_to(message, f'Please write only stake amount (Example : 10)')
        abstract.tb.register_next_step_handler(abstract.msg, stake_net_few, abstract)


def stake_cpu_few(message, abstract):
    try:
        abstract.stake_amount_cpu = float(message.text)
        msg = abstract.tb.reply_to(message, f'{abstract.stake_amount_cpu} Wax to CPU\n'
                                       f'________________________________________\n'
                                       f'Write amount of WAX to purchase RAM')
        abstract.tb.register_next_step_handler(msg, purchase_ram_few, abstract)
    except ValueError:
        abstract.tb.reply_to(message, f'Please write only stake amount (Example : 10)')
        abstract.tb.register_next_step_handler(abstract.msg, stake_cpu_few, abstract)


def purchase_ram_few(message, abstract):
    try:
        abstract.purchase_amount_ram = float(message.text)
        if abstract.purchase_amount_ram >= 2.0:
            abstract.tb.reply_to(message, f'{abstract.purchase_amount_ram} Wax to RAM\n' 
                                     f'__________________________________________\n'
                                     f'CPU: {abstract.stake_amount_cpu} WAX, NET: {abstract.stake_amount_net} WAX, '
                                     f'RAM: {abstract.purchase_amount_ram} WAX\n'
                                     f'__________________________________________\n'
                                     f'Creating in process')
            response = create_few_accounts(abstract)
            abstract.tb.send_message(message.chat.id, response)
            with open("accounts_info.txt", "rb") as doc:
                abstract.tb.send_document(abstract.msg.chat.id, doc)
        else:
            abstract.tb.send_message(message.chat.id, "Purchasing amount of RAM couldn't be less than 2 WAX")
            abstract.tb.register_next_step_handler(abstract.msg, purchase_ram_few, abstract)
    except ValueError:
        abstract.tb.reply_to(message, f'Please write only stake amount (Example : 10)')
        abstract.tb.register_next_step_handler(abstract.msg, purchase_ram_few, abstract)


