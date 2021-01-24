print('TeleConfettiCannon Script Started!')
from time import sleep
from firebase import firebase

timeBetweenChecks = 5
useLeds = True
useServos = True

LEDlecture_GPIOpin = 16
LEDconnected_GPIOpin = 20
LEDshoot_GPIOpin = 12
SERVO_GPIOpin = 21

servoValueClosed = 2.5
servoValueOpen = 12.5

fb_URL = "https://teleconfetticannon-default-rtdb.firebaseio.com/"

if useLeds or useServos:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

if useLeds:
    GPIO.setup(LEDlecture_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDconnected_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDshoot_GPIOpin,GPIO.OUT,initial=GPIO.LOW)

def openLectureLed(doOpen):
    if doOpen:
        GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
    else:
        GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)

if useServos:
    GPIO.setup(SERVO_GPIOpin, GPIO.OUT)
    p = GPIO.PWM(SERVO_GPIOpin, 50)
    p.start(servoValueClosed)

def openServo(doOpen):
    if doOpen:
        p.ChangeDutyCycle(servoValueOpen)
    else:
        p.ChangeDutyCycle(servoValueClosed)

justShooted = False
def shoot(doShoot):
    if doShoot:
        print('\n--- !!! SHOOT !!! ---')
        if useLeds:
            GPIO.output(LEDshoot_GPIOpin,GPIO.HIGH)
    else:
        print('\n--- ... unshoot ... ---')
        if useLeds:
            GPIO.output(LEDshoot_GPIOpin,GPIO.LOW)
    justShooted = doShoot
    openServo(doShoot)

def main():

    #Connect to Firebase
    connected = False
    while not connected:
        print('\n--- Will Try to Connect to Firebase ---')
        try:
            lol = firebase.FirebaseApplication(fb_URL, None)
        except:
            print('\n      NO INTERNET')
        else:
            print('\n      SUCCESS !!!')
            if useLeds:
                GPIO.output(LEDconnected_GPIOpin,GPIO.HIGH)
            connected = True

    #Endless Loop
    while True:
        print('\n--- NEW FIREBASE READING ---')
        if useLeds:
            openLectureLed(True)

        #Read Firebase Values
        justshoot = lol.get('/cannon/justshoot', '')
        buttonison = lol.get('/cannon/buttonison', '')
        dateison = lol.get('/cannon/dateison', '')
        print("justshoot: "+justshoot+", buttonison: "+buttonison+", dateison: "+dateison)

        if justShooted:
            shoot(False)

        #Check & Shoot
        if justshoot=="True":
            shoot(True)
        # if buttonison=="True":
        #     if GPIOdetectedINPUT:
        #         shoot(True)
        # if dateison=="True":
        #     if nowIsLaterThanSuchDate:
        #         shoot(True)

        #Led Feedback
        if useLeds:
            sleep(1)
            openLectureLed(False)
            sleep(timeBetweenChecks-1)
        else:
            sleep(timeBetweenChecks)

main()





    # SERVO EXAMPLES
    # GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
    # p.ChangeDutyCycle(5)
    # sleep(0.5)
    # GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
    # p.ChangeDutyCycle(7.5)
    # sleep(0.5)
    # GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
    # p.ChangeDutyCycle(10)
    # sleep(0.5)
    # GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
    # p.ChangeDutyCycle(12.5)
    # sleep(0.5)
    # GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
    # p.ChangeDutyCycle(10)
    # sleep(0.5)
    # GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
    # p.ChangeDutyCycle(7.5)
    # sleep(0.5)
    # GPIO.output(LEDlecture_GPIOpin,GPIO.HIGH)
    # p.ChangeDutyCycle(5)
    # sleep(0.5)
    # GPIO.output(LEDlecture_GPIOpin,GPIO.LOW)
    # p.ChangeDutyCycle(2.5)
    # sleep(0.5)
