import os # We need OS operations for this

## \brief Classe permettant de gerer le module PWM
class PWM(object):

    ## \brief Definit le duty_cycle
    # @param pinPWM Le pin de PWM
    # @param duty_cycle La valeur du duty_cycle souhaite
    def set_duty_cycle(self, pinPWM, duty_cycle):
        #On ecrit dans le bon dossier en fonction du pin de PWM
        pwm = ""
        if(pinPWM == "P8_19"):
            pwm = "pwm0"
        else:
            pwm = "pwm1"

        attribute = open(self.path + "/" + pwm + "/duty_cycle", "w")    #Ouvre le fichier

        duty_cycle = duty_cycle*self.period/100 #On convertit le duty_cycle en pourcentage
        print "duty_cycle: {}".format(duty_cycle)

        attribute.write(str(duty_cycle))    #Ecrit la valeur desiree dans le fichier

        attribute.close()   #On ferme le fichier

    ## \brief Definit la periode du PWM
    # @param pinPWM Le pin de PWM
    # @param period La valeur de la periode souhaitee
    def set_period(self, pinPWM, period):
        #On ecrit dans le bon dossier en fonction du pin de PWM
        pwm = ""
        if(pinPWM == "P8_19"):
            pwm = "pwm0"
        else:
            pwm = "pwm1"

        attribute = open(self.path + "/" + pwm + "/period", "w")    #Ouvre le fichier

        self.period = period

        attribute.write(str(self.period))   # Ecrit la valeur desiree dans le fichier

        attribute.close()   #ferme le fichier

    ## \brief Constructor
    def __init__(self):
        self.path = "/sys/class/pwm/pwmchip6"    #Chemin qui permet d'acceder aux pwm utilises
        self.period = 0

    ## \brief Envoie un duty_cycle de 0
    # @param pinPWM Le pin de PWM
    def stop(self, pinPWM):
        self.set_duty_cycle(pinPWM, 0)
