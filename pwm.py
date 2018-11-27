import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import time

myPWM="P8_13"
GPIO.setup("P8_8",GPIO.OUT)

PWM.start(myPWM, 100, 1000000)
PWM.set_duty_cycle(myPWM, 90)

GPIO.output("P8_8",GPIO.HIGH)

to = time.clock()

while True:
    GPIO.output("P8_8", GPIO.LOW)
    time.sleep(2)
    GPIO.output("P8_8", GPIO.HIGH)
    time.sleep(2)

PWM.stop(myPWM)
PWM.cleanup()