from telegram.ext import *
from requests import *
from telegram import *

updater = Updater(token='5668531051:AAEeX4OWwO1sOPvIYMI-2nUyhTcz_UWQVH4',use_context=True)
dp = updater.dispatcher

#telehamdle linked with account details
database = {'@shawn':{'bank':'posb', 'currency':'sgd', 'account':'12345', 'balance':100 }, 
            '@kaydon':{'bank':'maybank','currency':'rmb','account':'23456','balance':200},
            '@drago':{'bank':'ocbc','currency':'hkd','account':'34567','balance':300}}


#update with database based on telehandle when logged in
current_account = ''
print('hello world')
print()

def login(update, context):
    update.message.reply_text('(url link to finverse)')




def handle_message(update,context):
    # text = str(update.message.text).lower()
    # response = ''
    # if 'hello' in text:
    #     response = 'Hellooo!'
    #     update.message.reply_text(f"{response} {update['message']['chat']['first_name']}.")
    # if 'how are you' in text:
    #     response = 'GRAAAAPEEEE!'
    #     update.message.reply_text(f"I'm {response}, {update['message']['chat']['first_name']}.")
    #     update.message.reply_text(f"how are you {update.message.chat.first_name}.")
    # #update.message.chat.first_name == update['message']['chat']['first_name']
    if 'Account Balance' in update.message.text:
        update.message.reply_text(f'{update.message.chat.first_name}, your account balance is {current_account["@shawn"]["balance"]}')
    if 'Funds Transfer' in update.message.text:
        update.message.reply_text(f'please input receivers handle and amount')
    if 'Account Details' in update.message.text:
        update.message.reply_text(f'name: {update.message.chat.first_name}, account balance: XXX')


def startCommands(update: Update,context:CallbackContext):
    buttons = [[KeyboardButton('MAYBANK: Account Balance')], [KeyboardButton('MAYBANK: Funds Transfer')], [KeyboardButton('Change Bank Account')]]
    context.bot.send_message(chat_id=update.effective_chat.id, text='WELCOME!',reply_markup = ReplyKeyboardMarkup(buttons))

dp.add_handler(CommandHandler('start', startCommands))
dp.add_handler(MessageHandler(Filters.text, handle_message))
dp.add_handler(CommandHandler('login', login))

updater.start_polling()

# if __name__ == '__main__':
#     Token = '5668531051:AAEeX4OWwO1sOPvIYMI-2nUyhTcz_UWQVH4'
#     updater = Updater(Token, use_context=True)
#     dp = updater.dispatcher
#     dp.add_handler(MessageHandler(Filters.text, handle_message))
#     dp.add_handler(CommandHandler('start',startCommands))
#     updater.start_polling(1.0)
#     updater.idle()

