from app import celery

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


auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin")
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
            # payload=ev(payload)
            print(payload)
            task_1.delay()

            return custom_json_response(payload, "Success", 200)
        except Exception as err:
            return custom_json_response({}, str(err), 500)


@celery.task(bind=True, trail=True)
def task_1(self):
     
    response = client.get('https://opensea.io/assets/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/4949',
                        )

    print('Response HTTP Status Code: ', response.status_code)
    page_html = response.content
    soup = BeautifulSoup(page_html, "html.parser")
    lxml_text = etree.HTML(str(soup))
    #print(soup.prettify)
    common(soup,lxml_text)
    # webhook