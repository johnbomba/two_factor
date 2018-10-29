#!/usr/bin/env python3 
# this goes on the block writer server
import os
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def new_key_to_block():
    # addresses that are used to build labels
    block_address = ''
    tfa_address = ''
    login_address = ''

    # generate password 
    password = generate_password()

    # transaction id's for the login and 2fa public keys in the pubkeys stream 
    login_tx_id =
    tfa_tx_id = 

    # pull pub keys from the block chain 
    l_pubkey = login_secret_key(login_tx_id)
    t_pubkey = tfa_secret_key(tfa_tx_id)
    secret_message = secret_message()


    #generate lables for the assets stream
    login_label = f'{login_tx_id}-{login_address}'
    print(f'login_label {login_label}')
    tfa_label = f'{tfa_tx_id}-{tfa_address}'
    print(f'tfa_label {tfa_label}')

    # encrypt the secret block key with the login and tfa public keys
    encrypt_l_pw = encrypt_login_pw(password)
    encrypt_t_pw = encrypt_tfa_pw(password)

    # thess are the publish functions for the secret key , login , and tfa 
    publish_secret_message(block_address, secret_message)
    publish_login_pw(block_address, login_label, encrypt_l_pw)
    publish_tfa_pw(block_address, tfa_label, encrypt_t_pw)
    
    return 'This Worked'

def generate_password():
    # use os.system to generate a pw that will encrypt the secret msg on the block chain 
    os.system(f'PASSWORD=$(openssl rand -base 64 48)')
    password = os.environ.get('PASSWORD')
    return password

def login_secret_key(login_tx_id):
    # pulls down login pub key from the block chain
    os.system(f'multichain-cli 2fact gettxoutdata {login_tx_id} 0 | tail -n 1 | xxd -p -r > tmp/l_pubkey.pem')
    print('downloaded l_pub')

def tfa_secret_key(tfa_tx_id):
    # pull down 2fa pub key from the block chain
    os.system(f'multichain-cli 2fact gettxoutdata {tfa_tx_id} 0 | tail -n 1 | xxd -p -r > tmp/t_pubkey.pem')
    print('downloaded t_pub')

def secret_message():
    # this function creates the block key as a secret message to be used in the 2fa functions on the login and 2fa servers
    secret_msg = os.urandom(16).hex
    os.system(f'echo "{secret_msg}" > /tmp/block_key')
    print('secret created')
    return secret_message

def publish_secret_message(block_address, cipher):
    os.system(f"multichain-cli 2fact publish from {block_address} items '' {cipher}" )

def publish_login_pw(block_address, login_label, encrypt_l_pw):
    os.system(f"multichain-cli 2fact publish from {block_address} access {login_lable} {encrypt_l_pw}")


def publish_tfa_pw(block_address,tfa_label, encrypt_t_pw):
    os.system(f"multichain-cli 2fact publish from {block_address} access {tfa_lable} {encrypt_t_pw}")


def encrypt_secret_message(secret_message, password):
    # used to encrypt the secret message on the block chain
    os.system(f"cipher=$(echo '{secret_message}' | openssl enc -aes-256-cbc -pass pass:{password} | xxd -p -c 99999)")
    cipher = os.environ.get('cipher')
    return cipher 

def encrypt_login_pw(password):
    # need to be able pass this to another function
    os.system(f'encrypt_t_key=$(echo "{password}" | openssl rsautl -encrypt -inkey /tmp/l_pubkey.pem -pubin | xxd -p -c 9999)')
    encrypt_l_key = os.environ.get('encrypt_l_key')
    print('login_pw created')
    return encrypt_l_pw

def encrypt_tfa_pw(password):
    # need to be able pass this to another function
    os.system(f'encrypt_t_key=$(echo "{password}" | openssl rsautl -encrypt -inkey /tmp/t_pubkey.pem -pubin | xxd -p -c 9999)')
    encrypt_t_key = os.environ.get('encrypt_t_key')
    print('tfa_pw created')
    return encrypt_t_pw

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host= '0.0.0.0', debug=True)