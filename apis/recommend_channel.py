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
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

recommendation_parser = reqparse.RequestParser()

recommendation_parser.add_argument(
    "followups", dest="followups",
    location='json', required=True,
    help='followups is missing',
    )


class RecommendChannel(Resource):

    @auth.login_required
    def post(self):
        try:
            print("here", flush=True)
            flag=True
            args = recommendation_parser.parse_args()
            print(args)
            payload = args.followups
            payload=ev(payload)
            print(payload)
            print(payload[0]['number'])
            numbers=["+15612718275", "+19546483989", "+14159007571", "+15615126132", "+17867659578"]
            if payload[0]["number"] in numbers:
                if payload[0]["email"]:
                    payload[0]['channel']=9
                else:
                    payload[0]['channel']=2
            print(payload)

            return custom_json_response(payload, "Success", 200)
        except Exception as err:
            return custom_json_response({}, str(err), 500)
