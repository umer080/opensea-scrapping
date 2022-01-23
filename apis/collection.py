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
from app import celery
from scrapingbee import ScrapingBeeClient
client = ScrapingBeeClient(api_key='3E411HQ2N1WG5EMXNGYNSG1D06OZOZH4MMGLD4B7PBL5E5QFV4MF4LCO40N3WF78OKYSTOQE2FCZJNEN')
from bs4 import BeautifulSoup
from lxml import etree #alternative of xpaths in beautifulsoup
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from concurrent.futures import ThreadPoolExecutor

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(4)

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
            #executor.submit(task_2, payload)
            task_2.delay(payload)

            return custom_json_response(payload, "Under process not live yet", 200)
        except Exception as err:
            return custom_json_response({}, str(err), 500)

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

celery.task(bind=True, trail=True)
def task_2(self, payload):
    payload=ev(payload)
    print(payload)

    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    #driver = webdriver.Chrome(desired_capabilities=caps)
    chrome_options = webdriver.ChromeOptions()

    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                                             chrome_options=chrome_options, desired_capabilities=caps)
    for i in payload:
        print("NEW COLLECTION")
        driver.get('https://opensea.io/collection/'+str(i))

        items = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[5]/div/div[1]/a/div/div[1]/span')
        owners = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[5]/div/div[2]/a/div/div[1]/span/div')
        floor_price = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[5]/div/div[3]/a/div/div[1]/span/div')
        volume_traded = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[5]/div/div[4]/a/div/div[1]/span/div')
        print(items.text)
        print(owners.text)
        print(floor_price.text)
        print(volume_traded.text)

        driver.execute_script("""
            let hrefs = [], counter = 1;
            setInterval(() => {
                window.scrollBy(0, 800*counter);
            }, 2500);
        """)
        # time.sleep(15)

        activities=[]
        length=0
        u=0
        main_list=[]
        count=0
        hrfs=[]
        prev=0

        full_final=[]
        while True:
            if length==12:
                print("TOP")

                element = driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[2]/div[5]/div/div[1]/a/div/div[1]/span')
                driver.execute_script("return arguments[0].scrollIntoView(true);", element)
            link=[]
            try:
                length=length+1
                elems = driver.find_elements_by_css_selector(".styles__StyledLink-sc-l6elh8-0.ekTmzq.Asset--anchor")
                link = [elem.get_attribute('href') for elem in elems]
                main_list.extend(link)

                main_list=list(set(main_list))

                current=len(main_list)
                if current==prev:
                    count=count+1
                else:
                    count=0
                    prev=len(main_list)

            except:
                pass
            if count==12:
                break

            browser_log = driver.get_log('performance')
            #print(browser_log)
            events = [process_browser_log_entry(entry) for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]
            # count=0

            for i in events:
                try:
                    if i['params']['type']=='Fetch':
                        # print(count)
                        url=i['params']['response']['url']
                        # print(i['params']['response']['url'])
                        if "graphql" in url:
                            rsp=driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': i["params"]["requestId"]})
                            # print(rsp)
                            resp=json.loads(rsp['body'])

                            for i in resp['data']['query']['search']['edges']:
                                address=i['node']['asset']['assetContract']['address']
                                token=i['node']['asset']['tokenId']
                                hrfs.append('https://opensea.io/assets/'+address+'/'+token)
                            u=u+1
                            print()

                except Exception as err:
                    pass

                # count+=1
            print(u)
            time.sleep(10)


        print("================")
        print(len(main_list))
        print(main_list)
        print(len(hrfs))
        print(hrfs)
        print("================")

        full_final.extend(main_list)
        full_final.extend(hrfs)
        full_final=list(set(full_final))
        print(len(full_final))
        for each_hrf in full_final:
            print(each_hrf)