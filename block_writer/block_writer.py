#!/usr/bin/env python3 
# this goes on the block writer server
import os
import sys
import subprocess

from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def new_key_to_block():
    # addresses that are used to build labels
    block_address = '1TuA5SDysRHGPgzvqVXgN9kDT88SFa51ZRPcMN'
    tfa_address = '1Sr8mr4pXhcdPTDZhu74iyFAchM3Tt52ZZU5jE'
    login_address = '1FmqcFmFxQPbNJuKYvMSu61mWGV1iVtiTqxfUM'

        # transaction id's for the login and 2fa public keys in the pubkeys stream 
    login_tx_id = 'c8935925db039376fb3778f5a97c14df493c2323f3486e86d02e8336e62af5da'
    tfa_tx_id = '8edb17e166c4ff26402f62dddb9282714de42de603827c2fece48898d2062d96'

    # generate password 
    password = generate_password()

    # pull pub keys from the block chain 
    login_secret_key(login_tx_id)
    tfa_secret_key(tfa_tx_id)
    secret_msg = secret_message()


    #generate lables for the assets stream
    login_label = f'{login_tx_id}-{login_address}'
    print(f'login_label {login_label}')
    tfa_label = f'{tfa_tx_id}-{tfa_address}'
    print(f'tfa_label {tfa_label}')

    # encrypt the secret block key with the login and tfa public keys
    encrypt_l_pw = encrypt_login_pw(password)
    encrypt_t_pw = encrypt_tfa_pw(password)
    encrypt_secret_msg = encrypt_secret_message(secret_msg, password)

    # thess are the publish functions for the secret key , login , and tfa 
    publish_secret_message(block_address, encrypt_secret_msg)
    publish_login_pw(block_address, login_label, encrypt_l_pw)
    publish_tfa_pw(block_address, tfa_label, encrypt_t_pw)
    
    return 'This Worked'

def generate_password():
    # use os.system to generate a pw that will encrypt the secret msg on the block chain 
    os.environ['PASSWORD'] = 'openssl rand -base64 48'
    password = subprocess.run('$PASSWORD', shell=True, stdout=subprocess.PIPE)
    password = password.stdout
    password = password.decode('utf-8')
    print(f'password {password}')
    print(type(password))
    return password

def login_secret_key(login_tx_id):
    # pulls down login pub key from the block chain
    os.system(f'multichain-cli 2fact gettxoutdata {login_tx_id} 0 | tail -n 1 | xxd -p -r > /tmp/l_pubkey.pem')
    print('downloaded l_pub')

def tfa_secret_key(tfa_tx_id):
    # pull down 2fa pub key from the block chain
    os.system(f'multichain-cli 2fact gettxoutdata {tfa_tx_id} 0 | tail -n 1 | xxd -p -r > /tmp/t_pubkey.pem')
    print('downloaded t_pub')

def secret_message():
    # this function creates the block key as a secret message to be used in the 2fa functions on the login and 2fa servers
    secret_msg = os.urandom(16).hex
    print('secret created')
    return secret_msg

def publish_secret_message(block_address, cipher):
    cipher = cipher.decode('utf-8')
    # publish the secret message
    os.system(f"multichain-cli 2fact publishfrom {block_address} items '' {cipher}" )
    print('message published')


def publish_login_pw(block_address, login_label, encrypt_l_pw):
    encrypt_l_pw = encrypt_l_pw.decode('utf-8')
    # publish the encrypted login pw 
    os.system(f"multichain-cli 2fact publishfrom {block_address} access {login_label} {encrypt_l_pw}")
    print('login published')

def publish_tfa_pw(block_address,tfa_label, encrypt_t_pw):
    encrypt_t_pw = encrypt_t_pw.decode('utf-8')
    # publish the encrypted tfa pw
    os.system(f"multichain-cli 2fact publishfrom {block_address} access {tfa_label} {encrypt_t_pw}")
    print('t published')

# TODO rewrite this tomorrow needs subvproccess
def encrypt_secret_message(secret_message, password):
    # used to encrypt the secret message on the block chain
    openssl_echo = f'echo {secret_message}'
    openssl_echo2 = subprocess.Popen(openssl_echo, shell=True, stdout=subprocess.PIPE)
    openssl_enc = subprocess.Popen(f"openssl enc -aes-256-cbc -pass pass:{password} ", shell=True, stdin=openssl_echo2.stdout, stdout=subprocess.PIPE)
    hex_openssl = subprocess.Popen(f"xxd -p -c 99999", shell=True, stdin=openssl_enc.stdout, stdout=subprocess.PIPE)

    cipher = hex_openssl.stdout
    print(f'this is the cipher {cipher}')
    cipher = cipher.read()
    print(cipher)
    # os.system(f"CIPHER=$(echo {secret_message} | openssl enc -aes-256-cbc -pass pass:{password} | xxd -p -c 99999)")
    # cipher = os.environb.get('CIPHER')
    print(f'this is the cipher {cipher}')
    return cipher 

def encrypt_login_pw(password):

    openssl_echo = f'echo {password}'
    openssl_echo2 = subprocess.Popen(openssl_echo, shell=True, stdout=subprocess.PIPE)
    openssl_enc = subprocess.Popen("openssl rsautl -encrypt -inkey /tmp/l_pubkey.pem -pubin", shell=True, stdin=openssl_echo2.stdout, stdout=subprocess.PIPE)
    hex_openssl = subprocess.Popen(f"xxd -p -c 9999", shell=True, stdin=openssl_enc.stdout, stdout=subprocess.PIPE)

    #encrypt_l_pw = subprocess.Popen(["xxd", "-p", "-c", "9999"],stdin=ssl.stdou$
    encrypt_l_pw = hex_openssl.stdout
    encrypt_l_pw = encrypt_l_pw.read()

    print('login_pw created')
    return encrypt_l_pw

def encrypt_tfa_pw(password):
    # need to be able pass this to another function
    openssl_echo = f'echo {password}'
    openssl_echo2 = subprocess.Popen(openssl_echo, shell=True, stdout=subprocess.PIPE)
    openssl_enc = subprocess.Popen("openssl rsautl -encrypt -inkey /tmp/t_pubkey.pem -pubin", shell=True, stdin=openssl_echo2.stdout, stdout=subprocess.PIPE)
    hex_openssl = subprocess.Popen(f"xxd -p -c 9999", shell=True, stdin=openssl_enc.stdout, stdout=subprocess.PIPE)

    #encrypt_t_pw = subprocess.Popen(["xxd", "-p", "-c", "9999"],stdin=ssl.stdou$
    encrypt_t_pw = hex_openssl.stdout
    encrypt_t_pw = encrypt_t_pw.read()

    print('tfa_pw created')
    return encrypt_t_pw

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host= '0.0.0.0', debug=True)
    