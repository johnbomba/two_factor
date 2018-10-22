#! /usr/bin/env python3

import time
import os
import hashlib
import Crypto
from flask import Flask, renfer_template, request, redirect, session

app = Flask(__name__)

# need refresh button on the html page and a display pane

@app.route(/, methods=['GET'])
def display_key():
    # needs to display the 8 digit code 
    result = gen_login_code()

def decrypt_block_key():
    # pull down secret key from blockchain

    # TODO get the block key 
    block_key = os.system("")

	# decrypt key stored in blockchain
    rsakey = RSA.importKey(private_key)
    return decrypted_key

def gen_login_code():
    # calls the decrypt key function
    decrypted_key = decrypt_block_key()
    # encode the key that was pulled from the block chain to bytes
	byte_key = str.encode(decrypted_key)
    # get the current system time
    raw_time = time.time()
    # round the time to eliminate the decimal places
	round_time = round(raw_time)
    # use floor division to insure that the time variable only changes once per 30 seconds 
    floor_time = round_time // 30 
    # convert the time to a string 
    str_time = str(floor_time)
    # convert the time string to bytes for hashing
    byte_time = str.encode(str_time)
    # I used sha256 for the hash 
    hash = hashlib.sha256()
    # update the hash function with the byte time and the key from the block chain 
    hash.update(byte_time)
    hash.update(byte_key)
    # convert the hexed hash to integers for math 
    auth_hash = int.from_bytes(hash.digest(), byteorder='big')
    # create a 8 digit code
    auth_code = auth_hash % 10 ** 8
    return auth_code

