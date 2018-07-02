import os
import os.path as paths

import json

default_config = {
	'trigger_pin_num': -1,
	'pin_high_time': 0.25,
	'deposit_delay_time': 2.0,
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
