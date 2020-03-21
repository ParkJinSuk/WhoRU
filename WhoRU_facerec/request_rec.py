# -*- coding: utf-8 -*-
'''
2020.03.21
버튼이 눌리면 firebase database에 있는 'Request' 값을 1로 바꾸고,
firebase database의 Request 값이 1인 차량 번호를 불러온다.
(미완)
'''

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
# red_led = port 12
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

db_url = 'https://whoru-ed991.firebaseio.com/'
cred = credentials.Certificate("myKey.json")
db_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})
ref = db.reference()

while True:
    input_state = GPIO.input(11)
    if input_state is False:
        ref.child("06수 8850").update({'Request': '1'})
        GPIO.output(12, GPIO.HIGH)
    else:
        GPIO.output(12, GPIO.LOW)

    query = ref.order_by_child('Request').equal_to('1')
    snapshot = query.get()
    for key in snapshot:
        print(key)
    car_number = ref.child("Request").get()

    time.sleep(0.5)