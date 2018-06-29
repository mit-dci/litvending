
import time

gpio = None
try:
	import RPi.GPIO
	gpio = RPi.GPIO
except:
	print('RPi library not found.  We\'re probably on a dev machine.  Moving on...')

import lvconfig

cfg = lvconfig.load_config()

try:
    # Just turn it on, wait a bit, and turn it off.
    gpio.output(cfg['pin_num'], gpio.HIGH)
    time.sleep(cfg['pin_high_time'])
    gpio.output(cfg['pin_num'], gpio.LOW)
except:
    print('Error sending GPIO signals.  You probably did something horribly wrong.')
