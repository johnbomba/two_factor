import time
import os
from flask import Flask, renfer_template, request, redirect, session

app = Flask(__name__)

# need refresh button on the html page and a display pane

@app.route(/, methods=['POST'])
def display_key():
    # needs to display the 6 digit code 
    