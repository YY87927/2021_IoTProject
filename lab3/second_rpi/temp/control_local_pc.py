#**************************************************** 
# Import Packages
import time  
import http.client, urllib  
import json  
import sys
# import Adafruit_SSD1306
# from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont
from pynput.keyboard import Key, Listener
from mcs_functions import *
#****************************************************

#**************************************************** 
# Detecting keyboard events
keyPressed = str(Key.space)

# # define the sensor module and the connected pin
# DHT_SENSOR = Adafruit_DHT.DHT11
# DHT_PIN = 4

# #define parameters of the OLED screen
# RST = None     # on the PiOLED this pin isnt used
# # 128x32 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
# # Initialize library.
# disp.begin()
# # Clear OLED display.
# disp.clear()
# disp.display()

# width = disp.width
# height = disp.height
# image = Image.new('1', (width, height))
# padding = -2
# top = padding
# bottom = height-padding
# # Move left to right keeping track of the current x position for drawing shapes.
# x = 0
# # Load default font.
# font = ImageFont.load_default()
# # Get drawing object to draw on image.
# draw = ImageDraw.Draw(image)

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

# def show_info():
#     # Draw a black filled box to clear the image.
#     draw.rectangle((0,0,width,height), outline=0, fill=0)
#     # write texts on the screen with the drawing object
#     draw.text((x, top), "Current Condition", font=font, fill=255)
#     draw.text((x, top+8), "temp: "+str(temperature)+"*C", font=font, fill=255)
#     draw.text((x, top+16), "humid: "+str(humidity)+"%", font=font, fill=255)
#     # Display the image.
#     disp.image(image)
#     disp.display()
#     # waits for 1 second before executing again
#     time.sleep(.1)

def main():
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


        # show_info()

    #**************************************************** 

if __name__ == '__main__':
    main()