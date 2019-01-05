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

import subprocess
import commands

systemlog = commands.getoutput("ls -d /home/rafal/radiosonde_auto_rx/auto_rx/log/* | grep system | tail -n 1")
telemetry = commands.getoutput("ls -d /home/rafal/radiosonde_auto_rx/auto_rx/log/* | grep sonde.log | tail -n 1")
check = commands.getoutput("cat \"" + systemlog + "\"| grep 'Detected new'")


def function_last_line(file,x):
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
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)
    with canvas(device) as draw:
        if line_count(systemlog) < 4:
            draw.text((0, 14), "waiting for logs", font=font2, fill="white")
        if line_count(systemlog) >= 4:
            draw.text((0, 0), function_last_line(systemlog,1), font=font2, fill="white")
        if device.height >= 16 and line_count(systemlog) >= 4:
            draw.text((0, 14), function_last_line(systemlog,2), font=font2, fill="white")
        if device.height >= 32 and line_count(systemlog) >= 4:
            draw.text((0, 26), function_last_line(systemlog,3), font=font2, fill="white")
        if device.height >=48 and line_count(systemlog) >= 4:
	        draw.text((0, 38), function_last_line(systemlog,4), font=font2, fill="white")
        if device.height >=48 and line_count(systemlog) >= 4:
            draw.text((0, 50), function_last_line(systemlog,5), font=font2, fill="white")

def tele(device):
    # use custom font
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)
    with canvas(device) as draw:
        draw.text((0, 0), SondeID(function_last_line(telemetry,1)), font=font2, fill="white")
        if device.height >= 16:
            draw.text((0, 14), date(function_last_line(telemetry,1)), font=font2, fill="white")
        if device.height >= 32:
            draw.text((0, 26), longitute(function_last_line(telemetry,1)), font=font2, fill="white")
        if device.height >=48:
            draw.text((0, 38), latitude(function_last_line(telemetry,1)), font=font2, fill="white")
            try:
                draw.text((0, 50), altitude(function_last_line(telemetry,1)), font=font2, fill="white")
            except KeyError:
                pass
if check is not None:
    device = get_device()
    log(device)
    time.sleep(2)
        
else:
    device = get_device()
    tele(device)
    time.sleep(2)