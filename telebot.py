from telegram.ext import *
from requests import *
from telegram import *


# updater = Updater(token='5668531051:AAEeX4OWwO1sOPvIYMI-2nUyhTcz_UWQVH4',use_context=True) #shawn's bot
updater = Updater(token='5828726712:AAH2mCRI9FKiQmZBgM_SEmHeQhMl23kEK88',use_context=True) #drago's bot
# updater = Updater(token='5860916892:AAF8lhYm-CZiNigpGxbJehVAckG6w2ekHhk',use_context=True) #kaydon's bot


dp = updater.dispatcher

#telehamdle linked with account details

database = {'shawntyw':{'bank':'posb', 'currency':'sgd', 'account':'12345', 'balance':100, 'pin':'1', 'userID':''}, 
            'kaydong':{'bank':'maybank','currency':'rmb','account':'23456','balance':200, 'pin':'1', 'userID':''},
            'nmywrld':{'bank':'ocbc','currency':'hkd','account':'34567','balance':300, 'pin':'1', 'userID':''},
            'ivyyytan':{'bank':'ocbc','currency':'hkd','account':'78990','balance':300, 'pin':'1', 'userID':''},
            'hyperpencil':{'bank':'ocbc','currency':'hkd','account':'78990','balance':300, 'pin':'1', 'userID':''}
            }



#update with database based on telehandle when logged in
current_account = ''

logged_in = False

#must login first, to retrieve the ID.
def login(update: Update, context:CallbackContext):
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


# transfer process
# used for transfer processx
startstate, receiverstate, trfamtstate, confirmationstate = range(4)

def transfer_process(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Receivers' Telegram handle (without @)")
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Please Enter Your Pin")
    return startstate

def transfer_process_start (update, context):
    context.user_data["pin"] = update.message.text
    if context.user_data["pin"] != database[update.message.chat.username]["pin"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Pin Incorrect!")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Pin Confirmed!")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Receivers' Telegram handle (without @)")
        return receiverstate
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Transfer Amount")
    return trfamtstate

def transfer_process_name (update, context):
    context.user_data["receiverTeleId"] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Transfer Amount")
    return trfamtstate

def transfer_process_amt (update, context):
    context.user_data["transferAmount"] = float(update.message.text)
    if context.user_data["transferAmount"] > database[update.message.chat.username]["balance"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You Do Not Have Enough Funds!')
        return startstate
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You want to send ${context.user_data["transferAmount"]} to @{context.user_data["receiverTeleId"]}?')
        print(context.user_data)
        return confirmationstate
    

def transfer_process_confirm(update, context):
    if update.message.text == "yes":
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'A Request to transfer ${context.user_data["transferAmount"]} to @{context.user_data["receiverTeleId"]} has been made.')
        database[update.message.chat.username]["balance"] -= context.user_data["transferAmount"]
        database[context.user_data["receiverTeleId"]]["balance"] += context.user_data["transferAmount"]
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Transfer Successful!')
        context.bot.send_message(chat_id=database[context.user_data["receiverTeleId"]]['userID'], text='you have received money!')
        return ConversationHandler.END
    else:
        return startstate
    
# def transfer_process_complete(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=f'Transfer Successful!')
#         # send "Transfer has been made"

#     return ConversationHandler.END


def handle_message(update, context):
    global transferFlag
    global receiverTeleId
    global transferAmount

    if 'Account Balance' in update.message.text:
        update.message.reply_text(f'{update.message.chat.username}, your account balance is {database[update.message.chat.username]["balance"]}')

    if 'Account Details' in update.message.text:
        update.message.reply_text(f'name: {update.message.chat.first_name}, account balance: XXX')


def startCommands(update: Update, context:CallbackContext):
    database[update.message.chat.username]["userID"] = chat_id=update.effective_chat.id
    buttons = [[KeyboardButton('Account Balance')], [KeyboardButton('/Transfer')], [KeyboardButton('Change Bank Account')]]
    print(update)
    print()
    print(database)
    context.bot.send_message(chat_id=update.effective_chat.id, text='WELCOME!',reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True))


transaction_process_conv = ConversationHandler(
    entry_points=[CommandHandler(f'Transfer', transfer_process)],
    states={
        startstate : [MessageHandler(Filters.text, callback=transfer_process_start)],
        receiverstate : [MessageHandler(Filters.text, callback=transfer_process_name)],
        trfamtstate : [MessageHandler(filters= Filters.regex('[0-9]'), callback=transfer_process_amt)],
        confirmationstate: [MessageHandler(Filters.regex('yes|no'), callback=transfer_process_confirm)]
    },
    fallbacks=[CommandHandler('start', startCommands)]
)


dp.add_handler(CommandHandler('start', startCommands))
dp.add_handler(transaction_process_conv)
dp.add_handler(MessageHandler(Filters.text, handle_message))
dp.add_handler(CommandHandler('login', login))

updater.start_polling()


