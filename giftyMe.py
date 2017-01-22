import json
import os

from flask import flash, Flask, jsonify, redirect, request, render_template
from flask_socketio import SocketIO
# from time import gmtime, strftime
# from urllib import *
from requestService import get_service

app = Flask(__name__)
app.secret_key = "GiftMe"
app.config.from_object(__name__)
socketio = SocketIO(app)
LOGIN = False
CUSTOMER_TOKEN = None

@app.route('/')
def index():
    print('Navigate in Home Page')
    if LOGIN:
        return render_template('indexprofile.html')
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/event')
def event():
    if LOGIN:
        return render_template('eventgiftprofile.html')
    return render_template('eventgift.html')


@app.route('/valentine_gift')
def valentine_gift():
    return render_template('valentine.html')


@app.route('/halloween_gift')
def halloween_gift():
    return render_template('halloween.html')


@app.route('/christmas_gift')
def christmas_gift():
    return render_template('christmas.html')


@app.route('/login')
def login():
    return render_template('signin.html')


@app.route('/signIn', methods=['POST'])
def login_form():
    email = request.form['email']
    pwd = request.form['pwd']
    result = get_service('login', email=email, password=pwd)
    if result != False:
        global LOGIN
        LOGIN = True
        global CUSTOMER_TOKEN
        CUSTOMER_TOKEN = result['accessToken']
        return render_template('indexprofile.html')
    return render_template('/')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/signUp', methods=['POST'])
def register_form():
    email = request.form['email']
    pwd = request.form['pwd']
    conf_pwd = request.form['conf_pwd']
    firstName = request.form['firstname']
    lastName = request.form['lastname']
    result = get_service('signUp',  email=email, password=pwd)
    if result != False:
        print(result)
        result = get_service('login', email=email, password=pwd)
        if result != False:
            global LOGIN
            LOGIN = True
            global CUSTOMER_TOKEN
            CUSTOMER_TOKEN = result['accessToken']
            return render_template('indexprofile.html')
    return render_template('index.html')


@app.route('/logout')
def logout():

    result = get_service('logout', accessToken=CUSTOMER_TOKEN)
    if result != False:
        return render_template('index.html')


@app.route('/setting')
def setting():
    return render_template('settings.html')
if __name__ == '__main__':
    socketio.run(app)

