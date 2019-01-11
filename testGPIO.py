from pwm import PWM
import Adafruit_BBIO.GPIO as GPIO
import time

pinPWM = "P8_19"
pinDir = "P8_17"
pinLu = "P8_8"

pwmm = PWM()
pwmm.set_period(pinPWM, 20000)
pwmm.set_duty_cycle(pinPWM, 50)

GPIO.setup(pinDir, GPIO.OUT)
GPIO.setup(pinLu, GPIO.IN)

while(True):
	GPIO.output(pinDir, GPIO.HIGH)
"""	GPIO.output(pinDir, GPIO.LOW)
	print "GPIO: {}".format(GPIO.input(pinLu))
	time.sleep(4)
	pwmm.set_duty_cycle(pinPWM,0)
	pwmm.set_duty_cycle(pinPWM,50)

	GPIO.output(pinDir, GPIO.HIGH)
	print "GPIO: {}".format(GPIO.input(pinLu))
	time.sleep(4)
	pwmm.set_duty_cycle(pinPWM,0)
	pwmm.set_duty_cycle(pinPWM,50)"""
	

