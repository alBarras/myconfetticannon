print('TeleConfettiCannon Script Started!')
from time import sleep
from firebase import firebase
from datetime import datetime
import pytz
tz_Spain = pytz.timezone('Europe/Madrid')

timeBetweenChecks = 1
useLeds = True
useServos = True
useTrigger = True

LEDlecture_GPIOpin = 16
LEDconnected_GPIOpin = 20
LEDshoot_GPIOpin = 12
LEDdate_GPIOpin = 13
LEDtrigger_GPIOpin = 6
SERVO_GPIOpin = 21
BUTTONtrigger_GPIOpin = 26

servoValueClosed = 2.5
servoValueOpen = 9

afterShootTotalCount = 5

fb_URL = "https://teleconfetticannon-default-rtdb.firebaseio.com/"

if useLeds or useServos or useTrigger:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

if useTrigger:
    GPIO.setup(BUTTONtrigger_GPIOpin,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)  #el posem a input mode
        # GPIO.PUD_DOWN actiu si li arriben 3.3V, inactiu si li arriben <3.3V
        # GPIO.PUD_UP inactiu si li arriben 3.3V, actiu si li arriben <3.3V

if useLeds:
    GPIO.setup(LEDlecture_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDconnected_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDshoot_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDdate_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDtrigger_GPIOpin,GPIO.OUT,initial=GPIO.LOW)

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
        # myfb = firebase.FirebaseApplication(fb_URL, None)
        myfb.put('/cannon','justshoot',"True")
        myfb.put('/cannon','justshoot',"False")
        myfb.put('/cannon','dateison',"False")
        myfb.put('/cannon','tempison',"False")
        myfb.put('/cannon','date',"")
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
            triggerison = myfb.get('/cannon/triggerison', '')
            tempison = myfb.get('/cannon/tempison', '')
            dateison = myfb.get('/cannon/dateison', '')
            date = myfb.get('/cannon/date', '')
            print("justshoot: "+justshoot+", triggerison: "+triggerison+", tempison: "+tempison+", dateison: "+dateison+", date: "+date)

            #Check & Shoot
            if justshoot=="True":
                justShooted = True
                afterShootCount = 0
                shoot(True)

            if triggerison=="True":
                if useLeds:
                    GPIO.output(LEDtrigger_GPIOpin,GPIO.HIGH)
                if GPIO.input(BUTTONtrigger_GPIOpin):   #if button pressed, do shoot
                    shoot(True)
            elif useLeds:
                GPIO.output(LEDtrigger_GPIOpin,GPIO.LOW)

            if dateison=="True" or tempison=="True":
                if useLeds:
                    GPIO.output(LEDdate_GPIOpin,GPIO.HIGH)
                now = datetime.now(tz_Spain).strftime("%D %H:%M:%S")
                if now >= date:
                    shoot(True)
            elif useLeds:
                GPIO.output(LEDdate_GPIOpin,GPIO.LOW)

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
