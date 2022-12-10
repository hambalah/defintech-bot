from telegram.ext import *
from requests import *
from telegram import *

# updater = Updater(token='5668531051:AAEeX4OWwO1sOPvIYMI-2nUyhTcz_UWQVH4',use_context=True)
updater = Updater(token='5828726712:AAH2mCRI9FKiQmZBgM_SEmHeQhMl23kEK88',use_context=True)

# bot = TeleBot("5828726712:AAFx7vMV1rv3oiqJFyEhx76HpY2bqU_iVXI")
dp = updater.dispatcher

#telehamdle linked with account details
database = {'shawn':{'bank':'posb', 'currency':'sgd', 'account':'12345', 'balance':100 }, 
            'kaydon':{'bank':'maybank','currency':'rmb','account':'23456','balance':200},
            'nmywrld':{'bank':'ocbc','currency':'hkd','account':'34567','balance':300}}


#update with database based on telehandle when logged in
current_account = ''


# used for transfer processx
receiverstate, trfamtstate = range(2)





def login(update, context):
    update.message.reply_text('(url link to finverse)')


# transfer process
def transfer_process(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Receivers' Telegram handle")
    return receiverstate

def transfer_process_name (update, context):
    context.user_data["receiverTeleId"] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Transfer Amount")
    return trfamtstate

def transfer_process_amt (update, context):
    context.user_data["transferAmount"] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'You want to send ${context.user_data["transferAmount"]} to @{context.user_data["receiverTeleId"]}')

    print(context.user_data)
    return ConversationHandler.END
    

def handle_message(update,context):
    global transferFlag
    global receiverTeleId
    global transferAmount

    if 'Account Balance' in update.message.text:
        update.message.reply_text(f'{update.message.chat.username}, your account balance is {database[update.message.chat.username]["balance"]}')
    if 'Funds Transfer' in update.message.text:
        transferFlag = True 
    if 'Account Details' in update.message.text:
        update.message.reply_text(f'name: {update.message.chat.first_name}, account balance: XXX')



def startCommands(update: Update, context:CallbackContext):
    buttons = [[KeyboardButton('Account Balance')], [KeyboardButton('/Transfer')], [KeyboardButton('Change Bank Account')]]
    print(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text='WELCOME!',reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True))


transaction_process_conv = ConversationHandler(
    entry_points=[CommandHandler(f'Transfer', transfer_process)],
    states={
        receiverstate : [MessageHandler(Filters.text, callback=transfer_process_name)],
        trfamtstate : [MessageHandler(filters= Filters.regex('[0-9]'), callback=transfer_process_amt)]
    },
    fallbacks=[CommandHandler('start', startCommands)]
)


dp.add_handler(CommandHandler('start', startCommands))
dp.add_handler(transaction_process_conv)
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

