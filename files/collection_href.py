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

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
#driver = webdriver.Chrome(desired_capabilities=caps)
chrome_options = webdriver.ChromeOptions()

# Create a new instance of the Firefox driver
browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                                         chrome_options=chrome_options, desired_capabilities=caps)

browser.get('https://opensea.io/collection/8-bit-sport-football')

time.sleep(2)

browser.execute_script("""
    let hrefs = [], counter = 1;
    setInterval(() => {
        window.scrollBy(0, 300*counter);
    }, 3000);
""")

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

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


#links=[]
#elems = browser.find_elements_by_css_selector(".styles__StyledLink-sc-l6elh8-0.ekTmzq.Asset--anchor")
#links = [elem.get_attribute('href') for elem in elems]
#main_list = list(set(links) - set(hrf))
#hrf.extend(main_list)
# print(hrf)
#print(len(hrf))