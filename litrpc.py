#!/usr/bin/env python3
# Copyright (c) 2017 The lit developers
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
#
# Stolen from https://github.com/mit-dci/lit/blob/c565392054d2c2c1cf5d2917e40ab69188163808/cmd/litpy/litrpc.py
"""Python interface to lit"""

import json
import logging
import random
import time

import asyncio
import websockets  # `pip install websockets

logger = logging.getLogger("litrpc")

class LitConnection():
    """A class representing a connection to a lit node."""
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self):
        """Connect to the node. Continue trying for 10 seconds"""
        logger.debug("Opening RPC connection to litnode %s:%s" % (self.ip, self.port))
        for _ in range(50):
            try:
                s = asyncio.get_event_loop().run_until_complete(websockets.connect("ws://%s:%s/ws" % (self.ip, self.port)))
                self.ws = s
            except ConnectionRefusedError:
                # lit is not ready to accept connections yet
                time.sleep(0.25)
            else:
                # No exception - we're connected!
                break
        self.msg_id = random.randint(0, 9999)

    def send_message(self, method, params):
        """Sends a websocket message to the lit node"""
        logger.debug("Sending rpc message to %s:%s %s(%s)" % (self.ip, self.port, method, str(params)))
        el = asyncio.get_event_loop();
        print('foo')
        el.run_until_complete(self.ws.send(json.dumps({"method": "LitRPC.%s" % method,
                                 "params": [params],
                                 "jsonrpc": "2.0",
                                 "id": str(self.msg_id)})))

        self.msg_id = self.msg_id + 1 % 10000

        print('bar')
        resp = json.loads(el.run_until_complete(self.ws.recv()))
        print('baz')
        logger.debug("Received rpc response from %s:%s method: %s Response: %s." % (self.ip, self.port, method, str(resp)))
        return resp

    def __getattr__(self, name):
        """Dispatches any unrecognised messages to the websocket connection"""
        def dispatcher(**kwargs):
            return self.send_message(name, kwargs)
        return dispatcher

    def new_address(self):
        """Add a new wallit address"""
        return self.Address(NumToMake=1)

    def balance(self):
        """Get wallit balance"""
        return self.Bal()
