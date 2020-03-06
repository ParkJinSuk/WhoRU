#-*- coding: utf-8 -*-
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
from bs4 import BeautifulSoup

db_url = 'https://whoru-ed991.firebaseio.com/'
sr_buck = 'whoru-ed991.appspot.com'
cred = credentials.Certificate("whoru-ed991-745544e53a1c.json")
db_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})
sr_app = firebase_admin.initialize_app(cred, {'storageBucket': sr_buck,}, name='storage')

ref = db.reference('whoru-ed991/')


def find_user():
    usr = ref.order_by_child('FlAG').equal_to(1).get()
    # item = usr.popitem() //첫번째 element를 가져오는 함수
    print(usr)


find_user()
bucket = storage.bucket(app=sr_app)
blob = bucket.blob("WhoRU_target/jacob.jpg")
print(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))
# img_url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')


