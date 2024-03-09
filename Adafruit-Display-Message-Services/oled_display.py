import os
import sys
import subprocess
import shlex
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306







serial = i2c(port=2, address=0x3C)
device = ssd1306(serial)



def print():
    command = "ip addr"
    test = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    output = test.communicate()[0]


    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0, 10), "Starting...", fill="white")
        draw.text((0, 20), output, fill="white")



if __name__ == '__main__':
    while True:
        print()