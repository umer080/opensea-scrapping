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

from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("494E85F37AD34F748D7BBD4A1409F5AA")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

collection_parser = reqparse.RequestParser()

collection_parser.add_argument(
    "collection", dest="collection",
    location='json', required=True,
    help='collection is missing',
    )


class Collection(Resource):

    @auth.login_required
    def post(self):
        try:
            print("here", flush=True)
            flag=True
            args = collection_parser.parse_args()
            print(args)
            payload = args.collection
            # payload=ev(payload)
            print(payload)
            task_2(payload)

            return custom_json_response(payload, "Success", 200)
        except Exception as err:
            return custom_json_response({}, str(err), 500)

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

#celery.task(bind=True, trail=True)
def task_2(self, payload):

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    #driver = webdriver.Chrome(desired_capabilities=caps)
    chrome_options = webdriver.ChromeOptions()

    # Create a new instance of the Firefox driver
    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                                             chrome_options=chrome_options, desired_capabilities=caps)

    opensea_collection="https://opensea.io/collection/"+str(payload)
    browser.get(opensea_collection)

    time.sleep(3)

    browser.execute_script("""
        let hrefs = [], counter = 1;
        setInterval(() => {
         window.scrollBy(0, 300*counter);
        }, 3000);
    """)

    main_list=[]
    hrf=[]
    prev=0
    while True:
        try:
            links=[]
            elems = browser.find_elements_by_css_selector(".styles__StyledLink-sc-l6elh8-0.ekTmzq.Asset--anchor")
            link = [elem.get_attribute('href') for elem in elems]
            main_list.extend(link)

            main_list=list(set(main_list))

            current=len(main_list)
            if current==prev:
                count=count+1
            else:
                count=0
                prev=len(main_list)

            if count==10:
                break

            browser_log = browser.get_log('performance')
            #print(browser_log)
            events = [process_browser_log_entry(entry) for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]
            print(len(events))

            print("--------------")
        except Exception as err:
            print(str(err))
            pass