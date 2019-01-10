#import Adafruit_BBIO.PWM as PWM
from pwm import PWM
import Adafruit_BBIO.GPIO as GPIO
import time
from eqep import eQEP
from threading import Thread

class Controller(Thread):
	#INITIALISATION
	def __init__(self, pinPWM1, pinDir1, pinPWM2, pinDir2):
		Thread.__init__(self)

		#Encodeurs
		self.encoder1 = eQEP("/sys/devices/ocp.3/48304000.epwmss/48304180.eqep", eQEP.MODE_ABSOLUTE)
		self.encoder1.set_period(40000)
		self.encoder2 = eQEP("/sys/devices/ocp.3/48300000.epwmss/48300180.eqep", eQEP.MODE_ABSOLUTE)
		self.encoder2.set_period(40000)

		#PWMs
		self.pinPWM1 = "P8_19"
		self.pinDir1 = pinDir1
		self.pinPWM2 = pinPWM2
		self.pinDir2 = pinDir2

#		PWM.start(self.pinPWM1, 0, periodPWM)
#		PWM.start(self.pinPWM2, 0, periodPWM)
		self.PWM = PWM()
		self.PWM.set_period(pinPWM1, 20000)
		self.PWM.set_period(pinPWM2, 20000)

		#GPIO setup
		self.GPIO = GPIO
		self.GPIO.setup(pinDir1, GPIO.OUT)
		self.GPIO.setup(pinDir2, GPIO.OUT)

		#PID
		self.Kp = 10
		self.Kd = 0
		self.Ki = 0
		self.lastError1 = 0
		self.totalError1 = 0
		self.lastError2 = 0
		self.totalError2 = 0

	#SEND COMMAND TO A MOTOR
	def sendCmd(self, motor, val):
		val = int(val)
		print "valeur envoyee: {}".format(val)
		if(motor == 1):
			self.PWM.set_duty_cycle(self.pinPWM1, val)
		else:
			self.PWM.set_duty_cycle(self.pinPWM2, val)

	#CALCULATE THE COMMAND TO SEND TO EACH MOTOR
	def execute(self):
		#PID FOR MOTOR1
		error1 = self.des1 - self.encoder1.poll_position()/4
		print "erreur1: {}".format(error1)
		pTerm1 = self.Kp*error1
		dTerm1 = self.Kd*(error1 - self.lastError1)
		self.totalError1+= error1
		iTerm1 = self.Ki*self.totalError1
		lastError1 = error1
		cmd1 = pTerm1 + dTerm1 + iTerm1

		self.sendCmd(1, self.regulateCmd(1, cmd1))


		#PID FOR MOTOR2
		error2 = self.des2 - self.encoder2.poll_position()/4
		print "erreur2: {}".format(error2)
		pTerm2 = self.Kp*error2
		dTerm2 = self.Kd*(error2 - self.lastError2)
		self.totalError2 += error2
		iTerm2 = self.Ki*self.totalError2
		lastError2 = error2
		cmd2 = pTerm2 + dTerm2 + iTerm2

		self.sendCmd(2, self.regulateCmd(2, cmd2))


	#STOP BOTH MOTORS
	def stop(self):
		self.sendCmd(1, 0)
		self.sendCmd(2, 0)

	#SET A NEW DESIRED MOTOR ORIENTATION
	def setDes(self, val1, val2):
		self.des1 = val1*180/3.1415
		self.des2 = val2*180/3.1415

	#REGULATE THE COMMAND AND THE MOTOR DIRECTION
	def regulateCmd(self, motor, cmd):
		pinDir = self.pinDir1
		if(motor == 2):
			pinDir = self.pinDir2

		if(cmd > 0):
			self.GPIO.output(pinDir, self.GPIO.HIGH)
			if(cmd > 100):	#le duty_cycle ne peut pas depasser la valeur de la periode
				cmd = 100
		elif(cmd < 0):
			self.GPIO.output(pinDir, self.GPIO.LOW)
			cmd *= -1	#le duty cycle doit etre positif
			if(cmd > 100):
				cmd = 100
		return cmd

