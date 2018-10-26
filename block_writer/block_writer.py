#!/usr/bin/env python3 
import os
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def new_key_to_block():
    # pull pub keys from the block chain 
    login_secret_key()
    tfa_secret_key()
    block_key()

    # use addresses to build labels
    block_address = '15vNHaziST8Qt8JbaSRwvKacBgoXwRjcWVYQfK'
    tfa_address = '1PbnmjFeTLHX8gr4HbtynmwX4Ly1Z62dXtpciA'
    login_address = '17FpM44bdxjYAKwr9oubZa6phGeLTzXZTrxd5r'

    login_label = f'{block_address}-{login_address}'
    print(f'login_label {login_label}')
    tfa_label = f'{block_address}-{tfa_address}'
    print(f'tfa_label {tfa_label}')

    # encrypt the secret block key with the login and tfa public keys
    encrypt_login_key()
    encrypt_tfa_key()

    # this calls the publish function for the login and tfa addresses
    publish_login_secret(block_address, login_label)
    publish_tfa_secret(block_address, tfa_label)
    
    return 'This Worked'

def login_secret_key():
    # pulls down login pub key from the block chain
    os.system('multichain-cli 2fact gettxoutdata ded49d0339fae366da6061f7ccc3df83ce018a40dfec3f276916ef63e549c1cd 0 | tail -n 1 | xxd -p -r > /tmp/l_pubkey.pem')
    print('downloaded l_pub')

def tfa_secret_key():
    # pull down 2fa pub key from the block chain
    os.system('multichain-cli 2fact gettxoutdata 65c490da5b043cb90fc6adf1a5b49511d794d70efe876efbbabb988b620847b8 0 | tail -n 1 | xxd -p -r > /tmp/t_pubkey.pem')
    print('downloaded t_pub')

def block_key():
    block_key = os.urandom(16).hex
    os.system(f'echo "{block_key}" > /tmp/block_key')
    print('block key created')

def publish_login_secret(block_address, login_label):
    with open('log_msg','rb') as f:
        x = f.read()
        x = x.hex()
        print(x)
        print(type(x))
    # encrypt and publish block key for login
    os.system(f'multichain-cli 2fact publishfrom {block_address} items {login_label} {x}')

def publish_tfa_secret(block_address,tfa_label):
    with open('tfa_msg','rb') as g:
        y = g.read()
        y = y.hex()
        print(y)
        print(type(y))
    # encrypt and publish block key for tfa
    os.system(f'multichain-cli 2fact publishfrom {block_address} items {tfa_label} {y}')


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