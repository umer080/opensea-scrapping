
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

driver.get('https://opensea.io/collection/the-mike-trout-cyber-trout-limited-edition-collect')

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
def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response
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