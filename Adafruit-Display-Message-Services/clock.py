import time
import sys
import RPi.GPIO as GPIO 
import os
import subprocess
import shlex



from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep 


serial = i2c(port=2, address=0x3C)
device = ssd1306(serial)


offset = 0


while True:
    if offset == 0:
        
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            text = time.strftime("%A")
            draw.text((0, 0), text, fill="white")
            text = time.strftime("%e %b %Y")
            draw.text((0, 16), text, fill="white")
            text = time.strftime("%X")
            draw.text((0, 32+4), text, fill="white")


      
    
        time.sleep(1)
    else:
        time.sleep(1)
 # vertically scroll to switch between buffers
 