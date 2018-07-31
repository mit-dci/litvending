#!/usr/bin/env python3

import os
import time
import sys

gpio = None
try:
	import RPi.GPIO
	gpio = RPi.GPIO
except:
	print('RPi library not found.  We\'re probably on a dev machine.  Moving on...')

import lvconfig
import litrpc

def check_deposit(cointype):
	bals = conn.balance()['Balances']
	sum = 0
	for b in bals:
		if b['CoinType'] == cointype:
			sum += b['ChanTotal'] # I'm not sure how this works, can it return dupes?
	return sum

def main(cfg):
	if cfg['trigger_pin_num'] == -1:
		print('You need to configure me first.  Come back later.')
		sys.exit(1)

	# Find important commonly-used variables.
	trigger_pin = cfg['trigger_pin_num']
	sleep_time = cfg['pin_high_time']
	deposit_delay = cfg['deposit_delay_time']

	# Set up the GPIO pins.
	if gpio != None:
		gpio.setmode(gpio.BOARD)
		gpio.setwarnings(False)
		gpio.setup(trigger_pin, gpio.OUT)

	# Set up the connection and connect.
	print('Connecting to lit at', cfg['lit_ip'], 'on port', cfg['lit_port'])
	global conn
	conn = litrpc.LitClient(cfg['lit_ip'], cfg['lit_port'])
	print('Set up client.')

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

				for i in range(units_to_insert):
					# Just turn it on, wait a bit, and turn it off.
					gpio.output(trigger_pin, gpio.HIGH)
					time.sleep(sleep_time)
					gpio.output(trigger_pin, gpio.LOW)
					time.sleep(deposit_delay)

			else:
				print('Not running on RPi, doing nothing!')
		else:
			print('No payment')
		time.sleep(cfg['poll_rate'])

if __name__ == '__main__':
	main(lvconfig.load_config())
