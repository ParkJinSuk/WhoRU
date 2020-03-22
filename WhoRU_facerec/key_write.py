# -*- coding: utf-8 -*-


# FOR STORAGE
try:
    from google.cloud import storage
except ImportError:
    raise ImportError('Failed to import the Cloud Storage library for Python. Make sure '
                      'to install the "google-cloud-storage" module.')

# FOR DATABASE
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


####### Global Variable ######
cnt_face = 0
###############################

################ firebase import name #####################
db_url = 'https://whoru-ed991.firebaseio.com/'
cred = credentials.Certificate("myKey.json")
db_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})
alldata = db.reference()
username = alldata.child("06수 8850/username").get()
sr_buck = 'whoru-ed991.appspot.com'
sr_app = firebase_admin.initialize_app(cred, {'storageBucket': sr_buck, }, name='storage')
#########################################################

alldata.child('carlist').set({'08구 8500/Request': '1'})