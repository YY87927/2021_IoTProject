import time
import http.client, urllib  
import json  
import sys
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pynput.keyboard import Key, Listener

# Set MediaTek Cloud Sandbox (MCS) Key
deviceId = "DuZV6dw2"
deviceKey = "4bgfxbFrlxfQwvuW"

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
#****************************************************
keyPressed = str(Key.space)

def on_press(key):
    # print(f'{key} pressed')
    global keyPressed
    keyPressed = str(key)[1]
    
def on_release(key):
    # print(f'{key} released')
    global keyPressed
    keyPressed = str(Key.space)
    if key == Key.esc:
        # Stop listener
        return False
#define parameters of the OLED screen
RST = None     # on the PiOLED this pin isnt used
# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
# Initialize library.
disp.begin()
# Clear OLED display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# set paddings at the edge of the screen
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
font = ImageFont.load_default()
font2 = ImageFont.truetype('FreeSans.ttf', 16)
#font = ImageFont.truetype('Montserrat-Light.ttf', 8)
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
# write texts on the screen with the drawing object

# enter infinite loop to keep detecting the current temperature and humidity
def main():
    # Start keyboard event listener
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    permission=0
    
    while True:
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,width,height), outline=0, fill=0) 
        draw.text((x, top), "Please enter the", font=font, fill=255)
        draw.text((x, top+8), "password:", font=font, fill=255)
        disp.image(image)
        disp.display()
        password = input('please enter the password：')
        mode = 1
        
        if(password=='0000'):
            permission=1
            draw.rectangle((0,0,width,height), outline=0, fill=0) 
            draw.text((x, top+8), "       Hello~~", font=font2, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(3)
        else :
            permission=0
            draw.rectangle((0,0,width,height), outline=0, fill=0) 
            draw.text((x, top), "Retry", font=font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(5)
                
        while(permission==1):
            try:
                payload = {"datapoints":[{"dataChnId":"direction_m","values":{"value":keyPressed}}]}
                post_to_mcs(payload)
                response = parse_response(str(get_from_mcs("direction_m")), "direction_m")
                
                      
            except KeyboardInterrupt:
                permission=0
                exit()
                
            draw.rectangle((0,0,width,height), outline=0, fill=0)    
            draw.text((x, top), "Mode :", font=font, fill=255)
            draw.text((x, top+9), "Direction : ", font=font, fill=255)
            
            response_user = parse_response(str(get_from_mcs("user")), "user")
            draw.text((x, top+18), "User : "+str(response_user), font=font, fill=255)
            
            if mode==1:
                draw.text((x, top), "Mode : Manual", font=font, fill=255)
                if response=='w':
                    draw.text((x, top+9), "Direction : Forward", font=font, fill=255)
                elif response=='s':
                    draw.text((x, top+9), "Direction : Backward", font=font, fill=255)
                elif response=='a':
                    draw.text((x, top+9), "Direction : Left", font=font, fill=255)
                elif response=='d':
                    draw.text((x, top+9), "Direction : Right", font=font, fill=255)
                elif response=='2':
                    mode = 2
                    
            elif mode==2:
                response = parse_response(str(get_from_mcs("direction")), "direction")
                response2 = parse_response(str(get_from_mcs("direction_m")), "direction_m")
                draw.text((x, top), "Mode : Autopilot", font=font, fill=255)                      
                if response=='w':
                    draw.text((x, top+9), "Direction : Forward", font=font, fill=255)
                elif response=='s':
                    draw.text((x, top+9), "Direction : Backward", font=font, fill=255)
                elif response=='a':
                    draw.text((x, top+9), "Direction : Left", font=font, fill=255)
                elif response=='d':
                    draw.text((x, top+9), "Direction : Right", font=font, fill=255)
                if response2=='1':
                    mode = 1
                    
            disp.image(image)
            disp.display()
            
            
        #draw.text((x, top+8), "temp: "+str(temperature)+"*C", font=font, fill=255)
        #draw.text((x, top+16), "humid: "+str(humidity)+"%", font=font, fill=255)
        # Display the image.
        
    # waits for 1 second before executing again
if __name__ == '__main__':
    main()