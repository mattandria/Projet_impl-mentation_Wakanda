export SLOTS=/sys/devices/platform/bone_capemgr/slots
echo cape-universaln > $SLOTS

#####Activate PWM######
export OCP3=/sys/devices/platform/ocp
echo pwm > $OCP3/ocp:P8_13_pinmux/state  #On met le Pin 8_13 en mode PWM
echo pwm > $OCP3/ocp:P8_19_pinmux/state  #On met le Pin 8_13 en mode PWM

#On fait correspondre le Pin au bon module PWM (grâce à son numéro)
export PWM=/sys/class/pwm/pwmchip6
echo 0 > $PWM/export #p8_19
echo 1 > $PWM/export #p8_13

echo 1 > $PWM/pwm0/enable
echo 1 > $PWM/pwm1/enable

#Activate P8_11 && P8_12 pins for the encoder
echo qep > $OCP3/ocp:P8_11_pinmux/state
echo qep > $OCP3/ocp:P8_12_pinmux/state
echo qep > $OCP3/ocp:P9_27_pinmux/state
echo qep > $OCP3/ocp:P9_92_pinmux/state
