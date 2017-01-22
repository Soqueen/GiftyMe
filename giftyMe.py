import json
import os

from flask import flash, Flask, jsonify, redirect, request, render_template
from flask_socketio import SocketIO
# from time import gmtime, strftime
# from urllib import *

app = Flask(__name__)
app.secret_key = "GiftMe"
app.config.from_object(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    print('Navigate in index.html')
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('signin.html')


@app.route('/signIn', methods=['POST'])
def login_form():
    email = request.form['email']
    pwd = request.form['pwd']
    # TODO- CALL API FOR VERIFY THE LOGIN
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
    # if conf_pwd != pwd:
    #     flash(u'Your passwords do not match!')
    #     return render_template('register.html')
    # TODO- CALL API FOR Register the new user
    return redirect('/')

if __name__ == '__main__':
    socketio.run(app)

