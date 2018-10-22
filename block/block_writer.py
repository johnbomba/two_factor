#!/usr/bin/env python3 
import os
import Crypto
from flask import Flask

app = Flask(__name__)

@app.route(/)
def new_key_to_block():
    block_key = os.urandom(16)
    # need to link the public keys to this app
    login_server_pub_key = # Key/location
    two_factor_pub_key = # Key/location
    # need to link the private key for the block writer
    block_writer_pri_key = # Key/location
    # encrypt the secret key with

    # os.system block command
