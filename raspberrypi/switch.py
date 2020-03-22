########################################
스위치 제어 코드
########################################
import RPi.GPIO as GPIO
from time import sleep
from subprocess import call
from datetime import datetime

btn_pin = 3
shutdown_sec = 0.5 

GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)

press_time = None

def button_state_changed(pin):
    global press_time
    if GPIO.input(pin) == 0:    # btn down
        if press_time is None:
            press_time = datetime.now()
    else:                       # btn up
        if press_time is not None:
            elapsed = (datetime.now() - press_time).total_seconds()
            press_time = None 
            if elapsed >= shutdown_sec:
                call(["shutdown", "-h", "now"], shell=False)
        
# subscribe to button presses
GPIO.add_event_detect(btn_pin, GPIO.BOTH, callback=button_state_changed)

while True:
sleep(5)
##########################################