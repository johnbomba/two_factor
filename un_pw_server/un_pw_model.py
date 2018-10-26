#! /usr/bin/env python3
## this goes on the login server

import sqlite3

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

def decrypt_block_key():
    # pull down secret key from blockchain
    block_address = '15vNHaziST8Qt8JbaSRwvKacBgoXwRjcWVYQfK'
    login_address = '17FpM44bdxjYAKwr9oubZa6phGeLTzXZTrxd5r'
    login_lable = f'{block_address}-{login_address}'

    # pull down secret key from blockchain
    client = c = mcrpc.RpcClient('127.0.0.1', 4790, 'multichainrpc', 'HxYzWMi4deNTX2SzSShDjJ8GvCWB9c9b2WxiLS2FhaHf')
    block_key = client.liststreamkeyitems('items', login_lable, count=True, start=1)
    block_key = block_key[0]['data']

    # export the block_key to bash
    os.environ['SECRET']=block_key

    # decrypt key stored in blockchain
    os.system('DECRYPT=$(echo $SECRET | xxd -p -r | openssl rsautl -decrypt -inkey ~/.multichain/2fact/stream-privkeys/17FpM44bdxjYAKwr9oubZa6phGeLTzXZTrxd5r.pem)')
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
