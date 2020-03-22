import RPi.GPIO as GPIO
import time

pin_servo_motor = 18 # GPIO.BCM 18
#pin_servo_motor = 12 # GPIO.BOARD
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin_servo_motor, GPIO.OUT)


p = GPIO.PWM(pin_servo_motor, 50)
p.start(0)

cnt = 0

pwm = 0
try:
    while True: 
        pwm = input()
        pwm = int(pwm)
        p.ChangeDutyCycle(pwm)
        print("angle : {}".format(pwm))
        time.sleep(1)
        
        '''
        pwm += 1
        if pwm == 10:
            pwm = 0
        '''
except KeyboardInterrupt:
    p.stop()
GPIO.cleanup()
