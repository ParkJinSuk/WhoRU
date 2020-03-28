# -*- coding: utf-8 -*-
'''
2020.03.21
버튼이 눌리면 firebase database에 있는 'request' 값을 1로 바꿈
2020.03.22.
'approved'값이 1이 되면 servo motor 제어
'''

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import RPi.GPIO as GPIO
import time

pin_servo_motor = 18 # GPIO.BCM
pin_switch = 21 # GPIO.BCM
pin_led = 26 # GPIO.BCM

# red_led = port 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led, GPIO.OUT)
GPIO.setup(pin_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(pin_servo_motor, GPIO.OUT)

db_url = 'https://whoru-ed991.firebaseio.com/'
cred = credentials.Certificate("myKey.json")
db_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})
ref = db.reference()

#pin_servo_motor = 12 # GPIO.BOARD

#p = GPIO.PWM(pin_servo_motor, 50)
p = GPIO.PWM(pin_servo_motor, 50)

p.start(0)

cnt = 0
pwm = 0
switch = 0
input_state = 0
input_state_pre = 0
isrequest = False
GPIO.output(pin_led, GPIO.LOW)

try:
    while True:
        input_state_pre = input_state
        input_state = GPIO.input(pin_switch)
        
        flag = ref.child("carlist/06수 8850/approved").get()
        # APPRROVED
        if flag == '1':
            print("flag 1")
            # led off
            GPIO.output(pin_led, GPIO.LOW)
            # motor on
            p.ChangeDutyCycle(10)
            print("angle : {}".format(pwm))
            time.sleep(0.5)
        
        '''
        # REQUEST
        if input_state == 1:
            if switch == 0:
                switch = 1
                ref.child("carlist/06수 8850").update({'request': '1'})
            elif switch == 1 & flag == 0:
                switch = 0
                ref.child("carlist/06수 8850").update({'request': '0'})
        '''
        
        if (input_state != input_state_pre):
            print("edge!")
            if input_state == 0:
                switch += 1
            else:
                pass
        
        if (switch % 2 == 1) and (isrequest == False):
            print("request 1")
            ref.child("carlist/06수 8850").update({'request': '1'})
            GPIO.output(pin_led, GPIO.HIGH)
            isrequest = True
        if (switch % 2 == 0) and (isrequest == True):
            print("request 0")
            ref.child("carlist/06수 8850").update({'request': '0'})
            ref.child("carlist/06수 8850").update({'approved': '0'})
            
            GPIO.output(pin_led, GPIO.LOW)
            isrequest = False
            p.ChangeDutyCycle(1)

        '''
        pwm += 1
        if pwm == 10:
            pwm = 0
        '''
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
