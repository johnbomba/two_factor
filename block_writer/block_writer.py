#!/usr/bin/env python3 
import os
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['POST'])
def new_key_to_block():
    # pull pub keys from the block chain 
    login_secret_key()
    tfa_secret_key()

    # use addresses to build lables
    block_address = '1KNibad2yyoZimaXkDgEzdCgJiRoynqE6bVUTt'
    login_address = '1GsqQEwfMfYu773ywxBF7xj4ZBvW8VcQJEEA8i'
    tfa_address = '1Kgb6cwndPfZWHp62sxqxW15661nafgC1uFHU'

    login_lable = f'{block_address}-{login_address}'
    tfa_lable = f'{block_address}-{tfa_address}'
    
    # encrypt the secret block key with the login and tfa public keys
    encrypt_login_key()
    encrypt_tfa_key()

    # this calls the publish function for the login and tfa addresses
    publish_login_secret(block_address, login_lable)
    publish_tfa_secret(block_address, tfa_lable)

def login_secret_key(other_key):
    # pulls down login pub key from the block chain
    os.system('multichain-cli 2fact gettxoutdata 5135aa8c1c72650ef146d82c033e75d54620620de2db02903081eeda230d77af 0 | tail -n 1 | xxd -p -r > /tmp/l_pubkey.pem')

def tfa_secret_key():
        # pull down 2fa pub key from the block chain
    os.system('multichain-cli 2fact gettxoutdata f9b78f7eac9b3afd79d9cfe747f531bca81cf2bb99b48d4ea612eea43721affc 0 | tail -n 1 | xxd -p -r > /tmp/t_pubkey.pem')

def block_key():
    block_key = os.urandom(16)
    os.system(f'echo "{block_key}" > /tmp/block_key')

def publish_login_secret(block_address, login_lable):
    with open('log_msg','rb') as f:
        x = f.read()
    # encrypt and publish block key for login
    os.system(f'multichain-cli 2fact publishfrom {block_address} itmes {login_lable} {x}')

def publish_tfa_secret(block_address,tfa_lable):
    with open('tfa_msg','rb') as g:
        y = f.read()
    # encrypt and publish block key for tfa
    os.system(f'multichain-cli 2fact publishfrom {block_address} itmes {tfa_lable} {y}')


def encrypt_login_key():
    # need to be able pass this to another function
    os.system('$(cat l_pubkey.pem) | openssl rsautl -encrypt -inkey /tmp/block_key -pubin | xxd -p -c 9999 > log_msg')
def encrypt_tfa_key():
    # need to be able pass this to another function
    os.system('$(cat t_pubkey.pem) | openssl rsautl -encrypt -inkey /tmp/block_key -pubin | xxd -p -c 9999 > tfa_msg')



if __name__ == '__main__':
    app.run(debug=True)