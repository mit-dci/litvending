#!/usr/bin/env python3

import os
import os.path as paths
import sys

import json

gpio = None
try:
	import RPi.GPIO
	gpio = RPi.GPIO
except:
	print('RPi library not found.  We\'re probably on a dev machine.  Moving on...')

default_config = {
	'pin_num': -1,
	'pin_high_time': 1,
	'vend_cost_sat': 1000
}

def get_cfg_path():
	if os.getenv('LITVENDING_CONFIG') is not None:
		return paths.expanduser(os.getenv('LITVENDING_CONFIG'))
	else:
		return paths.join(os.getenv('HOME'), '.litvending', 'config.json')

def load_config():

	# Figure out what the path is.
	cfgpath = get_cfg_path()

	# Here is where we decide if we need to create a new config.
	if not paths.exists(cfgpath):
		print('Config not found, creating at', cfgpath)
		dir = paths.dirname(cfgpath)
		if dir != '':
			os.makedirs(dir, exist_ok=True)
		with open(cfgpath, 'w') as f:
			f.write(json.dumps(default_config, indent=4))
		return default_config
	else:
		# This is easy, just load it.
		with open(cfgpath, 'r') as f:
			return json.loads(f.read())

def main(cfg):
	if cfg['pin_num'] == -1:
		print('You need to configure me first.  Come back later.')
		sys.exit(1)

if __name__ == '__main__':
	main(load_config())
