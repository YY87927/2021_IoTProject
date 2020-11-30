#**************************************************** 
# Import Packages
import time  
import http.client, urllib  
import json  
import sys
from pynput.keyboard import Key, Listener
#****************************************************


#**************************************************** 
# Set MediaTek Cloud Sandbox (MCS) Key
deviceId = "D3X0jwfT"
deviceKey = "0E6pZs0E6WM6hPbn"
#****************************************************

#**************************************************** 
# Define functions responsible for MCS connections
# Function for uploading data to MCS
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
    print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
    data = response.read()
    conn.close()

# Function for retrieving data from MCS
def get_from_mcs():
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

    conn.request("GET", "/mcs/v2/devices/" + deviceId + "/datachannels/Humidity/datapoints", "", headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data
#****************************************************

#**************************************************** 
# Detecting keyboard events
keyPressed = str(Key.space)

# Keyboard on press event function
def on_press(key):
    # print(f'{key} pressed')
    global keyPressed
    keyPressed = str(key)[1]

# Keyboard on release event function
def on_release(key):
    # print(f'{key} released')
    global keyPressed
    keyPressed = str(Key.space)
    if key == Key.esc:
        # Stop listener
        return False

# Start keyboard event listener
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
#**************************************************** 

#**************************************************** 
# Constantly detect keyboard events with listener and post the pressed key to MCS
# Default pressed key is “Key.space”, which indicates that the automobile stops moving
while True:
    # print(keyPressed)
    try:
        payload = {"datapoints":[{"dataChnId":"direction_m","values":{"value":keyPressed}}]}
        post_to_mcs(payload)
    except KeyboardInterrupt:
        exit()
#**************************************************** 