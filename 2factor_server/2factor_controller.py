#! /usr/bin/env python3

# run this on the 2 factor server

import time
import os
import hashlib
import mcrpc
from flask import Flask, renfer_template, request, redirect, f

app = Flask(__name__)

# need refresh button on the html page and a display pane

@app.route(/, methods=['POST'])
def display_key():
    # needs to display the 8 digit code 
    result = gen_login_code()


def decrypt_block_key():
    # pull down secret key from blockchain
    block_address = '1KNibad2yyoZimaXkDgEzdCgJiRoynqE6bVUTt'
    tfa_address =  '1Kgb6cwndPfZWHp62sxqxW15661nafgC1uFHU' 
    tfa_lable = f'{block_address}-{tfa_address}'
    
    # pull down secret key from blockchain
    client = c = mcrpc.RpcClient('127.0.0.1', 4332, 'multichainrpc', 'FgUY2NdS7ydYwpGQifCBzkUmqmpynKcQuwbNuf7PfhmR')
    block_key = client.liststreamkeyitems('items', tfa_lable, count=True, start=1)
    block_key = block_key[0]['data']
    
    # export the block_key to bash
    os.environ['SECRET']=block_key
    
    # decrypt key stored in blockchain
    os.system('DECRYPT=$(echo $SECRET | xxd -p -r | openssl rsautl -decrypt -inkey ~/.multichain/2fact/stream-privkeys/1Kgb6cwndPfZWHp62sxqxW15661nafgC1uFHU.pem)')
    decrypted_key = os.environ.get('DECRYPT')

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

if __name__ == "__main__":
    app.run('127.0.0.1', debug=True)
    # app.run("0.0.0.0", debug=True)