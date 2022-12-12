from telegram.ext import *
from requests import *
from telegram import *
import logging
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# updater = Updater(token='5668531051:AAEeX4OWwO1sOPvIYMI-2nUyhTcz_UWQVH4',use_context=True) #shawn's bot
# updater = Updater(token='5828726712:AAH2mCRI9FKiQmZBgM_SEmHeQhMl23kEK88',use_context=True) #drago's bot
updater = Updater(token='5860916892:AAF8lhYm-CZiNigpGxbJehVAckG6w2ekHhk',use_context=True) #kaydon's bot


dp = updater.dispatcher

#telehamdle linked with account details


local_database = {'shawntyw':{'bank':'posb', 'currency':'sgd', 'account':'12345', 'balance':100, 'pin':'1', 'userID':'', 'verified':True, "addressBook":{}}, 
            'kaydong':{'bank':'maybank','currency':'rmb','account':'23456','balance':200, 'pin':'1', 'userID':'', 'verified':False, "addressBook":{}},
            'nmywrld':{'bank':'ocbc','currency':'hkd','account':'34567','balance':300, 'pin':'1', 'userID':'', 'verified':True, "addressBook":{}},
            'ivyyytan':{'bank':'ocbc','currency':'hkd','account':'78990','balance':300, 'pin':'1', 'userID':'', 'verified':True, "addressBook":{}},
            'hyperpencil':{'bank':'ocbc','currency':'hkd','account':'78990','balance':300, 'pin':'1', 'userID':'', 'verified':True, "addressBook":{}}
            }

city_info = {'Singapore':{'bank': ['UOB', 'DBS', 'OCBC'], 'currency': 'sgd'}, 
            'Malaysia':{'bank':['MayBank', 'AHB'], 'currency':'rmb'}, 
            'Indonesia': {'bank': ['RHB', 'BNI'], 'currency':'idr'},
            }

#update with local_database based on telehandle when logged in
current_account = ''
# used for transfer processx
receiverstate, trfamtstate = range(2)

logged_in = False
verified = False
displayed = ''

#KYC Process
kycImgState, kycDetailsState, kycCountryState, kycBankState = range(4)

def kyc_start(update: Update, context: CallbackContext):
    print('--- kyc ---')
    global verified
    verified = local_database[update.message.chat.username]['verified']
    if verified == False:
        print('not verified')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Starting your KYC process.', reply_markup=ReplyKeyboardRemove())
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('./img/ic_w_date.jpg', 'rb'), caption='Please upload an image of yourself holding your IC, with the current date and time clearly visible.')
        return kycImgState
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You are already verified.')
    return ConversationHandler.END

def kyc_img(update: Update, context: CallbackContext):
    global verified
    print('--- kyc_img ---')
    # context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    photo_file = update.message.photo[-1].get_file()
    print(photo_file)
    if photo_file == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please upload an image of yourself!')
        return kycImgState
    else:
        photo_file.download('./kyc_images/'+update.message.chat.username+'.jpg')
        verified = True
        local_database[update.message.chat.username]['verified'] = verified
        buttons = [InlineKeyboardButton('Done', callback_data='done')]
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please click the button after you uploaded your image.', reply_markup=InlineKeyboardMarkup([buttons]))
        print('--- kyc_img ends ---')
        return kycDetailsState

def kyc_details(update: Update, context: CallbackContext):
    global local_database
    global city_info
    print('--- kyc_details ---')

    buttons = []
    for city in city_info.keys():
        buttons.append(InlineKeyboardButton(city, callback_data=city))
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please select your country of residence',reply_markup = reply_markup)

    return kycCountryState

def kyc_country(update: Update, context: CallbackContext):
    global local_database
    global city_info
    print('--- kyc_country ---')
    #updating country details
    local_database[update.callback_query.from_user.username]['country'] = update.callback_query.data
    local_database[update.callback_query.from_user.username]['currency'] = city_info[update.callback_query.data]['currency']

    buttons = []
    for bank in city_info[update.callback_query.data]['bank']:
        buttons.append(InlineKeyboardButton(bank, callback_data=bank))
    reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please select your bank',reply_markup = reply_markup)
    return kycBankState

def kyc_bank(update: Update, context: CallbackContext):
    global local_database
    global city_info
    print('--- kyc_bank ---')
    print(update)
    #updating bank details
    local_database[update.callback_query.from_user.username]['bank'] = update.callback_query.data

    #creating a new rng account number
    newAccountNumber = False
    while newAccountNumber != True:
        accountNumber = random.randint(10000,99999)
        existingAccounts = [local_database[user]['account'] for user in local_database.keys()]
        if accountNumber not in existingAccounts:
            newAccountNumber = True
            local_database[update.callback_query.from_user.username]['account'] = accountNumber
            local_database[update.callback_query.from_user.username]['balance'] = 0

    username = update.callback_query.from_user.username
    bank = local_database[username]['bank']
    country = local_database[username]['country']
    currency = local_database[username]['currency']
    print(username, country, currency, accountNumber, local_database[username]['verified'], sep=' | ')
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text=f'Thank you for verifying your details, {username} 😊. \n Country : {country} \n Bank : {bank} \n Currency : {currency} \n Account Number : {accountNumber}. \n\nIf you wish to restart the KYC process, please enter /kyc again. \nIf you wish to start using the bot, please enter /start.')
    return ConversationHandler.END

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu


#must login first, to retrieve the ID.
def login(update: Update, context:CallbackContext):
    global logged_in 
    if logged_in == False:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'https://www.finverse.com/')
        global user 
        global current_account
        user = update.message.chat.first_name
        current_account = local_database[user]
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


def createPin(update: Update, context: CallbackContext):
    if logged_in == True:
        pin = ' '.join(context.args)
        #pointer that updates both the current_account and local_database
        current_account['pin'] = pin
        displayed=f'Your pin has been created, {pin}.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=displayed)
        print(current_account)
        print(local_database)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='please /login first')
pin_handler = CommandHandler('createPin', createPin)
dp.add_handler(pin_handler)


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
    buttons = [[KeyboardButton('Account Balance')], [KeyboardButton('/Transfer')], [KeyboardButton('/AddRecipient')]]
    print(update)
    print()
    print(database)
    context.bot.send_message(chat_id=update.effective_chat.id, text='WELCOME!',reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True))

# transfer process
# used for transfer processx
startstate, receiverstate, trfamtstate, confirmationstate = range(4)

def transfer_process(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Receivers' Telegram handle (without @)")
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Please Enter Your Pin")
    return startstate

def transfer_process_start (update, context):
    context.user_data["pin"] = update.message.text
    if context.user_data["pin"] != local_database[update.message.chat.username]["pin"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Pin Incorrect!")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Pin Confirmed!")
        # buttons = [[KeyboardButton('Account Balance')], [KeyboardButton('/Transfer')], [KeyboardButton('/AddRecipient')]]
        buttons = []
        for key in database[update.message.chat.username]["addressBook"].keys():
            buttons.append([KeyboardButton(f'{key}')])
        
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please select Recipient!',reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
        # context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Receivers' Telegram handle (without @)")
        return receiverstate

def transfer_process_name (update, context):
    context.user_data["receiverTeleId"] = database[update.message.chat.username]["addressBook"][update.message.text]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please Input Transfer Amount")
    return trfamtstate

def transfer_process_amt (update, context):
    context.user_data["transferAmount"] = float(update.message.text)
    if context.user_data["transferAmount"] > local_database[update.message.chat.username]["balance"]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You Do Not Have Enough Funds!')
        return startstate
    else:
        buttons = [[KeyboardButton('Yes')], [KeyboardButton('No')]]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'You want to send ${context.user_data["transferAmount"]} to @{context.user_data["receiverTeleId"]}?', reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
        print(context.user_data)
        return confirmationstate
    
def transfer_process_confirm(update, context):
    if update.message.text == "Yes":
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'A Request to transfer ${context.user_data["transferAmount"]} to @{context.user_data["receiverTeleId"]} has been made.')
        local_database[update.message.chat.username]["balance"] -= context.user_data["transferAmount"]
        local_database[context.user_data["receiverTeleId"]]["balance"] += context.user_data["transferAmount"]
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Transfer Successful!')
        context.bot.send_message(chat_id=local_database[context.user_data["receiverTeleId"]]['userID'], text='you have received money!')
        return ConversationHandler.END
    else:
        return startstate
    
# def transfer_process_complete(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=f'Transfer Successful!')
#         # send "Transfer has been made"

#     return ConversationHandler.END


#### New recipient process

recipientName , recipientHandle = range(2)

def newRecipient (update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Please Enter New Recipient Name")
    return recipientName

def add_recipient_name (update, context):
    context.user_data["recipientName"] = update.message.text
    database[update.message.chat.username]["addressBook"][update.message.text] = ""
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Please Enter New Recipient telegram Handle (without @)")
    return recipientHandle

def add_recipient_handle (update, context):
    context.user_data["recipientHandle"] = update.message.text
    database[update.message.chat.username]["addressBook"][context.user_data["recipientName"]] = update.message.text
    return ConversationHandler.END



def handle_message(update, context):
    global transferFlag
    global receiverTeleId
    global transferAmount

    if 'Account Balance' in update.message.text:
        update.message.reply_text(f'{update.message.chat.username}, your account balance is {local_database[update.message.chat.username]["balance"]}')

    if 'Account Details' in update.message.text:
        update.message.reply_text(f'name: {update.message.chat.first_name}, account balance: XXX')


def startCommands(update: Update, context:CallbackContext):
    local_database[update.message.chat.username]["userID"] = chat_id=update.effective_chat.id
    buttons = [[KeyboardButton('Account Balance')], [KeyboardButton('Transfer')], [KeyboardButton('Change Bank Account Details')]]
    print(update)
    print()
    print(local_database)
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

add_recipient_conv = ConversationHandler(
    entry_points= [CommandHandler(f'AddRecipient', newRecipient)],
    states = {
        recipientName : [MessageHandler(Filters.text, callback= add_recipient_name)],
        recipientHandle : [MessageHandler(Filters.text, callback= add_recipient_handle)]
    },
    fallbacks=[CommandHandler('start', startCommands)]
)


kyc_process_conv = ConversationHandler(
    entry_points=[CommandHandler(f'kyc', kyc_start)],
    states={
        kycImgState : [MessageHandler(Filters.photo, callback=kyc_img)],
        kycDetailsState : [CallbackQueryHandler(kyc_details)],
        kycCountryState : [CallbackQueryHandler(kyc_country)],
        kycBankState : [CallbackQueryHandler(kyc_bank)]
    },
    fallbacks=[CommandHandler('start', startCommands)]
)


dp.add_handler(CommandHandler('start', startCommands))
dp.add_handler(transaction_process_conv)
dp.add_handler(add_recipient_conv)
dp.add_handler(kyc_process_conv)
dp.add_handler(MessageHandler(Filters.text, handle_message))
dp.add_handler(CommandHandler('login', login))

updater.start_polling()