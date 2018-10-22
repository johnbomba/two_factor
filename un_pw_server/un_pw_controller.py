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
        # submit username and pw from login page
        submitted_username = request.form['username']
        submitted_password = request.form['password']
        result = m.validate_credentials(submitted_username,submitted_password)
        if result:
            # load to /authorize.html
        else:
            # return bad Credentials 

@app.route(/authorize, methods=['GET', 'POST'])
def authorize():
    if request.method == 'GET':
        return render_template('authorzie.html')
    else:
        #submit authentication key from authenticator app
        submitted_key = request.form['Authenticator Key']
        result = m.check_two_factor(submitted_key)
        if result:
            # load index.html
        else:
            # return bad credentials 



@app.route(/index, methods=['GET'])
