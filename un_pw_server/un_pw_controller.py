#! /usr/bin/env python3
# this goes on the login server

from flask import Flask, request, redirect, session, flash, render_template

import un_pw_model as m

app = Flask(__name__)
app.secret_key = 'correct-horse-battery-staple'

@app.route('/')
def redirect_to_login():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
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
            flash("Bad Credentials. Please try again", 'danger')
            return redirect('/login')

@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    if request.method == 'GET':
        return render_template('authorzie.html')
    
    else:
        #submit authentication key from authenticator app
        submitted_key = request.form['Authenticator_key']
        result = m.check_two_factor(submitted_key)

        if result:
            # load index.html
            session['authenticated'] = True
            return redirect('/index')
        
        else:
            # return bad credentials 
            flash("Bad Credentials. Please try again", 'danger')
            return redirect('/login')

@app.route('/create', methods=['GET', 'POST'])
def create_account():
        # submit username and pw from account creation page 
        submitted_username = request.form['username']
        submitted_password = request.form['password']

        # call model create account function
        m.create_acount(submitted_username, submitted_password)
        render_template('login.html')

@app.route('/index', methods=['GET','POST'])
def display_index():
    if request.method == 'GET':
        if not session.get('authenticated'):
            return redirect('/login')
        print("GET")
        return render_template('dashboard.html')
    else:
        return 'post'

if __name__ =="__main__":
    app.run('127.0.0.1', port=5001, debug=True)
    app.run('0.0.0.0', debug=True)