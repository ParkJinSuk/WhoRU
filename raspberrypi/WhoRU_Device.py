# -*- coding: utf-8 -*-
'''
2020.03.21
버튼이 눌리면 firebase database에 있는 'request' 값을 1로 바꿈
2020.03.22.
'approved'값이 1이 되면 servo motor 제어
'''
import threading, requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import RPi.GPIO as GPIO
import time

pin_servo_motor = 18 # GPIO.BCM
pin_switch = 21 # GPIO.BCM
pin_led_yellow = 19 # GPIO.BCM
pin_led_blue = 26 # GPIO.BCM

# red_led = port 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led_yellow, GPIO.OUT)
GPIO.setup(pin_led_blue, GPIO.OUT)
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
flag = 0
request = 0
input_state = 0
input_state_pre = 0
isrequest = False
GPIO.output(pin_led_yellow, GPIO.LOW)
GPIO.output(pin_led_blue, GPIO.LOW)

class get_database (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
        
    def run(self):
        print("[Thread] get database start")
        global flag
        global request
        while True:
            flag = ref.child("carlist/06수 8850/approved").get()
            request = ref.child("carlist/06수 8850/request").get()
            print("[Thread] flag\t: {}".format(flag))
            print("[Thread] request\t: {}".format(request))
            


if __name__ == "__main__":
    try:
        _time = 0
        thread_database = get_database()
        thread_database.start()
        p.ChangeDutyCycle(1)
                
        while True:
            input_state_pre = input_state
            input_state = GPIO.input(pin_switch)
            
            # APPRROVED
            if flag == '1' and request == '1':
                print("flag 1")
                # led off   
                GPIO.output(pin_led_yellow, GPIO.LOW)
                GPIO.output(pin_led_blue, GPIO.HIGH)
                # motor on
                p.ChangeDutyCycle(10)
                print("angle : {}".format(pwm))
                
            
            if (input_state != input_state_pre): # switch edge detecting
                print("edge!")
                if input_state == 0:
                    switch += 1
                else:
                    pass
            
            if (switch % 2 == 1) and (isrequest == False):
                print("request 1")
                _time =time.time()
                ref.child("carlist/06수 8850").update({'request': '1'})
                GPIO.output(pin_led_yellow, GPIO.HIGH)
                GPIO.output(pin_led_blue, GPIO.LOW)
                isrequest = True
            if (switch % 2 == 0) and (isrequest == True):
                print("request 0")
                _time = 0
                GPIO.output(pin_led_yellow, GPIO.LOW)
                GPIO.output(pin_led_blue, GPIO.LOW)
                p.ChangeDutyCycle(1)
                
                ref.child("carlist/06수 8850").update({'request': '0'})
                ref.child("carlist/06수 8850").update({'approved': '0'})
                isrequest = False
                time.sleep(1)
                
            '''
            if time.time() - _time > 15: # time out
                switch += 1
            '''
            

    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
