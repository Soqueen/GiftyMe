import collections
import codecs
import json
import os
import re
import requests
import subprocess


from flask import flash, Flask, jsonify, request, redirect, sessions, send_file, url_for, render_template
from flask_wtf import Form
from flask_socketio import SocketIO
from time import gmtime, strftime
from urllib import *
# from serviceRequest import get_service

app = Flask(__name__)
app.secret_key = "GiftMe"
app.config.from_object(__name__)
socketio = SocketIO(app)

BASE_URL = 'https://api.beta.yaas.io/hybris'
TENANT = 'conuhack2017.myapp'
LANGUAGE = 'en'
CLIENT_ID = 'UZESkK5v7Q6H7i580D1U7Ye8k6zoNhK7'
CLIENT_SECRET = 'LU9kNT0qs79FzZRx'
SUCCESS_CODE = ['200', '201']


# @app.before_request
# def before_request():
#     print("loading config...")


@app.route('/')
def index():
    print('Navigate in index.html')
    return render_template('index.html')


# @app.route('/Product', method=['GET', 'POST'])
# def product():
#     return redirect(url_for(''))


# @app.route('/Order', method=['POST'])
# def order():
#     """
#     Order tab
#     :return:
#     """
#     id_product = request.args.get('id_product')
#     id_user = request.args.get('id_user')
#     payment_credential = request.args.get('payment_credential')


@app.route('/login', methods=['GET'])
def login():
    """
    :return:
    """
    #email = requests.args.get('email')
    #pwd = requests.args.get('pwd')

    # service = 'login_sm'
    # data = {'email': email, 'password': pwd}
    # token_info = get_token()
    # token = token_info['token']
    # token_exp_time = token_info['time_expired']
    # result = get_service(token, service, token_exp_time, 'post', data)
    # if result is not False:
    #     ## TODO: GET customer profile and return approate profile login

    return render_template('singin.html')
    # elif request.method == 'POST':
    #     email = requests.form['email']
    #     pwd = requests.form['pwd']
    #     print(email)
    #     print('pwd: ', pwd)
    # return render_template('index.html')

# def get_token():
#     # TODO - return a dictionary ['token': token, 'expire': expire]
#     token_info = {'token': None, 'time_expired': None}
#     return token_info

# TODO: Services
#  2.  Get single product*
#  3.  Get all prices*
#  4.  Get single price*
#  5.  Create a specific order* (admin)
#  6.  Retrieve a specific Order* (admin)
#  7.  Create a order * (customer)
#  8.  retrieve a list order * (customer)
#  9.  Create customer profile*
#  10. Retrieve customer profile by customer number*
#  11. Update customer profile
#  12. Delete customer profile*
#  13. Create address for given customer*
#  14. Retrieve a list of address for given customer*
#  13. Delete order (admin)
#  14. Send email*
#  15. Reset password for customer *
#  16. Reset-Update password for customer*
#  17. Change password for customer
#  18. Customer login*
#  19. Customer logout *
## 20. persistence??
def my_main():
    socketio.run(app, host='0.0.0.0')
    # app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    socketio.run(app)

