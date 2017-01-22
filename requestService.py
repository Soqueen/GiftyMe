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
TENANT = 'conuhack2017'
LANGUAGE = 'en'
CLIENT_ID = 'UZESkK5v7Q6H7i580D1U7Ye8k6zoNhK7'
CLIENT_SECRET = 'LU9kNT0qs79FzZRx'
SUCCESS_CODE = ['200', '201']
TOKEN = "Bearer 021-520e7244-ea6e-4c58-88e6-5179b3ae778a"

def get_new_token():
    url = 'https://api.beta.yaas.io/hybris/oauth2/v1/token'
    headers = {
               'Content-Type':'application/x-www-form-urlencoded'
               }

    payload = "client_id=UZESkK5v7Q6H7i580D1U7Ye8k6zoNhK7&client_secret=LU9kNT0qs79FzZRx&responce_type=token&scope=hybris.tenant%3Dconuhack2017%20hybris.pubsub.topic%3Dhybris.category.assignment-created%20hybris.pubsub.topic%3Dhybris.customer.customer-signup%20hybris.cart_manage%20hybris.checkout_manage%20hybris.pubsub.topic%3Dhybris.checkout.checkout-failure%20hybris.customer_read%20hybris.customer_update%20hybris.customer_create%20hybris.customer_view_profile%20hybris.customer_edit_profile%20hybris.pubsub.topic%3Dhybris.customer.password-reset-requested%20hybris.pubsub.topic%3Dhybris.customer.password-updated%20hybris.pubsub.topic%3Dhybris.customer.customer-oauth-logout%20hybris.pubsub.topic%3Dhybris.customer.customer-oauth-login%20hybris.pubsub.topic%3Dhybris.customer.customer-login%20hybris.pubsub.topic%3Dhybris.customer.customer-logout%20hybris.pubsub.topic%3Dhybris.customer.customer-updated%20hybris.pubsub.topic%3Dhybris.customer.address-created%20hybris.pubsub.topic%3Dhybris.customer.address-updated%20hybris.pubsub.topic%3Dhybris.customer.address-deleted%20hybris.pubsub.topic%3Dhybris.customer.address-tag-added%20hybris.pubsub.topic%3Dhybris.customer.address-tag-deleted%20hybris.pubsub.topic%3Dhybris.customer.customer-account-linked%20hybris.pubsub.topic%3Dhybris.customer.customer-account-unlinked%20hybris.email_view%20hybris.email_manage%20hybris.email_send%20hybris.email_admin%20hybris.order_post%20hybris.order_read%20hybris.order_update%20hybris.order_delete%20hybris.order_view_history%20hybris.order_create%20hybris.pubsub.topic%3Dhybris.order.order-created%20hybris.pubsub.topic%3Dhybris.order.order-status-changed%20hybris.pubsub.topic%3Dhybris.order.order-updated%20hybris.order_update_as_customer%20hybris.schema_manage%20hybris.schema_view%20hybris.schema_admin%20hybris.document_view%20hybris.document_manage%20hybris.document_admin%20hybris.configuration_view%20hybris.configuration_manage%20hybris.configuration_admin%20hybris.price_manage%20hybris.price_delete_all%20hybris.pubsub.topic%3Dhybris.price.price-change%20hybris.pubsub.topic%3Dhybris.price.price%20hybris.product_create%20hybris.product_update%20hybris.product_read_unpublished%20hybris.product_delete%20hybris.product_publish%20hybris.product_unpublish%20hybris.pubsub.topic%3Dhybris.product.product-created%20hybris.pubsub.topic%3Dhybris.product.product-updated%20hybris.pubsub.topic%3Dhybris.product.product-deleted%20hybris.product_delete_all%20hybris.pubsub.topic%3Dhybris.product.all-products-deleted%20hybris.product_migrate%20hybris.search-algolia_read%20hybris.search-algolia_manage%20hybris.search-algolia_index%20hybris.category_read_unpublished%20hybris.category_create%20hybris.category_update%20hybris.category_delete%20hybris.category_publish%20hybris.category_unpublish%20hybris.pubsub.topic%3Dhybris.category.assignments-deleted%20hybris.pubsub.topic%3Dhybris.category.category-deleted%20hybris.pubsub.topic%3Dhybris.category.category-updated%20hybris.pubsub.topic%3Dhybris.category.category-created%20hybris.category_delete_all%20hybris.pubsub.topic%3Dhybris.category.all-categories-deleted%20hybris.pcm_manage%20hybris.pcm_read%20hybris.org_manage%20hybris.org_view%20hybris.org_project_create%20hybris.org_payment%20hybris.org_members%20sap.subscription_provider_view%20sap.bill_view%20sap.invoicerequest_manage%20hybris.org_project_manage%20hybris.account_view%20hybris.account_manage%20hybris.marketplace_subscribe%20sap.subscription_provider_terminate%20hybris.marketplace_submit%20sap.subscription_cancel%20sap.subscription_manage%20hybris.api_manage%20hybris.api_view%20hybris.blocks_view%20hybris.package_view%20hybris.package_manage%20hybris.package_rateplanview%20hybris.package_rateplanmanage%20hybris.market_subscriptions_view%20hybris.market_subscriptions_manage&grant_type=client_credentials"
    r = requests.request("POST", url, data=payload, headers=headers)
    jr=r.json()
    return ('Bearer '+ jr['access_token'])

def request_error(responce):
    # token expired
    if responce.status_code == 401:
        global TOKEN
        TOKEN = get_new_token()
        print("401 error, new token generated: "+TOKEN)
        return -1
    return 0

def get_service(service, **params):
    """
    Request different services to YAAS api
    :param token:
    :param service: Type of service: product, order, price, cart, account, persistence or email
    :param timeout:
    :param params:
    :return: respo;nse from request in json format
    """
    # token = verify_token(token, token_exp_time)
    # 0. POST a product
    """  {
    "id": "5882ece1944b32001d36d422",
    "yrn": "urn:yaas:hybris:product:product:conuhack2017;5882ece1944b32001d36d422",
    "code": "545b4e3dfaee4c10def3db25",
    "name": {},
    "description": {},
    "published": false,
    "media": [
      {
        "id": "bfb861b9-e5f7-47bf-9b6f-74c81bef9356",
        "yrn": "urn:yaas:hybris:product:product-media:conuhack2017;5882ece1944b32001d36d422;bfb861b9-e5f7-47bf-9b6f-74c81bef9356",
        "url": "https://api.us.yaas.io/hybris/media/v2/public/files/5882ed7006f5d2001d2e3cac",
        "contentType": "image/jpeg",
        "createdAt": "2017-01-21T05:11:12.698Z",
        "uploadLink": "https://s3.amazonaws.com/sap.yaas.us.public.media/5882ed7006f5d2001d2e3cac?X-Amz-Security-Token=FQoDYXdzEIb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDAcHPPQ5hWqO%2BfgSFyLLAR01oxtMC6RVGV4sdlWqDegFAKa%2Bb%2FGqMH9AO1J5ZOOVYY6bbOwuR8s1ZrOb%2FrHAccRXiAQGxVX60iUq793S8Oy9SOGXDhaErmSV%2Fsksnwri8ymnpJNE2kO9baXGdY9nXjnIqaL%2BG3Vi8ch3i2f2q71tG5DLaisNC%2BxPV%2BGjwvfk9FE%2FVW40eUvvoJxHvoyvIrQzrN78PAZbUhA0qqvNfe9wA83NSTxsiFFaVONtk0YmDy8M%2FNhx2V%2BmyHYozCFl8Ug9BtEPNULgFqT4KIrZi8QF&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20170121T051112Z&X-Amz-SignedHeaders=content-type%3Bhost&X-Amz-Expires=3600&X-Amz-Credential=ASIAJRQ2ZC3TXLB5SSYA%2F20170121%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b11ac8b58a6f1fb169e4a5966f69f818c31067bcd76435252b69d9d3f32f514a"
      }
    ],
    "metadata": {
      "variants": {
        "options": {},
        "mixins": {}
      },
      "version": 11,
      "createdAt": "2017-01-21T05:08:49.134+0000",
      "modifiedAt": "2017-01-21T19:02:23.846+0000",
      "mixins": {}
    },
    "mixins": {}
  }"""
    if service == 'postProduct':
        url = BASE_URL+'/product'+'/v2/'+TENANT+'/products'
        payload = "{\r\n    \"name\": \"apple1\",\r\n    \"code\": \"apple3\",\r\n    \"description\": \"da la da da da\",\r\n    \"published\":\"true\"\r\n}"
        headers = {
                    'authorization': "Bearer 021-ccf4970e-beaa-4131-8ba1-910122c22c73",
                    'content-language': "pl",
                    'content-type': "application/json"
                }
        r = requests.request("POST", url, data=payload, headers=headers)
        """r.text={
                    "id": "58840a90944b32001d36d763",
                    "yrn": "urn:yaas:hybris:product:product:conuhack2017;58840a90944b32001d36d763",
                    "link": "https://api.beta.yaas.io/hybris/product/v2/conuhack2017/products/58840a90944b32001d36d763"
                }"""
    # 1. GET ALL PRODUCT
    elif service == 'getAllProduct':
        url = BASE_URL+'/product'+'/v2/'+TENANT+'/products'
        headers = {"Authorization": TOKEN, "Accept-Language": "pl", "hybris-languages": "en","Content-Type":"application/json"}
        r = requests.get(url=url,headers=headers)
    #  2.  Get a single product*
    elif service == 'getOneProduct':
        url = BASE_URL+'/product'+'/v2/'+TENANT+'/products'+ ??product id
        headers = {"Authorization": TOKEN, "Accept-Language": "pl", "hybris-languages": "en","Content-Type":"application/json"}
        r = requests.get(url=url,headers=headers)

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
    #  14. Signup
    elif service == 'signUp':
        url = BASE_URL+'/customer/v1/'+TENANT+'/signup'
        headers = {"Authorization": TOKEN,"Content-Type":"application/json"}
        # example of params={'email': 'guanqing.hu@mail.mcgill.ca', 'password': '123123'}
        payload = '''{"email":"'''+params['email']+'''","password":"'''+params['password']+'''"}'''
        # payload = "email={}&password={}".format(params['email'],params['password'])
        r = requests.post(url=url, headers=headers,data=payload)
    #  15. Reset password for customer *

    #  16. Reset-Update password for customer*

    #  17. Change password for customer

    #  18. Customer login*
    elif service == 'login':
        url = BASE_URL+'/customer/v1/'+TENANT+'/login'
        headers = {"Authorization": TOKEN,"Content-Type":"application/json"}
        payload = '''{"email":"'''+params['email']+'''","password":"'''+params['password']+'''"}'''
        r = requests.request("POST", url, data=payload, headers=headers)
        print(r.text)
    #  19. Customer logout *

    ## 20. persistence??

#     if request_type == 'get':
#         try:
#             r = requests.get(url=url,
#                              headers=header)
#         except Exception as e:
#             print('Exception: ', e)
#             flash(u'Unable to get product')
#             return False
#     elif request_type == 'post':
#         r = requests.post(url=url, data=json.dump(data), headers=header)
    # 21 get all customers

    elif service == 'getAllCustomer':
        url = BASE_URL+'/customer/v1/'+TENANT+'/customers'
        headers = {"Authorization": TOKEN,"Content-Type":"application/json"}
        r = requests.request("GET", url, headers=headers)
    
    status = request_error(r)
    # -1 : token expire error
    ####################### RISKY OF INFINITE LOOP ##########################3
    # if status==-1:
    #     get_service(token, service, token_exp_time, request_type, **params)

    return r.json()



