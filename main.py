#!/bin/python3

import subprocess
import re
from sys import stderr

from pynput import keyboard
import functions
from threading import Thread

result = subprocess.Popen(['evtest', '--grab'], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)


keyboard_name = "Dell Dell USB Entry Keyboard" # Set this to yours

while True:
    out = result.stderr.readline()
    if out.endswith(keyboard_name + "\n"):
        break

device = out.split(':')[0]

result.kill()

result = subprocess.Popen(['evtest', '--grab', device], stdout=subprocess.PIPE, text=True)

while result.stdout.readline() != "Testing ... (interrupt to exit)\n":
    pass

switcher = False
while True:
    line = ""
    report = []
    while True:
        line = re.sub(r'^.*?,', '', result.stdout.readline())[1:-1] # Remove timestamp and newline
        if line == "-------------- SYN_REPORT ------------":
            break
        else:
            report.append(line)
    if len(report) != 1: # Verify that it isn't just a long press
        switcher = not switcher
        if switcher: # Remove the double running for a single press
            code = int(report[0][42:], base=16) # convert the code into an int
            Thread(target=functions.run, args=(code,)).start()