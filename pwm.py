# API for the TI eQEP hardware driver I wrote

# We need OS operations for this
import os
import Adafruit_BBIO.GPIO as GPIO

class PWM(object):
    # Set the unit timer period of the PWM hardware
    def set_duty_cycle(self, pinPWM, duty_cycle):
        pwm = ""
        if(pinPWM == "P8_19"):
            pwm = "pwm5"
        else:
            pwm = "pwm6"

        # Open the mode attribute file
        attribute = open(self.path + "/" + pwm + "/duty_ns", "w")

        duty_cycle = duty_cycle*self.period/100
        # Write the desired mode into the file
        attribute.write(str(duty_cycle))

        # Close the file
        attribute.close()

    # Set the unit timer period of the PWM hardware
    def set_period(self, pinPWM, period):
        pwm = ""
        if(pinPWM == "P8_19"):
            pwm = "pwm5"
        else:
            pwm = "pwm6"

        # Open the mode attribute file
        attribute = open(self.path + "/" + pwm + "/period_ns", "w")
        print self.path + "/" + pwm + "/period_ns"

        self.period = period

        # Write the desired mode into the file
        attribute.write(str(self.period))

        # Close the file
        attribute.close()

    # Constructor - specify the path and the mode
    def __init__(self):
        self.path = "/sys/class/pwm"
        self.period = 0
        print "created"

    def stop(self, pinPWM):
        self.set_duty_cycle(pinPWM, 0)
