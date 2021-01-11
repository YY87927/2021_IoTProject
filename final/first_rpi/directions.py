import RPi.GPIO as GPIO
import time  

TRIGGER_PINL = 31
ECHO_PINL = 29
TRIGGER_PINR = 11
ECHO_PINR = 13
ENA = 10
ENB = 12
FREQ = 100

Forward1 = 37
Backward1 = 38
Forward2 = 15
Backward2 = 16
auto_speed = 25
auto_turn_speed = 40
manual_speed = 40
manual_turn_speed = 50

LIGHT_SENSE = 10
LED_PIN = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(TRIGGER_PINL, GPIO.OUT)
GPIO.setup(ECHO_PINL,GPIO.IN)
GPIO.setup(TRIGGER_PINR, GPIO.OUT)
GPIO.setup(ECHO_PINR,GPIO.IN)
GPIO.setup(Forward1, GPIO.OUT)
GPIO.setup(Backward1, GPIO.OUT)
GPIO.setup(Forward2, GPIO.OUT)
GPIO.setup(Backward2, GPIO.OUT)
GPIO.setup(ENA,GPIO.OUT) #ENA
GPIO.setup(ENB,GPIO.OUT) #ENB
motor1GPIO = GPIO.PWM(ENA, FREQ)
motor1GPIO.start(0)
motor2GPIO = GPIO.PWM(ENB, FREQ)
motor2GPIO.start(0)

GPIO.setup(LED_PIN, GPIO.OUT)

def stop():
    print("stop!!!")
    GPIO.output(Forward1, GPIO.LOW)
    GPIO.output(Forward2, GPIO.LOW)
    GPIO.output(Backward1, GPIO.LOW)
    GPIO.output(Backward2, GPIO.LOW)

def forward():
    GPIO.output(Forward1, GPIO.HIGH)
    GPIO.output(Forward2, GPIO.HIGH)
    GPIO.output(Backward1, GPIO.LOW)
    GPIO.output(Backward2, GPIO.LOW)
    print("Moving Forward")
    

def backward():
    GPIO.output(Backward1, GPIO.HIGH)
    GPIO.output(Backward2, GPIO.HIGH)
    GPIO.output(Forward1, GPIO.LOW)
    GPIO.output(Forward2, GPIO.LOW)
    print("Moving Backward")
    
def turn_right():
    GPIO.output(Forward1, GPIO.HIGH)
    GPIO.output(Forward2, GPIO.LOW)
    GPIO.output(Backward1, GPIO.LOW)
    GPIO.output(Backward2, GPIO.HIGH)
    print("turning right")

def turn_left():
    GPIO.output(Forward2, GPIO.HIGH)
    GPIO.output(Forward1, GPIO.LOW)
    GPIO.output(Backward1, GPIO.HIGH)
    GPIO.output(Backward2, GPIO.LOW)
    print("turning left")

def manual_control(response):
    if response=='w':
        motor1GPIO.ChangeDutyCycle(manual_speed)   # left
        motor2GPIO.ChangeDutyCycle(manual_speed)  # right
        forward()
    elif response=='s':
        motor1GPIO.ChangeDutyCycle(manual_speed)   # left
        motor2GPIO.ChangeDutyCycle(manual_speed)  # right
        backward()
    elif response=='a':
        motor1GPIO.ChangeDutyCycle(manual_turn_speed)   # left
        motor2GPIO.ChangeDutyCycle(manual_turn_speed)  # right
        turn_right()
    elif response=='d':
        motor1GPIO.ChangeDutyCycle(manual_turn_speed)   # left
        motor2GPIO.ChangeDutyCycle(manual_turn_speed)  # right
        turn_left()
    elif response=="Key.space":
        stop()

def auto_pilot(response, distanceR, distanceL, old_distanceR, old_distanceL, turn):
    if (distanceR > old_distanceR + 0.5 or distanceL > old_distanceL + 0.5)\
        and turn == False:
        motor1GPIO.ChangeDutyCycle(auto_speed)
        motor2GPIO.ChangeDutyCycle(auto_speed)
        backward()
        turn = False
        time.sleep(1)
    elif (distanceR < old_distanceR - 50) or (distanceL < old_distanceL - 50):
        motor1GPIO.ChangeDutyCycle(auto_speed)
        motor2GPIO.ChangeDutyCycle(auto_speed)
        backward()
        time.sleep(1)
    if response=='w':
        motor1GPIO.ChangeDutyCycle(auto_speed)
        motor2GPIO.ChangeDutyCycle(auto_speed)
        forward()
        turn = False
        time.sleep(.7)
    elif response=='s':
        motor1GPIO.ChangeDutyCycle(auto_speed)
        motor2GPIO.ChangeDutyCycle(auto_speed)
        backward()
        turn = False
        time.sleep(.7)
    elif response=='a':
        motor1GPIO.ChangeDutyCycle(auto_turn_speed)
        motor2GPIO.ChangeDutyCycle(auto_turn_speed)
        turn_left()
        turn = True
        time.sleep(1)
    elif response=='d':
        motor1GPIO.ChangeDutyCycle(auto_turn_speed)
        motor2GPIO.ChangeDutyCycle(auto_turn_speed)
        turn_right()
        turn = True
        time.sleep(1)
