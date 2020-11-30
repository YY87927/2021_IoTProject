import time  
import http.client, urllib  
import json  
import sys
import RPi.GPIO as GPIO

deviceId = "D3X0jwfT"
deviceKey = "0E6pZs0E6WM6hPbn"

v=343

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
manual_speed = 17
manual_turn_speed = 20

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

def measure(trigger, echo):
	GPIO.output(trigger, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(trigger, GPIO.LOW)
	pulse_start = time.time()
	while GPIO.input(echo) == GPIO.LOW:
		pulse_start = time.time()
	while GPIO.input(echo) == GPIO.HIGH:
		pulse_end = time.time()
	t = pulse_end - pulse_start
	d = t * v
	d = d/2
	return d
    
def post_to_mcs(payload):
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    not_connected = 1
    while (not_connected):
        try:
            conn = http.client.HTTPConnection("api.mediatek.com:80")
            conn.connect()
            not_connected = 0
        except (http.client.HTTPException, socket.error) as ex:
            print ("Error: %s" % ex)
            time.sleep(10)  # sleep 10 seconds

    conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers)
    response = conn.getresponse()
    # print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
    data = response.read()
    conn.close()

def get_from_mcs(channel=""):
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    not_connected = 1
    while (not_connected):
        try:
            conn = http.client.HTTPConnection("api.mediatek.com:80")
            conn.connect()
            not_connected = 0
        except (http.client.HTTPException, socket.error) as ex:
            print ("Error: %s" % ex)
            time.sleep(10)  # sleep 10 seconds

    conn.request("GET", "/mcs/v2/devices/" + deviceId + "/datachannels/" + channel + "/datapoints", "", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

def parse_response(response, channel):
    response = response[response.find(channel):]
    response = response[response.rfind("value"):]
    # response = response[response.find(":")+2:response.find("\"")+1]
    response = response[response.find(":")+2:]
    response = response[:response.find("\"")]
    return response

def main():
    mode = 1
    old_distanceL = 100
    old_distanceR = 100
    turn = False
    while True:
        distanceL = measure(TRIGGER_PINL, ECHO_PINL)
        distanceR = measure(TRIGGER_PINR, ECHO_PINR)
        payload = {"datapoints":[{"dataChnId":"auto","values":{"value":str(distanceL) + "," + str(distanceR)}}]}
        post_to_mcs(payload)
        if mode==1:
            response = parse_response(str(get_from_mcs("direction_m")), "direction_m")
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
            elif response=='2':
                mode = 2
        if mode==2:
            response = parse_response(str(get_from_mcs("direction")), "direction")
            response2 = parse_response(str(get_from_mcs("direction_m")), "direction_m")
            if (distanceR > old_distanceR + 0.5 or distanceL > old_distanceL + 0.5)\
                and turn == False:
                motor1GPIO.ChangeDutyCycle(auto_speed)
                motor2GPIO.ChangeDutyCycle(auto_speed)
                backward()
                turn = False
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
            if response2=='1':
                mode = 1
            stop()
            time.sleep(.2)
            old_distanceR = distanceR
            old_distanceL = distanceL


if __name__ == '__main__':
    main()