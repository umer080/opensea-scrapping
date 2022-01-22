from flask_restful import reqparse, Resource
from utils.amazon_common import custom_json_response
import json
import requests
import time
from flask import Flask 
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from app import cache
from ast  import literal_eval as ev
from .orderbook import common
import time
from scrapingbee import ScrapingBeeClient
client = ScrapingBeeClient(api_key='3E411HQ2N1WG5EMXNGYNSG1D06OZOZH4MMGLD4B7PBL5E5QFV4MF4LCO40N3WF78OKYSTOQE2FCZJNEN')
import asyncio
from bs4 import BeautifulSoup
from lxml import etree #alternative of xpaths in beautifulsoup
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("494E85F37AD34F748D7BBD4A1409F5AA")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

orderbook_parser = reqparse.RequestParser()

orderbook_parser.add_argument(
    "nft_address", dest="nft_address",
    location='json', required=True,
    help='nft_address is missing',
    )


class NftOrderbook(Resource):

    @auth.login_required
    def post(self):
        try:
            print("here", flush=True)
            flag=True
            args = orderbook_parser.parse_args()
            print(args)
            payload = args.nft_address
            logging.info(payload)
            # payload=ev(payload)
            print(payload)
            asyncio.run(task_1(payload))

            return custom_json_response(payload, "Success", 200)
        except Exception as err:
            return custom_json_response({}, str(err), 200)



async def task_1(payload):

    response = client.get(payload)

    print('Response HTTP Status Code: ', response.status_code)
    page_html = response.content
    soup = BeautifulSoup(page_html, "html.parser")
    lxml_text = etree.HTML(str(soup))
    #print(soup.prettify)
    main_dict=common(soup,lxml_text)
    sending_response=json.dumps(main_dict, default=str)
    url="https://core-api.develop.blur.io/hooks/token-orderbook"
    headers = {
        'Content-Type': 'application/json'
    }
    sent = requests.post(url,data=sending_response, headers=headers)
    print(sent.json(), flush=True)
    # webhook