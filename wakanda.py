#from controller import Controller
from math import sqrt, acos, cos, atan2, pow

class Wakanda(object):
	#initialisation
	def __init__(self, periodPWM, periodEncoders):
		#self.controller = Controller(1000000, 100000000, "P8_13", "P8_8", "P8_19", "P8_17")
		self.og = [-10,0]
		self.od = [10,0]
		self.l1 = 60
		self.l2 = 80

	#DETERMINE THE DESIRED ORIENTATION OF THE MOTORS WRT A DESIRED POSE
	def modeleInverse(self, x, y):
		dg = sqrt( pow( x - self.og[0], 2) + pow(y, 2) )
		dd = sqrt( pow(x - self.od[0], 2) + pow(y,2) )
		thetad = atan2( y/dd, (x - self.od[0])/dd )
		thetag = atan2( y/dg, (x - self.og[0])/dg )


		d1 = pow(x - self.od[0], 2) + pow(y, 2) - pow(self.l1, 2) - pow(self.l2, 2)
		d2 = pow(x - self.og[0], 2) + pow(y, 2) - pow(self.l1, 2) - pow(self.l2, 2)

		print d1
		print d2

		if abs(d1) < 2*self.l1*self.l2 and abs(d2) < 2*self.l1*self.l2 :
			betad = acos( d1/(2*self.l1*self.l2) )
			betag = acos( d2/(2*self.l1*self.l2) )
			phid = acos( (self.l1 + self.l2*cos(betad)) / dd )
			phig = acos( (self.l1 + self.l2*cos(betag)) / dg )
			theta1 = thetag + phig
			theta2 = thetad - phid

			print "theta1 = {}, theta2 = {}".format(theta1, theta2)

			return [theta1, theta2]
		else:
			print "unreachable position"
			return []


wakanda = Wakanda(10, 10)
x = 20
y = 30
wakanda.modeleInverse(x, y)
