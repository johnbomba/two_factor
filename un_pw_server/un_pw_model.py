#! /usr/bin/env python3

import os
import time
import hashlib
import sqlite3

def validate_credentials(usernam, password)
    # connect to the credentails DB
    connection = sqlite3.connect('credentials.db',check_same_thread=False)
    cursor = connection.cursor()
    query = cursor.execute(f'SELECT username from users WHERE username = "{username}";')
    un_result = cursor.fetchone()
    # if the input username is equal to the username in the db return true
    if username == un_result:
        query2 = cursor.execute(f'SELECT password from users WHERE username = "{username}";')
        # if the PW is equal to the PW in the db return true 
        # TODO HASH The PW 
        if password == query2:
            return True
        return 'Invalid Login Credentials'
    return "Invalid Login Credentials"
    cursor.close()
    username = username


def decrypt_key(block_key)
	#decrypt key stored in blockchain
    

def gen_login_code(decrypted_key)
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

def check_two_factor(auth_code, input_code):
    # if the authentication code is equal to the input code return true
    if decrypted_key == input_code:
        return True
    return False
