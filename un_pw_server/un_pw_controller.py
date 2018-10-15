import time
import os
from flask import Flask, renfer_template, request, redirect, session

app = Flask(__name__)


@app.route(/login, methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
else:
    submitted_username = request.form['username']
    submitted_password = request.form['password']
    validate(submitted_username,submitted_password)

def validate(submitted_username, submitted_password):
    # need to send credentials to the log in server

@app.route(/index, methods=['GET'])
