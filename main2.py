#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

import os
import sys
import time
from datetime import datetime

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont

try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()

import commands

file = commands.getoutput("ls -d /home/rafal/radiosonde_auto_rx/auto_rx/log/* | grep sonde.log | tail -n 1")

def last_line(file):
#	file = file
	with open(file, 'r') as f:
    		lines = f.read().splitlines()
    		last_line = lines[-1]
	return last_line

def SondeID(last_line):
        ID = last_line.split(',')[1]
        frq = last_line.split(',')[8]
        return "ID: %s FRQ: %s" % (ID, frq)

def date(last_line):
        date = last_line.split(',')[0]
        import dateutil.parser
        date = dateutil.parser.parse(date)
        date = date.strftime('%d/%m/%Y %H:%M:%S')
        return date

def longitute(last_line):
        longitute = last_line.split(',')[3]
        return "Lon: %s" % longitute

def latitude(last_line):
        latitude = last_line.split(',')[4]
        return "Lat: %s" % latitude

def altitude(last_line):
        altitude = last_line.split(',')[5]
        temp = last_line.split(',')[6]
        return "Alt: %s m Temp: %s" % (altitude, temp)

def stats(device):
    # use custom font
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)

    with canvas(device) as draw:
        draw.text((0, 0), SondeID(last_line(file)), font=font2, fill="white")
        if device.height >= 16:
            draw.text((0, 14), date(last_line(file)), font=font2, fill="white")

        if device.height >= 32:
            draw.text((0, 26), longitute(last_line(file)), font=font2, fill="white")

        if device.height >=48:
            draw.text((0, 38), latitude(last_line(file)), font=font2, fill="white")

            try:
                draw.text((0, 50), altitude(last_line(file)), font=font2, fill="white")
            except KeyError:
                pass

#print last_line(file)
def main():
    global last_line
    while True:
	#print SondeID(last_line(file))
#	print last_line(file)
#	last_line = last_line(file)
#	print last_line
        stats(device)
        print SondeID(last_line(file))
	    print date(last_line(file))
	    print longitute(last_line(file))
	    print latitude(last_line(file))
	    print altitude(last_line(file))
	time.sleep(5)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass

