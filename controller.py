from pwm import PWM
import Adafruit_BBIO.GPIO as GPIO
import time
from eqep import eQEP
from threading import Thread
import math

## \brief Classe permettant de controler les moteurs grace a un PID (un PID pour chaque moteur)
class Controller(Thread):
        ## \brief Constructeur, on va y initialiser les pins pour le PWM et pour la direction pour chaque moteur
        # @param pinPWM1 Le pin de PWM du moteur 1
        # @param pinDir1 Le pin de direction du moteur 1
        # @param pinPWM2 Le pin de PWM du moteur 2
        # @param pinDir2 Le pin de direction du moteur 2

        #INITIALISATION
        def __init__(self, pinPWM1, pinDir1, pinPWM2, pinDir2):
                Thread.__init__(self)

                #Encodeurs: on specifie le dossier dans lequel on va lire la position du moteur
                self.encoder1 = eQEP("/sys/devices/platform/ocp/48304000.epwmss/48304180.eqep", eQEP.MODE_ABSOLUTE) #chemin vers position encodeur 1
                self.encoder1.set_period(20000)         #periode d'echantillonage a 20000 nanosecondes
                self.encoder1.set_position(90*4)        #moteur 1 a 90 degres
                self.encoder2 = eQEP("/sys/devices/platform/ocp/48300000.epwmss/48300180.eqep", eQEP.MODE_ABSOLUTE) #chemin vers position encodeur 2
                self.encoder2.set_period(20000)         #periode d'echantillonage a 20000 nanosecondes  
                self.encoder2.set_position(90*4)        #on place le moteur 2 a 90 degres

                #PWMs: on fait correspondre les differents pins entrés en argument
                self.pinPWM1 = pinPWM1
                self.pinDir1 = pinDir1
                self.pinPWM2 = pinPWM2
                self.pinDir2 = pinDir2

                self.PWM = PWM()                        
                self.PWM.set_period(pinPWM1, 20000)     #les deux pins PWM envoient un signal de periode 20000 nanosecondes
                self.PWM.set_period(pinPWM2, 20000)

                #GPIO setup
                self.GPIO = GPIO
                self.GPIO.setup(pinDir1, GPIO.OUT)      #on specifie que les deux pins GPIO (de direction) sont en OUTPUT
                self.GPIO.setup(pinDir2, GPIO.OUT)

                #PID: on initialise les gains des PID 
                self.Kp = 0.5
                self.Kd = 0
                self.Ki = 0
                self.lastError1 = 0
                self.totalError1 = 0
                self.lastError2 = 0
                self.totalError2 = 0


        ## \brief Envoie la commande entrée en argument a un moteur
        # @param motor Le moteur auquel on va envoyer la commande
        # @param val Valeur de la commande a envoyer (en pourcentage, faisant reference au duty cycle)

        #SEND COMMAND TO A MOTOR
        def sendCmd(self, motor, val):
                val = int(val)
                print "valeur envoyee: {}".format(val)
                if(motor == 1):                         #pour le moteur 1
                        self.PWM.set_duty_cycle(self.pinPWM1, val)
                else:                                   #pour le moteur 2
                        self.PWM.set_duty_cycle(self.pinPWM2, val)


        ## \brief Calcule la valeur de la commande a envoyer grace a un PID

        #CALCULATE THE COMMAND TO SEND TO EACH MOTOR
        def execute(self):
                print "angles desires: {}, {}".format(self.des1, self.des2)

                #PID FOR MOTOR1
                print "position courante 1 = {}".format(self.encoder1.poll_position())
                error1 = (2 * (self.des1 - (int(self.encoder1.poll_position()/4))%360)) % 360   #erreur
                print "erreur1: {}".format(error1)
                pTerm1 = self.Kp*error1                     #terme proportionnel
                print "pTerm1: {}".format(pTerm1)
                dTerm1 = self.Kd*(error1 - self.lastError1) #terme derive
                self.totalError1+= error1

                iTerm1 = self.Ki*self.totalError1           #terme integral (qu'on sature)
                if(iTerm1 > 10):
                        iTerm1 = 10
                if(iTerm1 < -10):
                        iTerm1 = -10

                lastError1 = error1
                cmd1 = pTerm1# + iTerm1

                # On envoie la commande apres en avoir fait une regulation 
                self.sendCmd(1, self.regulateCmd(1, cmd1))
                print "iTerm1: {}".format(iTerm1)

                #PID FOR MOTOR2
                print "position courante 2 = {}".format(self.encoder2.poll_position())
                error2 = (2 * (self.des2 - (self.encoder2.poll_position()/4)%360)) % 360
                print "erreur2: {}".format(error2)
                pTerm2 = self.Kp*error2                     #terme proportionnel                         
                dTerm2 = self.Kd*(error2 - self.lastError2) #terme derive
                self.totalError2 += error2
                iTerm2 = self.Ki*self.totalError2           #terme integral (qu'on sature)
                if(iTerm2 > 10):
                        iTerm2 = 10
                if(iTerm2 < -10):
                        iTerm2 = -10

                lastError2 = error2
                cmd2 = pTerm2 #+ dTerm2# + iTerm2

                # On envoie la commande apres en avoir fait une regulation
                self.sendCmd(2, self.regulateCmd(2, cmd2))


        ## \brief Arrete les deux moteurs

        #STOP BOTH MOTORS
        def stop(self):
                self.sendCmd(1, 0)
                self.sendCmd(2, 0)


        ## \brief Definit une nouvelle position angulaire a atteindre pour les deux moteurs
        # @param val1 Valeur de la commande pour le moteur 1
        # @param val1 Valeur de la commande pour le moteur 2

        #SET A NEW DESIRED MOTOR ORIENTATION
        def setDes(self, val1, val2):
                self.des1 = int(val1*180/math.pi)
                self.des2 = int(val2*180/math.pi)
                print "angles desires: {}, {}".format(self.des1, self.des2)


        ## \brief Effectue la regulation des commandes a envoyer a un moteur en les mettant sous forme de pourcentage
        # @param motor Le moteur auquel on va envoyer la commande
        # @param cmd Valeur de la commande a envoyer 

        #REGULATE THE COMMAND AND THE MOTOR DIRECTION
        def regulateCmd(self, motor, cmd):
                pinDir = self.pinDir1
                if(motor == 2):
                        pinDir = self.pinDir2

                if(cmd > 0):
                        self.GPIO.output(pinDir, self.GPIO.HIGH)        #si la commmande est positive, mettre le GPIO a HIGH
                        print "commande positive"
                elif(cmd < 0):
                        self.GPIO.output(pinDir, self.GPIO.LOW)         #si la commmande est negative, mettre le GPIO a LOW
                        cmd *= -1       #le duty cycle doit etre positif
                        print "commande negative"

                cmd = min(cmd, 100)     #le duty_cycle ne doit pas etre superieur a la periode
                if(motor==1):
                        print "commande 1 = {}".format(cmd)
                else:
                        print "commande 2 = {}".format(cmd)
                return cmd
