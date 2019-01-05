#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK

import os
import sys
import time
from datetime import datetime
from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont

import subprocess
import commands

systemlog = commands.getoutput("ls -d /home/rafal/radiosonde_auto_rx/auto_rx/log/* | grep system | tail -n 1")
telemetry = commands.getoutput("ls -d /home/rafal/radiosonde_auto_rx/auto_rx/log/* | grep sonde.log | tail -n 1")
check = commands.getoutput("cat \"" + systemlog + "\"| grep 'Telemetry Logger - Opening new log file'")


def function_last_line_log(file,x):
    	with open(file, 'r') as f:
        	lines = f.readlines()[-x]
        	last_line = lines.split(',')[1]
        	last_line = last_line.split(':')[1]
    	return last_line

def line_count(file):
        with open(file, 'r') as f:
            for i, l in enumerate(f):
                pass
        return i + 1

def last_line(file):
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

def log(device):
        # use custom font
    font2 = ImageFont.truetype('../fonts/C&C Red Alert [INET].ttf', 12)
    with canvas(device) as draw:
        if line_count(systemlog) < 4:
            draw.text((0, 14), "waiting for logs", font=font2, fill="white")
        if line_count(systemlog) >= 4:
            draw.text((0, 0), function_last_line_log(systemlog,1), font=font2, fill="white")
        if device.height >= 16 and line_count(systemlog) >= 4:
            draw.text((0, 14), function_last_line_log(systemlog,2), font=font2, fill="white")
        if device.height >= 32 and line_count(systemlog) >= 4:
            draw.text((0, 26), function_last_line_log(systemlog,3), font=font2, fill="white")
        if device.height >=48 and line_count(systemlog) >= 4:
	        draw.text((0, 38), function_last_line_log(systemlog,4), font=font2, fill="white")
        if device.height >=48 and line_count(systemlog) >= 4:
            draw.text((0, 50), function_last_line_log(systemlog,5), font=font2, fill="white")

def tele(device):
    # use custom font
    font2 = ImageFont.truetype('../fonts/C&C Red Alert [INET].ttf', 12)
    with canvas(device) as draw:
        draw.text((0, 0), SondeID(last_line(telemetry)), font=font2, fill="white")
        if device.height >= 16:
            draw.text((0, 14), date(last_line(telemetry)), font=font2, fill="white")
        if device.height >= 32:
            draw.text((0, 26), longitute(last_line(telemetry)), font=font2, fill="white")
        if device.height >=48:
            draw.text((0, 38), latitude(last_line(telemetry)), font=font2, fill="white")
            try:
                draw.text((0, 50), altitude(last_line(telemetry)), font=font2, fill="white")
            except KeyError:
                pass
print check
if check is None:
    device = ssd1306(port=0, address=0x3C)
    log(device)
            
else:
    device = ssd1306(port=0, address=0x3C)
    tele(device)
    