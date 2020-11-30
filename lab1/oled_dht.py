import Adafruit_DHT
import time
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# define the sensor module and the connected pin
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

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
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# enter infinite loop to keep detecting the current temperature and humidity
while True:
    try:
    	# read temperature and humidity with DHT11 sensor
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        # if the values are succesfully read, print them out
        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
            
        else:
            print("Failed to retrieve data from humidity sensor")
    except KeyboardInterrupt:
        exit()

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    # write texts on the screen with the drawing object
    draw.text((x, top), "Current Condition", font=font, fill=255)
    draw.text((x, top+8), "temp: "+str(temperature)+"*C", font=font, fill=255)
    draw.text((x, top+16), "humid: "+str(humidity)+"%", font=font, fill=255)
    # Display the image.
    disp.image(image)
    disp.display()
    # waits for 1 second before executing again
    time.sleep(.1)

