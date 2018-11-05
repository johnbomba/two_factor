#! /usr/bin/env python3
## this goes on the login server

import sqlite3
import mcrpc

def validate_credentials(username, password):
    # connect to the credentails DB
    username = username,
    connection = sqlite3.connect('credentials.db',check_same_thread=False)
    cursor = connection.cursor()
    query = cursor.execute('SELECT username from users WHERE username=?;', username)
    un_result = cursor.fetchone()

    # if the input username is equal to the username in the db return true
    if username == un_result:

        # check for the password
        query2 = cursor.execute('SELECT password from users WHERE username=?;', username)
        pw_query = cursor.fetchone()
        pw_query = pw_query[0]

        # check for the salt 
        query3 = cursor.execute('SELECT salt from users WHERE username=?;', username)
        salt_query = cursor.fetchone()
        salt_query = salt_query[0]

        #convert password to bytes
        password = bytes(password, 'utf-8')        

        # hash the input pw with the salt and check against the db
        hashed_pw = hashlib.pbkdf2_hmac('sha256', password, salt_query, 100000)

        # if the PW is equal to the PW in the db return true 
        if hashed_pw == pw_query:
            cursor.close()
            username = username
            print('true')
            return True

        cursor.close()
        username = username
        return None

    cursor.close()
    username = username
    return None

def retrieve_password():
    # pull down secret key from blockchain
    tx_id = '13918ddbdb573dbcc8b9730f89ac76c6da07209fc2bcef7f07a4cfbc9f33f2d2'
    login_address = '1FmqcFmFxQPbNJuKYvMSu61mWGV1iVtiTqxfUM'
    login_lable = f'{tx_id}-{login_address}'

    # pull down secret msg from blockchain 
    # TODO change port #
    # client = c = mcrpc.RpcClient(f'127.0.0.1', 6270, 'multichainrpc', {tx_id})
    # secret_msg = client.liststreamkeyitems('items', login_lable, count=True, start=1)
    # secret_msg = secret_msg[0]['data']

    password_build = f'multichain-cli 2fact gettxdataout {tx_id} 0'
    password_pipe = subprocess.Popen(password_build, shell=True, stdout=subprocess.PIPE)
    password_tail = subprocess.Popen('tail -n 1', shell=True, stdin=password_pipe.stdout, stdout=subprocess.PIPE)
    password_read = password_tail.stdout
    password = password_read.read()
    return password

def decrypt_password():
    password = retrieve_password()
    encrypted_pw = f'echo {password}'
    encrypted_pw_pipe = subprocess.Popen(encrypted_pw, shell=True, stdout=subprocess.PIPE)
    encrypted_pw_hex = subprocess.Popen('xxd -p -r', shell=True, stdin=encrypted_pw_pipe.stdout, stdout=subprocess.PIPE)
    encrypted_pw_ssl = subprocess.Popen(f'openssl rsautl -decrypt inkey ~/.multichain/2fact/stream-privkeys/{login_address}.pem' shell=True, stdin=encrypted_pw_hex.stdout, stdout=subprocess.PIPE)
    decrypted_pw = encrypted_pw_ssl.stdout
    decrypted_pw = decrypted_pw.read()
    return decrypted_pw

def retrieve_secret_msg():
    message_build = f'multichain-cli 2fact gettxdataout {tx_id} 0'
    message_pipe = subprocess.Popen(message_build, shell=True, stdout=subprocess.PIPE)
    message_tail = subprocess.Popen('tail -n 1', shell=True, stdin=message_pipe.stdout, stdout=subprocess.PIPE)
    message_read = message_tail.stdout
    message = message_read.read()
    return message

def decrypt_secret_msg():
    password = decrypt_password()
    message = retrieve_secret_msg()
    # export the secret_msg to bash
    # decrypt key stored in blockchain
    openssl_echo = f'echo {secret_message}'
    openssl_echo2 = subprocess.Popen(openssl_echo, shell=True, stdout=subprocess.PIPE)
    openssl_enc = subprocess.Popen(f"openssl enc -aes-256-cbc -pass pass:{password} ", shell=True, stdin=openssl_echo2.stdout, stdout=subprocess.PIPE)
    decrypted_msg = openssl_enc.stdout
    decrypted_key = decrypted_msg.read()
    return decrypted_key

def gen_login_code():
    # calls the decrypt key function
    decrypted_key = decrypt_secret_msg()

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

def create_acount(new_username, new_password):
    # username and password inputs
    username = new_username
    password = bytes(new_password, 'utf-8')

    # salt is randomly generated
    salt = os.urandom(16)

    # hash the password with the salt
    hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    connection  = sqlite3.connect('credentials.db', check_same_thread= False)
    cursor      = connection.cursor()
    cursor.execute(
        """INSERT INTO users(
            username,
            password,
            salt
            ) VALUES(
            ?,
            ?,
            ?
            );""", (username, hashed_password, salt)
    )
    connection.commit()
    cursor.close()
    connection.close()
    gen_two_factor()

def gen_two_factor():
    pass

def check_two_factor(submitted_key):
    # if the authentication code is equal to the input code return true
    if submitted_key == gen_login_code():
        return True
    else:
        return False



if __name__ == '__main__':
    create_acount('carter', 'cart')
    # validate_credentials('greg','Gu&essThi@sMo%fo')
