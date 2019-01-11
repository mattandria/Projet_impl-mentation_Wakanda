from pwm import PWM


myPWM="P8_19"
pwmmm = PWM()
pwmmm.set_period(myPWM, 20000)
pwmmm.set_duty_cycle(myPWM, 0)

