########################################
led 제어 코드
########################################
import RPi.GPIO as GPIO
import time

pin = 12 #BCM 12

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        GPIO.output(pin, False)
        time.sleep(1)
        GPIO.output(pin, True)
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()

#######################################
