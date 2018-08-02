import os
import os.path as paths

import json

default_config = {
	'trigger_pin_num': -1,
	'pin_high_time': 0.1,
	'deposit_delay_time': 0.75,
	'unit_costs': {
		'1': 30000 # very very high, like $2.25 at the time of writing. 9:1 loss for them
	},
	'coin_type_ids': [ '1' ], # bitcoin testnet3
	'lit_ip': '127.0.0.1',
	'lit_port': '8001',
	'poll_rate': 5
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
