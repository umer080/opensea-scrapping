from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
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

import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
#driver = webdriver.Chrome(desired_capabilities=caps)
chrome_options = webdriver.ChromeOptions()

# Create a new instance of the Firefox driver
driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                                         chrome_options=chrome_options, desired_capabilities=caps)

driver.get('https://opensea.io/activity')
time.sleep(25)
def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response
activities=[]
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
            print(i['params']['response']['url'])
            if "graphql" in url:
                rsp=driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': i["params"]["requestId"]})
                print(rsp)
                print()

    except:
        pass

    count+=1

print(len(events))
#time.sleep(30)