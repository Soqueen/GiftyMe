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



@app.route('/')
def index():
    print('Navigate in Home Page')
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('signin.html')


@app.route('/signIn', methods=['POST'])
def login_form():
    email = request.form['email']
    pwd = request.form['pwd']
    data = {'email': email, 'password': pwd}
    result = get_service('login', data)
    if result != False:
        return render_template('profile.html')
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
    data = {'email': email, 'password': pwd}
    result = get_service('login', data)
    if result != False:
        return render_template('profile.html')
    return render_template('/')

@app.route('/valProduct')
def valProduct():
    result = get_service('getAllProduct')
    valGold_id = result['id']
    valGold_name = result['name']
    valSilver_id = result['id']
    valSilver_name = result['name']
    valBronze_id = result['id']
    valBronze_name = result['name']
    # TODO -PLACE
    # return render_template('eventgift.html', gpkg = , 'Love Silver Package', 'Love Si'] )

@app.route('/christmasProduct')
def valProduct():
    result = get_service('getAllProduct')
    chmassGold_id = result['id']
    chmassGold_name = result['name']
    chmassSilver_id = result['id']
    chmassSilver_name = result['name']
    chmassBronze_id = result['id']
    chmassBronze_name = result['name']

@app.route('/halloweenProduct')
def valProduct():
    result = get_service('getAllProduct')
    halGold_id = result['id']
    halGold_name = result['name']
    halSilver_id = result['id']
    halSilver_name = result['name']
    halBronze_id = result['id']
    halBronze_name = result['name']

if __name__ == '__main__':
    socketio.run(app)

