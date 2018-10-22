#!/usr/bin/env python3


# DB setup on verification server 

import sqlite3

connection = sqlite3.connect('credentials.db',check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE users(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR,
        password VARCHAR,
        salt VARCHAR
    );"""
)
