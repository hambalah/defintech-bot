#Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

cred = credentials.Certificate("./firebase_db/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smufintech-telebot-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

data = {
    "Age" : 21,
    "Name" : "John Doe",
    "Address" : "Singapore"
}

# ref = db.reference("/")
# users_ref = ref.child("users")

# users_ref.push(data)

ref = db.reference("/users")
new_data =  {'shawntyw':{'bank':'posb', 'currency':'sgd', 'account':'12345', 'balance':100, 'pin':'1', 'userID':'', 'verified':True, "addressBook":{}}, 
            'kaydong':{'bank':'maybank','currency':'rmb','account':'23456','balance':200, 'pin':'1', 'userID':'', 'verified':False, "addressBook":{}},
            'nmywrld':{'bank':'ocbc','currency':'hkd','account':'34567','balance':300, 'pin':'1', 'userID':'', 'verified':True, "addressBook":{}},
            'ivyyytan':{'bank':'ocbc','currency':'hkd','account':'78990','balance':300, 'pin':'1', 'userID':'', 'verified':True, "addressBook":{}},
            'hyperpencil':{'bank':'ocbc','currency':'hkd','account':'78990','balance':300, 'pin':'1', 'userID':'', 'verified':True, "addressBook":{}}
            }

ref.push().set(new_data)

print(ref.get())