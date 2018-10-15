#!usr/bin/env python3

import sqlite3


def seed():
    username = input('username > ')
    password = input('password > ')
    connection  = sqlite3.connect('credentials.db', check_same_thread= False)
    cursor      = connection.cursor()
    cursor.execute(
        f"""INSERT INTO users(
            username,
            password
            ) VALUES(
            '{username}',
            '{password}'
        );"""
    )
    connection.commit()
    cursor.close()
    connection.close()

if __name__==('__main__'):
    seed()