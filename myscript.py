print('TeleConfettiCannon Script Started!')
from time import sleep
from firebase import firebase

timeBetweenChecks = 1
useLeds = True
useServos = True

LEDlecture_GPIOpin = 16
LEDconnected_GPIOpin = 20
LEDshoot_GPIOpin = 12
SERVO_GPIOpin = 21

servoValueClosed = 2.5
servoValueOpen = 12.5

afterShootTotalCount = 5

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

def shoot(doShoot):
    if doShoot:
        print('\n--- !!! SHOOT !!! ---')
        if useLeds:
            GPIO.output(LEDshoot_GPIOpin,GPIO.HIGH)
    else:
        print('\n--- ... unshoot ... ---')
        if useLeds:
            GPIO.output(LEDshoot_GPIOpin,GPIO.LOW)
    openServo(doShoot)

def main():

    #Connect to Firebase
    connected = False
    while not connected:
        print('\n--- Will Try to Connect to Firebase ---')
        try:
            myfb = firebase.FirebaseApplication(fb_URL, None)
            myfb.put('/cannon','justshoot',"False")
        except:
            print('\n      NO INTERNET')
        else:
            print('\n      SUCCESS !!!')
            if useLeds:
                GPIO.output(LEDconnected_GPIOpin,GPIO.HIGH)
            connected = True

    #Endless Loop
    justShooted = False
    afterShootCount = 0
    while True:
        print('\n--- NEW FIREBASE READING ---')
        if useLeds:
            openLectureLed(True)

        if not justShooted:
            #Read Firebase Values
            justshoot = myfb.get('/cannon/justshoot', '')
            buttonison = myfb.get('/cannon/buttonison', '')
            dateison = myfb.get('/cannon/dateison', '')
            print("justshoot: "+justshoot+", buttonison: "+buttonison+", dateison: "+dateison)

            #Check & Shoot
            if justshoot=="True":
                justShooted = True
                afterShootCount = 0
                shoot(True)
            # if buttonison=="True":
            #     if GPIOdetectedINPUT:
            #         shoot(True)
            # if dateison=="True":
            #     if nowIsLaterThanSuchDate:
            #         shoot(True)
        else:
            afterShootCount = afterShootCount + 1
            print("\n--- AFTER SHOOT WAIT ---")
            if afterShootCount >= afterShootTotalCount-1:
                justShooted = False
                myfb.put('/cannon','justshoot',"False")
                shoot(False)

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
