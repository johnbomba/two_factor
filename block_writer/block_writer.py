#!/usr/bin/env python3 
import os
from flask import Flask

import rsa

app = Flask(__name__)

@app.route('/', methods=['GET'])
def new_key_to_block():
    # pull pub keys from the block chain 
    login_secret_key()
    tfa_secret_key()

    block_key()

    # use addresses to build lables
    block_address = '1KNibad2yyoZimaXkDgEzdCgJiRoynqE6bVUTt'
    tfa_address = '1GsqQEwfMfYu773ywxBF7xj4ZBvW8VcQJEEA8i'
    login_address = '1Kgb6cwndPfZWHp62sxqxW15661nafgC1uFHU'

    login_lable = f'{block_address}-{login_address}'
    print(f'login_lable {login_lable}')
    tfa_lable = f'{block_address}-{tfa_address}'
    print(f'tfa_lable {tfa_lable}')
    # encrypt the secret block key with the login and tfa public keys
    encrypt_login_key()
    encrypt_tfa_key()

    # this calls the publish function for the login and tfa addresses
    publish_login_secret(block_address, login_lable)
    publish_tfa_secret(block_address, tfa_lable)
    
    return 'This Worked'

def login_secret_key():
    # pulls down login pub key from the block chain
    os.system('multichain-cli 2fact gettxoutdata 5135aa8c1c72650ef146d82c033e75d54620620de2db02903081eeda230d77af 0 | tail -n 1 | xxd -p -r > /tmp/l_pubkey.pem')
    print('downloaded l_pub')

def tfa_secret_key():
        # pull down 2fa pub key from the block chain
    os.system('multichain-cli 2fact gettxoutdata f9b78f7eac9b3afd79d9cfe747f531bca81cf2bb99b48d4ea612eea43721affc 0 | tail -n 1 | xxd -p -r > /tmp/t_pubkey.pem')
    print('downloaded t_pub')

def block_key():
    block_key = 'HGjgUpkIns6DJs/LA4/55QnBJzFxTp9nIurO4Dr5lKYa9wiL4v6ZRR0o0/LxjxJI' #os.urandom(16).hexdigest
    os.system(f'echo "{block_key}" > /tmp/block_key')
    print('block key created')

def publish_login_secret(block_address, login_lable):
    with open('log_msg','rb') as f:
        x = f.read()
        x = x.hex()
        print(x)
        print(type(x))
    # encrypt and publish block key for login
    os.system(f'multichain-cli 2fact publishfrom {block_address} items {login_lable} {x}')

def publish_tfa_secret(block_address,tfa_lable):
    with open('tfa_msg','rb') as g:
        y = g.read()
        y = y.hex()
        print(y)
        print(type(y))
    # encrypt and publish block key for tfa
    os.system(f'multichain-cli 2fact publishfrom {block_address} items {tfa_lable} {y}')


def encrypt_login_key():
    # need to be able pass this to another function
    os.system('cat /tmp/block_key | openssl rsautl -encrypt -inkey /tmp/l_pubkey.pem -pubin | xxd -p -c 9999 > log_msg')
    print('login_key created')
def encrypt_tfa_key():
    # need to be able pass this to another function
    os.system('cat /tmp/block_key | openssl rsautl -encrypt -inkey /tmp/t_pubkey.pem -pubin | xxd -p -c 9999 > tfa_msg')
    print('tfa_key created')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host= '0.0.0.0', debug=True)