print('Firebase Script Started!')
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

timeBetweenChecks = 1
useLeds = True
useServos = False

LEDlecture_GPIOpin = 16
LEDconnected_GPIOpin = 20
SERVO_GPIOpin = 21

#LED (feedback)
if useLeds:
    GPIO.setup(LEDlecture_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDconnected_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
if useServos:
    GPIO.setup(SERVO_GPIOpin,GPIO.OUT,initial=GPIO.LOW)

while True:
    GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
    sleep(timeBetweenChecks)
    GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
    sleep(timeBetweenChecks)
