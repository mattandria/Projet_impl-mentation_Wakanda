import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from time import sleep
from threading import Thread
import Adafruit_BBIO.Encoder as Encoder

old_A=0
old_B=0
count=0

pinA='P8_7'
pinB='P8_8'

GPIO.setup(pinA, GPIO.IN)
GPIO.setup(pinB, GPIO.IN)

def my_callback(channel):
        global old_A
        global old_B
        global count
        curr_A=GPIO.input(pinA)
        curr_B=GPIO.input(pinB)
        if not(curr_A==old_B):
                count=count-1
        else:
                count=count+1
        old_B=curr_B
        old_A=curr_A

# def callback_A(channel):
#         global count
#         curr_A=GPIO.input(pinA)
#         curr_B=GPIO.input(pinB)
#         if(curr_A==curr_B):
#                 count=count+1
#         else:
#                 count=count-1
                
# def callback_B(channel):
#         global count
#         curr_A=GPIO.input(pinA)
#         curr_B=GPIO.input(pinB)
#         if(curr_A==curr_B):
#                 count=count-1
#         else:
#                 count=count+1
                
# GPIO.add_event_detect(pinA,GPIO.BOTH,callback=callback_A)
# GPIO.add_event_detect(pinB,GPIO.BOTH,callback=callback_B)       

GPIO.add_event_detect(pinA,GPIO.BOTH,callback=my_callback)
GPIO.add_event_detect(pinB,GPIO.BOTH,callback=my_callback)
    
while(1):
        print count/4
        sleep(0.04)

class MyEncoder(Thread):
        """docstring for Encoder"""
        def __init__(self, pinA, pinB):
                Thread.__init__(self)
                self.pinA = pinA
                self.pinB = pinB
                self.encoder = Encoder.RotaryEncoder(Encoder.RotaryEncoder.EQEP2)
                self.encoder.setAbsolute()
                self.encoder.zero()

        def getPosition(self):
                return self.encoder.getPosition()
                