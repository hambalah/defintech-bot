from telegram.ext import *
from requests import *
from telegram import *

updater = Updater(token='5668531051:AAEeX4OWwO1sOPvIYMI-2nUyhTcz_UWQVH4',use_context=True)
dp = updater.dispatcher

#telehamdle linked with account details
database = {'@shawn':{'bank':'posb', 'currency':'sgd', 'account':'12345', 'balance':100, 'pin':''}, 
            '@kaydon':{'bank':'maybank','currency':'rmb','account':'23456','balance':200, 'pin':''},
            '@drago':{'bank':'ocbc','currency':'hkd','account':'34567','balance':300, 'pin':''}}


#update with database based on telehandle when logged in
current_account = ''
logged_in = False

#must login first, to retrieve the ID.
def login(update: Update, context:CallbackContext):#can include a separate function that returns the response
    global logged_in 
    if logged_in == False:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'https://www.finverse.com/')
        global user 
        global current_account
        user = update.message.chat.first_name
        current_account = database[user]
        logged_in = True
        print(update)
        print(current_account)
        print(user)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'logged in already.')
dp.add_handler(CommandHandler('login', login))

def help(update: Update, context: CallbackContext):
    displayed = '/login --> login to finverse\n/start --> view functions\n/createpin --> create pin for transactions, "type the command and pin together and send it"\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=displayed)
dp.add_handler(CommandHandler('help', help))

def createpin(update: Update, context: CallbackContext):
    if logged_in == True:
        #havent update in database
        pin = ' '.join(context.args)
        #pointer that updates both the current_account and database
        current_account['pin'] = pin
        displayed=f'Your pin has been created, {pin}.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=displayed)
        print(current_account)
        print(database)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='please /login first')
pin_handler = CommandHandler('createpin', createpin)
dp.add_handler(pin_handler)


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
        update.message.send_message(f'please input receivers handle and amount')
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

