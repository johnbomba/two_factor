#! /usr/bin/env python3
import time
import os
from flask import Flask, renfer_template, request, redirect, session

import un_pw_model as m

app = Flask(__name__)


@app.route(/login, methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        submitted_username = request.form['username']
        submitted_password = request.form['password']
        result = m.validate_credentials(submitted_username,submitted_password)
        if result:
            # go to index 
        else:
            # bad Credentials 

@app.route(/authorize, methods=['GET', 'POST'])


def validate_credentials(submitted_username, submitted_password):
    # if UN & PW are 
@app.route(/index, methods=['GET'])
