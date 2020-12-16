import time  
import http.client, urllib  
import json 
import sys
import RPi.GPIO as GPIO
from directions import *
from mcs_functions import *
import threading

v=343
TRIGGER_PINL = 31
ECHO_PINL = 29
TRIGGER_PINR = 11
ECHO_PINR = 13
LIGHT_SENSE = 36
LED_PIN = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

auto_speed = 25
auto_turn_speed = 40
manual_speed = 17
manual_turn_speed = 20

def measure_distance(trigger, echo):
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

def parse_response(response, channel):
    response = response[response.find(channel):]
    response = response[response.rfind("value"):]
    # response = response[response.find(":")+2:response.find("\"")+1]
    response = response[response.find(":")+2:]
    response = response[:response.find("\"")]
    return response

def readLDR():
    reading = 0
    GPIO.setup(LIGHT_SENSE, GPIO.OUT)
    GPIO.output(LIGHT_SENSE, False)
    time.sleep(.1)
    GPIO.setup(LIGHT_SENSE, GPIO.IN)
    while(GPIO.input(LIGHT_SENSE)==False):
        reading = reading+1
    return reading

def control_LED():
	while True:
		if readLDR()>30000:
			GPIO.output(LED_PIN, True)
		else:
			GPIO.output(LED_PIN, False)

def main():
    mode = 1
    old_distanceL = 100
    old_distanceR = 100
    turn = False
    dark_duration = 0

    t = threading.Thread(target=control_LED)
    t.start()

    while True:
        distanceL = measure_distance(TRIGGER_PINL, ECHO_PINL)
        distanceR = measure_distance(TRIGGER_PINR, ECHO_PINR)
        payload = {"datapoints":[{"dataChnId":"auto","values":{"value":str(distanceL) + "," + str(distanceR)}}]}
        post_to_mcs(payload)

        if mode==1:
            response = parse_response(str(get_from_mcs("direction_m")), "direction_m")
            manual_control(response)
        if mode==2:
            response = parse_response(str(get_from_mcs("direction")), "direction")
            response2 = parse_response(str(get_from_mcs("direction_m")), "direction_m")
            auto_pilot(response, response2, distanceR, distanceL, old_distanceR, old_distanceL)
            stop()
            time.sleep(.2)
            old_distanceR = distanceR
            old_distanceL = distanceL



if __name__ == '__main__':
    main()