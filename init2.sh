export SLOTS=/sys/devices/bone_capemgr.9/slots
echo cape-universaln > $SLOTS

#####Activate PWM######
#On met le Pin 8_13 en mode PWM
cd /sys/devices/ocp.3/P8_13_pinmux.21/
echo pwm > state  

cd .. && cd 48304000.epwmss/48304200.ehrpwm/pwm/pwmchip5/

#On fait correspondre le Pin au bon module PWM (grâce à son numéro)
cd /sys/class/pwm/
echo 5 > export
echo 6 > export


#Activate P8_11 && P8_12 pins for the encoder
cd /sys/devices/ocp.3/P8_11_pinmux.19/
echo qep > state
cd /sys/devices/ocp.3/P8_12_pinmux.20/
echo qep > state
