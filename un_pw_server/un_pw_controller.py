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
            return redirect('/authorize')
        else:
            # return bad Credentials 

@app.route(/authorize, methods=['GET', 'POST'])
def authorize():
    if request.method == 'GET':
        return render_template('authorzie.html')
    else:
        #submit authentication key from authenticator app
        submitted_key = request.form['Authenticator_Key']
        result = m.check_two_factor(submitted_key)
        if result:
            # load index.html
            return redirect('index.html)
        else:
            # return bad credentials 
            return redirect('/login')

@app.route(/create, methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('create.html')
    else:
        submitted_username = request.form['Username']
        submitted_password = request.form['password']
        m.create_acount(submitted_username,submitted_password)
        render_template('login.html')

# @app.route(/index, methods=['GET'])