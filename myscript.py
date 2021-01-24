print('TeleConfettiCannon Script Started!')
from time import sleep

timeBetweenChecks = 3
useLeds = True
useServos = True

LEDlecture_GPIOpin = 16
LEDconnected_GPIOpin = 20
SERVO_GPIOpin = 21

servoValueClosed = 2.5
servoValueOpen = 12.5

if useLeds or useServos:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

if useLeds:
    GPIO.setup(LEDlecture_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDconnected_GPIOpin,GPIO.OUT,initial=GPIO.LOW)

def openLed(doOpen):
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



from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
fb_url = 'https://teleconfetticannon-default-rtdb.firebaseio.com'
fb_dir = '/cannon1/'
credentials_path = "/home/pi/myconfetticannon/teleconfetticannon-firebase-adminsdk-3ho19-01b30e179c.json"


def connectFirebase():
    try:
        fb = firebase.FirebaseApplication(fb_url, authentication = None)
        cred = credentials.Certificate("/home/pi/mytransponder/mytransponder-ppl-firebase-adminsdk-c1kdd-fae40838ec.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL' : fb_url
        })
        root = db.reference()
    except:
        print('\n--- Waiting for Internet ---')
        return False
    else:
        if useLeds:
            GPIO.output(LEDconnected_GPIOpin,GPIO.HIGH)
        return True


def main():
    while not connectFirebase():
        sleep(2)
    while True:
        openLed(True)
        ref = db.reference(fb_url+fb_dir+'justshoot')
        print(ref.get())
        sleep(2)
        openLed(False)
        sleep(5)








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
