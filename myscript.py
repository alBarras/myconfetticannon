print('TeleConfettiCannon Script Started!')
from time import sleep
from firebase import firebase
from datetime import datetime
import pytz
tz_Spain = pytz.timezone('Europe/Madrid')

useLeds = True
timeBetweenChecks = 1
timeAfterDateForShooting = 60;  #time after which the confetti will still be shooted, after such amount of seconds, we'll consider it a miss (the cannon was not turned on when it was time for shooting so it does not shoot)
useServos = True
useTrigger = True
useSensor = True

LEDlecture_GPIOpin = 16
LEDconnected_GPIOpin = 20
LEDshoot_GPIOpin = 12
LEDdate_GPIOpin = 13
LEDtrigger_GPIOpin = 6
LEDsensor_GPIOpin = 19
SERVO_GPIOpin = 21
BUTTONtrigger_GPIOpin = 26
DETECTIONsensor_GPIOpin = 5

servoValueClosed = 2.5
servoValueOpen = 9

afterShootTotalCount = 2

fb_URL = "https://teleconfetticannon-default-rtdb.firebaseio.com/"

if useLeds or useServos or useTrigger or useSensor:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

if useTrigger:
    GPIO.setup(BUTTONtrigger_GPIOpin,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)  #el posem a input mode
        # GPIO.PUD_DOWN actiu si li arriben 3.3V, inactiu si li arriben <3.3V
        # GPIO.PUD_UP inactiu si li arriben 3.3V, actiu si li arriben <3.3V

if useSensor:
    GPIO.setup(DETECTIONsensor_GPIOpin,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)  #el posem a input mode

if useLeds:
    GPIO.setup(LEDlecture_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDconnected_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDshoot_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDdate_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDtrigger_GPIOpin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(LEDsensor_GPIOpin,GPIO.OUT,initial=GPIO.LOW)

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
        myfb = firebase.FirebaseApplication(fb_URL, None)
        myfb.put('/cannon_miki25','justshoot',"True")
        myfb.put('/cannon_miki25','justshoot',"False")
        myfb.put('/cannon_miki25','dateison',"False")
        myfb.put('/cannon_miki25','tempison',"False")
        myfb.put('/cannon_miki25','sensorison',"False")
        myfb.put('/cannon_miki25','date',"")
    else:
        print('\n--- ... unshoot ... ---')
        if useLeds:
            GPIO.output(LEDshoot_GPIOpin,GPIO.LOW)
    openServo(doShoot)

def getSdif(now, future):
    month_future = int(future[0:2])
    d_future = int(future[3:5])
    y_future = int(future[6:8])
    h_future = int(future[9:11])
    m_future = int(future[12:14])
    s_future = int(future[15:17])
    month_now = int(now[0:2])
    d_now = int(now[3:5])
    y_now = int(now[6:8])
    h_now = int(now[9:11])
    m_now = int(now[12:14])
    s_now = int(now[15:17])

    s_dif = 0
    if s_future-s_now>=0:
        s_dif = s_dif + s_future-s_now
    else:
        s_dif = s_dif + s_future
        s_dif = s_dif + 60-s_now
        m_future = m_future - 1
    if m_future-m_now>=0:
        s_dif = s_dif + (m_future-m_now)*60
    else:
        s_dif = s_dif + m_future*60
        s_dif = s_dif + (60-m_now)*60
        h_future = h_future - 1
    if h_future-h_now>=0:
        s_dif = s_dif + (h_future-h_now)*60*60
    else:
        s_dif = s_dif + h_future*60*60
        s_dif = s_dif + (24-h_now)*60*60
        d_future = d_future - 1
    if d_future-d_now>=0:
        s_dif = s_dif + (d_future-d_now)*60*60*24
    else:
        s_dif = s_dif + d_future*60*60*24
        s_dif = s_dif + (31-d_now)*60*60*24
        month_future = month_future - 1
    if month_future-month_now>=0:
        s_dif = s_dif + (month_future-month_now)*60*60*24*30
    else:
        s_dif = s_dif + month_future*60*60*24*30
        s_dif = s_dif + (13-month_now)*60*60*24*30
        y_future = y_future - 1
    if y_future-y_now>=0:
        s_dif = s_dif + (y_future-y_now)*60*60*24*30*12

    return s_dif

def main():
    lastLecture = True

    #Connect to Firebase
    connected = False
    useLeds = True
    while not connected:
        print('\n--- Will Try to Connect to Firebase ---')
        try:
            myfb = firebase.FirebaseApplication(fb_URL, None)
            myfb.put('/cannon_miki25','justshoot',"False")
        except:
            print('\n      NO INTERNET')
        else:
            print('\n      SUCCESS !!!')
            if useLeds:
                GPIO.output(LEDconnected_GPIOpin,GPIO.HIGH)
            connected = True
            lastLecture = not lastLecture
            myfb.put('/cannon_miki25','lastrasplecture',str(lastLecture))

    #Endless Loop
    justShooted = False
    afterShootCount = 0
    offlineTriggerIsOn = False
    offlineSensorIsOn = False
    sensorCounter = 0
    sensorCounterPeak = 3
    while True:
        print('\n--- NEW LECTURE ---')
        lastLecture = not lastLecture
        myfb.put('/cannon_miki25','lastrasplecture',str(lastLecture))

        if useLeds:
            openLectureLed(True)
            sleep(0.5)
            openLectureLed(False)

        if not justShooted:

            print("\nCheck ledsIsOn")
            ledsison = myfb.get('/cannon_miki25/ledsison', '')
            if ledsison=="True":
                if not useLeds:
                    useLeds = True
                    GPIO.output(LEDconnected_GPIOpin,GPIO.HIGH)
                    if offlineTriggerIsOn:
                        GPIO.output(LEDtrigger_GPIOpin,GPIO.HIGH)
                    if offlineSensorIsOn:
                        GPIO.output(LEDsensor_GPIOpin,GPIO.HIGH)
            else:
                if useLeds:
                    useLeds = False
                    GPIO.output(LEDconnected_GPIOpin,GPIO.LOW)
                    GPIO.output(LEDtrigger_GPIOpin,GPIO.LOW)
                    GPIO.output(LEDsensor_GPIOpin,GPIO.LOW)

            print("\nCheck triggerIsOn")
            triggerison = myfb.get('/cannon_miki25/triggerison', '')
            if triggerison=="True":
                if not offlineTriggerIsOn:
                    offlineTriggerIsOn = True
                    if useLeds:
                        GPIO.output(LEDtrigger_GPIOpin,GPIO.HIGH)
            else:
                if offlineTriggerIsOn:
                    offlineTriggerIsOn = False
                    if useLeds:
                        GPIO.output(LEDtrigger_GPIOpin,GPIO.LOW)
            if offlineTriggerIsOn and GPIO.input(BUTTONtrigger_GPIOpin):
                justShooted = True
                afterShootCount = 0
                shoot(True)

            else:


                print("\nCheck sensorIsOn")
                sensorison = myfb.get('/cannon_miki25/sensorison', '')
                if sensorison=="True":
                    if not offlineSensorIsOn:
                        offlineSensorIsOn = True
                        if useLeds:
                            GPIO.output(LEDsensor_GPIOpin,GPIO.HIGH)
                else:
                    if offlineSensorIsOn:
                        offlineSensorIsOn = False
                        if useLeds:
                            GPIO.output(LEDsensor_GPIOpin,GPIO.LOW)
                if offlineSensorIsOn and GPIO.input(DETECTIONsensor_GPIOpin):
                    sensorCounter = sensorCounter + 1
                    print ("Movement Detected, "+str(sensorCounter)+" of "+str(sensorCounterPeak))
                    if sensorCounter >= sensorCounterPeak:
                        print("As the sensor has detected movement "+str(sensorCounterPeak)+" times, it will now shoot!")
                        justShooted = True
                        afterShootCount = 0
                        shoot(True)


                else:
                    sensorCounter = 0




                    print("\n---START READING---")

                    #Read Firebase Values
                    justshoot = myfb.get('/cannon_miki25/justshoot', '')
                    tempison = myfb.get('/cannon_miki25/tempison', '')
                    dateison = myfb.get('/cannon_miki25/dateison', '')
                    date = myfb.get('/cannon_miki25/date', '')
                    print("justshoot: "+justshoot+", triggerison: "+triggerison+", sensorison: "+sensorison+", tempison: "+tempison+", dateison: "+dateison+", date: "+date)

                    #Check & Shoot
                    print("\nCheck justShoot")
                    if justshoot=="True":
                        justShooted = True
                        afterShootCount = 0
                        shoot(True)

                    print("\nCheck date/tempIsOn")
                    if dateison=="True" or tempison=="True":
                        if useLeds:
                            GPIO.output(LEDdate_GPIOpin,GPIO.HIGH)
                        now = datetime.now(tz_Spain).strftime("%D %H:%M:%S")
                        if now >= date: #if we have surpassed the shooting time
                            s_dif_afterwards = getSdif(date, now)
                            print("\ns_dif_afterwards: "+str(s_dif_afterwards)+", max is "+str(timeAfterDateForShooting))
                            if s_dif_afterwards <= timeAfterDateForShooting: #and we did not surpass it for too much time, shoot the confetti
                                justShooted = True
                                afterShootCount = 0
                                shoot(True)
                            else:   #if it is too long after the shooting time, just abort the shooting date as we missed it
                                myfb.put('/cannon_miki25','justshoot',"False")
                                myfb.put('/cannon_miki25','dateison',"False")
                                myfb.put('/cannon_miki25','tempison',"False")
                                myfb.put('/cannon_miki25','date',"")
                    elif useLeds:
                        GPIO.output(LEDdate_GPIOpin,GPIO.LOW)

                    print("\n---END READING---")

        else:
            afterShootCount = afterShootCount + 1
            print("\n--- AFTER SHOOT WAIT ---")
            if afterShootCount >= afterShootTotalCount-1:
                justShooted = False
                myfb.put('/cannon_miki25','justshoot',"False")
                shoot(False)

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
