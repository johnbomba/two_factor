#! /usr/bin/env python3

# run this on the 2 factor server

import time
import os
import subprocess

import hashlib
from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)

# need refresh button on the html page and a display pane

@app.route('/', methods=['GET','POST'])
def display_key():
    # needs to display the 8 digit code 
    result = gen_login_code()
    return render_template('2factor.html', result=result)

def retrieve_password(access_tx_id):
    # pull down secret key from blockchain
    # build the system command
    password_build = f'multichain-cli 2fact gettxdataout {access_tx_id} 0'
    password_pipe = subprocess.Popen(password_build, shell=True, stdout=subprocess.PIPE)
    password_tail = subprocess.Popen('tail -n 1', shell=True, stdin=password_pipe.stdout, stdout=subprocess.PIPE)
    password_read = password_tail.stdout
    password = password_read.read()

    return password

def decrypt_password(access_tx_id, tfa_address):
    # decrypt the password
    password = retrieve_password(access_tx_id)
    # build the system command including unix pipes 
    encrypted_pw = f'echo {password}'
    encrypted_pw_pipe = subprocess.Popen(encrypted_pw, shell=True, stdout=subprocess.PIPE)
    encrypted_pw_hex = subprocess.Popen('xxd -p -r', shell=True, stdin=encrypted_pw_pipe.stdout, stdout=subprocess.PIPE)
    encrypted_pw_ssl = subprocess.Popen(f'openssl rsautl -decrypt inkey ~/.multichain/2fact/stream-privkeys/{tfa_address}.pem', shell=True, stdin=encrypted_pw_hex.stdout, stdout=subprocess.PIPE)
    decrypted_pw = encrypted_pw_ssl.stdout
    decrypted_pw = decrypted_pw.read()
    return decrypted_pw

def retrieve_secret_msg(items_tx_id):
    # pull down the secret message from the block chain
    message_build = f'multichain-cli 2fact gettxdataout {items_tx_id} 0'
    message_pipe = subprocess.Popen(message_build, shell=True, stdout=subprocess.PIPE)
    message_tail = subprocess.Popen('tail -n 1', shell=True, stdin=message_pipe.stdout, stdout=subprocess.PIPE)
    message_read = message_tail.stdout
    message = message_read.read()
    return message

def decrypt_secret_msg(items_tx_id, access_tx_id, tfa_address):
    password = decrypt_password(access_tx_id, tfa_address)
    message = retrieve_secret_msg(items_tx_id)
    # decrypt key that was stored in blockchain
    openssl_echo = f'echo {message}'
    openssl_echo2 = subprocess.Popen(openssl_echo, shell=True, stdout=subprocess.PIPE)
    openssl_enc1 = subprocess.Popen('xxd -p -r', shell=True, stdin=openssl_echo2.stdout, stdout=subprocess.PIPE)
    openssl_enc2 = subprocess.Popen(f"openssl enc -d -aes-256-cbc -pass pass:{password} ", shell=True, stdin=openssl_enc1.stdout, stdout=subprocess.PIPE)
    decrypted_msg = openssl_enc2.stdout
    decrypted_key = decrypted_msg.read()
    return decrypted_key

def gen_login_code():
    items_tx_id = '44becbc521c2ecba19a69cb7f38a1b1fa168b1a7e434154879e6830cf14dc1a8'
    access_tx_id = '3fc1478475672b7691dd0d07ef5a76c03adffadd7581815f09f9bc94b2cf375c'
    tfa_address = '1GN9k6QfkNoHJjzDbaaBJgPJubRUH65jEconhg'
    tfa_lable = f'{access_tx_id}-{tfa_address}'

    # calls the decrypt key function returns bytes
    decrypted_key = decrypt_secret_msg(items_tx_id, access_tx_id, tfa_address)

    # encode the key that was pulled from the block chain to bytes
    # byte_key = str.encode(decrypted_key)

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
    hash.update(decrypted_key)

    # convert the hexed hash to integers for math 
    auth_hash = int.from_bytes(hash.digest(), byteorder='big')

    # create a 8 digit code
    auth_code = auth_hash % 10 ** 8
    return auth_code

if __name__ == "__main__":
    app.run('127.0.0.1', debug=True)
    # app.run("0.0.0.0", debug=True)