import os
import psutil 
import sys
import RPi.GPIO as GPIO 
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from pathlib import Path
from datetime import datetime

from time import sleep 

if os.name != 'posix':
    sys.exit(f'{os.name} platform is not supported')


try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()


# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return f"{n}B"


def cpu_usage():
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
        % (av1, av2, av3, str(uptime).split('.')[0])


def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def stats():
    serial = i2c(port=2, address=0x3C)
    device = ssd1306(serial)

    with canvas(device) as draw:
        draw.text((0, 0), cpu_usage(), fill="white")
        if device.height >= 32:
            draw.text((0, 14), mem_usage(), fill="white")

        if device.height >= 64:
            draw.text((0, 26), disk_usage('/'), fill="white")
            try:
                draw.text((0, 38), network('wlan0'), fill="white")
            except KeyError:
                pass
            
def cpu_info():
    while True:
        load1, load5, load15 = psutil.getloadavg()
 
        cpu_usage = (load15/os.cpu_count()) * 100
 
        print("The CPU usage is : ", cpu_usage)
        if cpu_usage > 90:
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BOARD) 
            GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) 
            GPIO.output(11, GPIO.HIGH) 
            sleep(1) 
            GPIO.output(11, GPIO.LOW) 
            sleep(1)

def main():
    while True:
        stats()
        cpu_info()
        sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass