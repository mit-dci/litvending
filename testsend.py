
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
reset_pin = cfg['reset_pin_num']
sleeping = cfg['pin_high_time']

try:
	# GPIO init.
	gpio.setmode(gpio.BOARD)
	gpio.setwarngings(True);

	# First reset the Arduino.
	gpio.output(reset_pin, gpio.HIGH)
	time.sleep(sleeping)
	gpio.output(reset_pin, gpio.LOW)
	time.sleep(sleeping)

	# Wait a bit for it to finish initing.  (Probably more than it needs.)
	time.sleep(1000)

    # Just turn it on, wait a bit, and turn it off.
    gpio.output(trigger_pin, gpio.HIGH)
    time.sleep(sleeping)
    gpio.output(trigger_pin, gpio.LOW)
	time.sleep(sleeping)
except:
    print('Error sending GPIO signals.  You probably did something horribly wrong.')
