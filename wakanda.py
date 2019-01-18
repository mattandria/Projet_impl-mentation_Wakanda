from controller import Controller
from math import sqrt, acos, cos, atan2, pow
import math

## \brief Classe principale responsable du suivi de trajectoire
# @param period The unit timer period of the eQEP hardware
class Wakanda(object):

        ## \brief Constructor
        def __init__(self):
                self.controller = Controller("P8_13", "P8_8", "P8_19", "P8_17") #controller 
                self.controller.start() #launch of the controller thread
                self.controller.join() 

                self.og = [-12.5,0] #Coordinates of the fixing point of the left motor
                self.od = [12.5,0] #Coordinates of the fixing point of the right motor
                self.l1 = 60 #Length of the first rod in mm
                self.l2 = 80 #Length of the second rod in mm (effector)

                self.positions = [] #Array of positions of the trajectory

        ## \brief Function computing the angular positions of the motors required to place the effector at (x,y)
        # @param x,y Position of the effector
        # @return An array containing the angles of the left and right motors. If the given position is unreachable, the function returns an empty array
        def modeleInverse(self, x, y):
                dg = sqrt( pow( x - self.og[0], 2) + pow(y, 2) )
                dd = sqrt( pow(x - self.od[0], 2) + pow(y,2) )
                thetad = atan2( y/dd, (x - self.od[0])/dd )
                thetag = atan2( y/dg, (x - self.og[0])/dg )

                d1 = pow(x - self.od[0], 2) + pow(y, 2) - pow(self.l1, 2) - pow(self.l2, 2)
                d2 = pow(x - self.og[0], 2) + pow(y, 2) - pow(self.l1, 2) - pow(self.l2, 2)

                if abs(d1) < 2*self.l1*self.l2 and abs(d2) < 2*self.l1*self.l2 :
                        betad = acos( d1/(2*self.l1*self.l2) )
                        betag = acos( d2/(2*self.l1*self.l2) )
                        phid = acos( (self.l1 + self.l2*cos(betad)) / dd )
                        phig = acos( (self.l1 + self.l2*cos(betag)) / dg )
                        theta1 = thetag + phig
                        theta2 = thetad - phid

                        print "theta1 = {}, theta2 = {}".format(theta1, theta2)

                        return [theta1, theta2] #angles of the motor (theta1 for the left one, theta2 for the right one)
                else:
                        print "unreachable position"
                        return [] #returns an empty array if the position is not reachable

        ## \brief Function verifying if the position targeted by the controller is reached with an given error
        # @param error Maximal value of the command to consider that the target for the controller is reached
        # @return True if the position is reached, False otherwise
        def isReached(error):
                cmd=0
                return (self.controller.regulateCmd(1,cmd)<error)&&(self.controller.regulateCmd(2,cmd)<error)


"""wakanda = Wakanda() #Instantiation of a Wakanda
x=100
y=0
angles = wakanda.modeleInverse(x, y)
if(len(angles) != 0):   #si la position est atteignable
        wakanda.controller.setDes(angles[0], angles[1])
        while True:
                wakanda.controller.execute()"""

wakanda = Wakanda() #Instantiation of a Wakanda
i=0 #index of the current target
list=[]
while i!=len(list): #while the path is not finished 
        angles=wakanda.modeleInverse(list[i],list[i+1])
        if len(angles)!=0: #if the position is reachable
                wakanda.controller.setDes(angles[0],angles[1]) #Setting the controller target
                wakanda.controller.execute() #We run the controller
                if wakanda.controller.isReached(10): #if the position is reached, the target of the controller switches to the next point of the path
                        i+=2
        else:
                i+=2 #next point of the path

