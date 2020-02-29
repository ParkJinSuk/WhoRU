#-*- coding: utf-8 -*-
try:
    from google.cloud import storage
except ImportError:
    raise ImportError('Failed to import the Cloud Storage library for Python. Make sure '
                      'to install the "google-cloud-storage" module.')
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime

cred = credentials.Certificate("whoru-ed991-745544e53a1c.json")
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'whoru-ed991.appspot.com',
}, name='storage')

bucket = storage.bucket(app=app)
blob = bucket.blob("WhoRU_target/jacob.jpg")

print(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))
