import telebot

from admin import Admin
from funcs import get_resources_info
from funcs import stake_resources_one
from funcs import stake_resources_few
from funcs import Abs

url = "https://testnet.waxsweden.org"
name_prefix = "serbt"
num = 5
tb = telebot.TeleBot("5026947122:AAH1IMmAKD6IhGf7yDtGlrWaPcY-boFQopY", parse_mode=None)

admin_private_key = "5KjKgZWqKd1pRtLCtCi27mAJhWRDrvgD73PDbEy8bqw4jDHo1Pa"

run_now = False
admin = Admin(admin_private_key, url)


@tb.message_handler(commands=['start'])
def create_user_tg(message):
    admin_info = admin.api.get_account(admin.account.name)
    markup = telebot.types.InlineKeyboardMarkup()
    cpu_in_percent = round(admin_info["account"]["cpu_limit"]["used"] / admin_info["account"]["cpu_limit"]["max"] * 100, 2)
    ram_in_percent = round(admin_info["account"]["ram_usage"] / admin_info["account"]["ram_quota"] * 100, 2)
    markup.add(telebot.types.InlineKeyboardButton(text='Create 1 WAX account', callback_data="one_account"))
    markup.add(telebot.types.InlineKeyboardButton(text=f'Create {num} WAX accounts', callback_data="few_accounts"))
    markup.add(telebot.types.InlineKeyboardButton(text=f'CPU {cpu_in_percent}% RAM {ram_in_percent}%', callback_data="resources"))
    tb.send_message(message.chat.id, text=f"Admin: {admin_info['account']['account_name']} \n"
                                          f"Balance: {admin_info['tokens'][0]['amount']} Wax \n"
                                          f"Choose function:", reply_markup=markup)


@tb.callback_query_handler(func=lambda call: True)
def query_handler(call):
    admin_info = admin.api.get_account(admin.account.name)
    if call.data == 'one_account':
            stake_resources_one(call.message, tb, admin, name_prefix)
    elif call.data == 'few_accounts':
        stake_resources_few(call.message, tb, admin, name_prefix, num)
    elif call.data == 'resources':
        result_text = get_resources_info(admin_info)
        tb.send_message(call.message.chat.id, result_text)


tb.infinity_polling()

