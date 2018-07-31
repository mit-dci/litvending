#!/usr/bin/env python3

import time

gpio = None
try:
	import RPi.GPIO
	gpio = RPi.GPIO
except:
	print('RPi library not found.  We\'re probably on a dev machine.  Moving on...')

import lvconfig

cfg = lvconfig.load_config()

trigger_pin = cfg['trigger_pin_num']
sleeping = cfg['pin_high_time']

# Debug
print('Trigger pin is', trigger_pin)

# GPIO init.
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(trigger_pin, gpio.OUT)

# Just turn it on, wait a bit, and turn it off.
print('Sending send trigger...')
gpio.output(trigger_pin, gpio.HIGH)
time.sleep(sleeping)
gpio.output(trigger_pin, gpio.LOW)
print('Released.')
time.sleep(sleeping)
