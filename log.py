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

file = commands.getoutput("ls -d /home/rafal/radiosonde_auto_rx/auto_rx/log/* | grep system | tail -n 1")

def line_count(file):
	file = file
	with open(file, 'r') as f:
		for i, l in enumerate(f):
			pass
	return i + 1



def function_last_line(file,x):
    file = file
    x = x
            with open(file, 'r') as f:
            lines = f.readlines()[-x]
            last_line = lines.split(',')[1]
            last_line = last_line.split(':')[1]
        return last_line


def stats(device):
    # use custom font
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)
    with canvas(device) as draw:
	if line_count(file) < 4:
		draw.text((0, 14), "waiting for logs", font=font2, fill="white")
	if line_count(file) >= 4:
		draw.text((0, 0), function_last_line(file,1), font=font2, fill="white")
	if device.height >= 16 and line_count(file) >= 4:
           	draw.text((0, 14), function_last_line(file,2), font=font2, fill="white")
        if device.height >= 32 and line_count(file) >= 4:
	        draw.text((0, 26), function_last_line(file,3), font=font2, fill="white")
        if device.height >=48 and line_count(file) >= 4:
	        draw.text((0, 38), function_last_line(file,4), font=font2, fill="white")
	if device.height >=48 and line_count(file) >= 4:
		 draw.text((0, 50), function_last_line(file,5), font=font2, fill="white")

def main():
    while True:
	stats(device)
	time.sleep(5)
	print line_count(file)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
