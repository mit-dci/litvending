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

import litrpc

default_config = {
	'pin_num': -1,
	'pin_high_time': 1,
	'unit_cost_sat': 1000,
	'coin_type_id': 1, # test btc
	'lit_ip': '127.0.0.1',
	'lit_port': '8001', # FIXME I don't think this is right.
	'pool_rate': 5
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

conn = None

def check_deposit(cointype):
	bals = conn.balance()
	sum = 0
	for b in bals:
		if b['CoinType'] == cointype:
			sum += b['ChanTotal'] # I'm not sure how this works, can it return dupes?
	return sum

def main(cfg):
	if cfg['pin_num'] == -1:
		print('You need to configure me first.  Come back later.')
		sys.exit(1)

	# Set up the GPIO pins.
	gpio.setmode(gpio.BOARD)
	gpio.setwarngings(True);
	gpio.setup(cfg['pin_num'], gpio.OUT)

	# Set up the connection and connect.
	print('Connecting to lit at', cfg['lit_ip'], 'on port', cfg['lit_port'])
	global conn
	conn = litrpc.LitConnection(cfg['lit_ip'], cfg['lit_port'])
	conn.connect()
	print('Connected!')

	# Then just enter the main loop.
	print('Waiting for payment...')
	last_bal = -1
	while True:
		bal = check_deposit(cfg['coin_type_id'])
		diff = 0
		if last_bal != -1:
			diff = bal - last_bal
		last_bal = bal
		if diff != 0:
			units_to_insert = diff / cfg['unit_cost_sat']
			extra = diff % cfg['unit_cost_sat']
			print('Balance is now', bal, 'got a spend of', diff, 'worth', units_to_insert, 'with an extra', extra, 'left over')
			if gpio != None:

				# Just turn it on, wait a bit, and turn it off.
				gpio.output(cfg['pin_num'], gpio.HIGH)
				time.sleep(cfg['pin_high_time'])
				gpio.output(cfg['pin_num'], gpio.LOW)

			else:
				print('Not running on RPi, doing nothing!')
		time.sleep(cfg['poll_rate'])

if __name__ == '__main__':
	main(load_config())
