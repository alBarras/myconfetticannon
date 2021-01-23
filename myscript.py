print('TeleConfettiCannon Script Started!')
from time import sleep

timeBetweenChecks = 3
useLeds = True
useServos = True

if useLeds or useServos:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

if useLeds:
    LEDlecture_GPIOpin = 16
    LEDconnected_GPIOpin = 20
    GPIO.setup(LEDlecture_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDconnected_GPIOpin,GPIO.OUT,initial=GPIO.LOW)

if useServos:
    SERVO_GPIOpin = 21
    import pigpio
    pi = pigpio.pi()
    pi.set_mode(SERVO_GPIOpin, pigpio.OUTPUT)

while True:
    GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
    pi.set_servo_pulsewidth(2,2500)
    sleep(timeBetweenChecks)
    GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
    pi.set_servo_pulsewidth(2,600)
    sleep(timeBetweenChecks)
    pi.set_servo_pulsewidth(2, 1500)
    sleep(timeBetweenChecks)
