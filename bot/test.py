import telebot
from telebot import types


tb = telebot.TeleBot("5026947122:AAH1IMmAKD6IhGf7yDtGlrWaPcY-boFQopY", parse_mode=None)


@tb.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Info', callback_data="info"))
    tb.send_message(message.chat.id, text="Nice cock", reply_markup=markup)


@tb.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'info':
        choose_step(call.message)
    elif call.data == 'info2':
        result_text = "We are not done here"
    else:
        result_text = "Impossible"


# @tb.message_handler(content_types=['text'])
# def message_reply(message):
#     print(message)


def choose_step(chat_id):
    msg = tb.reply_to(chat_id, 'Choose num pls')
    tb.register_next_step_handler(msg, first_step)


def first_step(message):
    try:
        input_num = float(message.text)
        msg = tb.reply_to(message, f'{input_num} Wax staked, Choose next pls')
        tb.register_next_step_handler(msg, second_step)
    except ValueError:
        tb.reply_to(message, f'Please write only stake amount (Example : 10)')
        tb.register_next_step_handler(message, first_step)


def second_step(message):
    try:
        input_num = float(message.text)
        tb.reply_to(message, f'{input_num} Wax staked')
    except ValueError:
        tb.reply_to(message, f'Please write only stake amount (Example : 10)')
        tb.register_next_step_handler(message, second_step)


tb.infinity_polling()
