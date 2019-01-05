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


def find_log():
    systemlog = commands.getoutput("ls -d /home/rafal/radiosonde_auto_rx/auto_rx/log/* | grep system | tail -n 1")
    tele = commands.getoutput("cat \"" + systemlog + "\"| grep 'Telemetry Logger - O\|Telemetry Logger - U'")
    if tele:
            tele = tele.split(',')[1]
            tele = tele.split('/')[2]
    else:
        tele = None
    
    return tele

def last_line():
    path = "/home/rafal/radiosonde_auto_rx/auto_rx/log/" + find_log()
    with open(path, 'r') as f:
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
        if  find_log() is None:
            draw.text((0, 0), "No sonde decoded", font=font2, fill="white")
        else:
            draw.text((0, 0), SondeID(last_line()), font=font2, fill="white")
            if device.height >= 16:
                draw.text((0, 14), date(last_line()), font=font2, fill="white")
            if device.height >= 32:
                draw.text((0, 26), longitute(last_line()), font=font2, fill="white")
            if device.height >=48:
                draw.text((0, 38), latitude(last_line()), font=font2, fill="white")
            try:
                draw.text((0, 50), altitude(last_line()), font=font2, fill="white")
            except KeyError:
                pass

def main():
    while True:
        stats(device)
        print find_log()
#        print SondeID(last_line())
#        print date(last_line())
#        print longitute(last_line())
#        print latitude(last_line())
#        print altitude(last_line())
        time.sleep(5)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass

