from time import sleep
from flask_restful import reqparse, Resource
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

from app import celery
import requests
import datetime

import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Open(Resource):

    def post(self):
        try:
            task = activity_event()
            return custom_json_response({}, False, 200, "Success")
        except Exception as err:
            return custom_json_response({}, str(err), 404)

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

#@celery.task(bind=True, trail=True)
def activity_event():

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    #driver = webdriver.Chrome(desired_capabilities=caps)
    chrome_options = webdriver.ChromeOptions()

    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                                             chrome_options=chrome_options, desired_capabilities=caps)

    driver.get('https://opensea.io/activity')
    time.sleep(5)

    activities=[]
    xtotal=0
    u=0
    while True:
        browser_log = driver.get_log('performance')
        #print(browser_log)
        events = [process_browser_log_entry(entry) for entry in browser_log]
        events = [event for event in events if 'Network.response' in event['method']]
        count=0

        for i in events:
            try:
                if i['params']['type']=='Fetch':
                    print(count)
                    url=i['params']['response']['url']
                    #print(i['params']['response']['url'])
                    if "graphql" in url:
                        u=u+1
                        rsp=driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': i["params"]["requestId"]})
                        #print(rsp)
                        print()
                        resp=json.loads(rsp['body'])
                        xtotal=xtotal+len(resp['data']['assetEvents']['edges'])
                        for i in resp['data']['assetEvents']['edges']:
                            event_relay_id=i['node']['assetQuantity']['asset']['relayId']
                            event_type=i['node']['eventType']
                            slug=i['node']['assetQuantity']['asset']['collection']['slug']
                            token_id=i['node']['id']
                            price=i['node']['price']['quantityInEth']
                            from_account=i['node']['fromAccount']
                            seller=i['node']['seller']
                            r=[]
                            for i in activities:
                               r.append(i['relayId'])
                            if event_relay_id not in r:
                                activity_response={}
                                activity_response['relayId']=event_relay_id
                                activity_response['Type']=event_type
                                activity_response['Collection Slug']=slug
                                activity_response['Token Id']=token_id
                                activity_response['Price']=price
                                activity_response['From Account']=from_account
                                activity_response['Seller']=seller
                                if activity_response not in activities:
                                    activities.append(activity_response)
                                    sending_response=json.dumps(activity_response, default=str)
                                    url="https://core-api.develop.blur.io/hooks/events"
                                    headers = {
                                        'Content-Type': 'application/json'
                                    }
                                    sent = requests.post(url,data=sending_response, headers=headers)
                                    print(sent.json(), flush=True)
            except:
                pass

            count+=1

        print(len(events))
        time.sleep(20)