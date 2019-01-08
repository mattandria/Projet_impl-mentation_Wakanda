export SLOTS=/sys/devices/bone_capemgr.9/slots
echo cape-universaln > $SLOTS

#####Activate PWM######
export OCP3=/sys/devices/ocp.3
echo pwm > $OCP3/P8_13_pinmux.21/state  #On met le Pin 8_13 en mode PWM
echo pwm > $OCP3/P8_19_pinmux.27/state  #On met le Pin 8_13 en mode PWM

#On fait correspondre le Pin au bon module PWM (grâce à son numéro)
export PWM=/sys/class/pwm/
echo 5 > $PWM/export #p8_19
echo 6 > $PWM/export #p8_13

echo 1 > $PWM/pwm5/run
echo 1 > $PWM/pwm6/run

#Activate P8_11 && P8_12 pins for the encoder
echo qep > $OCP3/P8_11_pinmux.19/state
echo qep > $OCP3/P8_12_pinmux.20/state
