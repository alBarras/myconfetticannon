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

# if useServos:
#     SERVO_GPIOpin = 21
#     import pigpio
#     pi = pigpio.pi()
#     pi.set_mode(SERVO_GPIOpin, pigpio.OUTPUT)
#
# while True:
#     GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
#     pi.set_servo_pulsewidth(2,2500)
#     sleep(timeBetweenChecks)
#     GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
#     pi.set_servo_pulsewidth(2,600)
#     sleep(timeBetweenChecks)
#     pi.set_servo_pulsewidth(2, 1500)
#     sleep(timeBetweenChecks)


servoPIN = 21
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization

try:
    while True:
        GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
        p.ChangeDutyCycle(5)
        sleep(0.5)
        GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
        p.ChangeDutyCycle(7.5)
        sleep(0.5)
        GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
        p.ChangeDutyCycle(10)
        sleep(0.5)
        GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
        p.ChangeDutyCycle(12.5)
        sleep(0.5)
        GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
        p.ChangeDutyCycle(10)
        sleep(0.5)
        GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
        p.ChangeDutyCycle(7.5)
        sleep(0.5)
        GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
        p.ChangeDutyCycle(5)
        sleep(0.5)
        GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
        p.ChangeDutyCycle(2.5)
        sleep(0.5)

# except KeyboardInterrupt:
#     p.stop()
#     GPIO.cleanup()
