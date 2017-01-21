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

BASE_URL = 'https://api.beta.yaas.io/hybris'
TENANT = 'conuhack2017.myapp'
LANGUAGE = 'en'
CLIENT_ID = 'UZESkK5v7Q6H7i580D1U7Ye8k6zoNhK7'
CLIENT_SECRET = 'LU9kNT0qs79FzZRx'
SUCCESS_CODE = ['200', '201']


def get_service(token, service, token_exp_time, request_type, **params):
    """
    Request different services to YAAS api
    :param token:
    :param service: Type of service: product, order, price, cart, account, persistence or email
    :param token_exp_time:
    :param token_acc_time:
    :param request_type:
    :param timeout:
    :param params:
    :return: response from request in json format
    """
    # token = verify_token(token, token_exp_time)

    # 1. GET ALL PRODUCT
    url = BASE_URL.join(['product', 'v2', TENANT, 'products'])
    if service == 'getAllProduct':
        header = {'Authorization': token, 'Accept-Language': LANGUAGE, 'hybris-languages': LANGUAGE}

    # TODO: Bonnie :)
    #  2.  Get a single product*
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
    elif service == 'login':
        url = os.path.join(BASE_URL, 'customer', 'v1', TENANT, 'login')
        header = {'Authorization': token, 'Accept-Language': LANGUAGE, 'hybris-languages': LANGUAGE}
        data = {'email': params['email'], 'password': params['password']}
    #  19. Customer logout *

    ## 20. persistence??

    if request_type == 'get':
        try:
            r = requests.get(url=url,
                             headers=header)
        except Exception as e:
            print('Exception: ', e)
            flash(u'Unable to get product')
            return False
    elif request_type == 'post':
        r = requests.post(url=url, data=json.dump(data), headers=header)
    return r.json()


# def verify_token(token, expired_time):
#     """
#     check if token is expired before calling the service
#     :param token: the authentication to access Yaas api service
#     :return: token
#     """
#     # compare the time expired to the request time
#     # TODO-Python intervention : get a better comparison
#     # TODO Get current time
#     access_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#     if access_time > expired_time:
#         # request new token
#         # TODO: NOT A GOOD FORM JUST A PLACE HOLDER
#         url = BASE_URL.join(TENANT, CLIENT_ID, CLIENT_SECRET)
#         try:
#             r = requests.get(url=url)
#             response = r.json()
#             request_code = r.status_code
#             print('Renew Token:{request_result}'.format(request_request=request_code))
#             if request_code not in SUCCESS_CODE:
#                 # TODO: display error message to user
#                 return False
#             token = response  # TODO: GRAPH THE JSON FOR TOKEN IF NECESSARY
#         except Exception as e:
#             print('exception: ', e)
#             return False
#     return token
