#!/usr/bin/env python3 
import os
import Crypto
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['POST'])
def new_key_to_block():
    if 
    block_key = os.urandom(16)
    # pull down 2fa pub key
    # pull down login pub key 

    # encrypt and publish block key for 2fa
    # encrypt and publish block key for login
