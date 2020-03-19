# -*- coding: UTF-8 -*-
try:
    from google.cloud import storage
except ImportError:
    raise ImportError('Failed to import the Cloud Storage library for Python. Make sure '
                      'to install the "google-cloud-storage" module.')
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import datetime
import urllib.request

db_url = 'https://whoru-ed991.firebaseio.com/'
sr_buck = 'whoru-ed991.appspot.com'
cred = credentials.Certificate("./whoru-ed991-firebase-adminsdk-o6sq7-2aa9f68fea.json")
db_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})
sr_app = firebase_admin.initialize_app(cred, {'storageBucket': sr_buck,}, name='storage')
# ref = db.reference('/whoru-ed991')
ref = db.reference()


def find_user():
    usr = ref.child('10주 1300/FLAG').get()
    print(usr)
    if usr == 1:
        print(usr)


find_user()
bucket = storage.bucket(app=sr_app)
blob = bucket.blob("WhoRU_target/jacob.jpg")
img_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
# print(img_url)

urllib.request.urlretrieve(img_url, './image/1.jpg')
print("save")
