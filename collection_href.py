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

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# chrome_options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"')
try:
    browser = webdriver.Chrome(options=chrome_options)
except WebDriverException:
    browser = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                                chrome_options=chrome_options)
browser.set_window_size(1300, 700)
browser.get('https://opensea.io/collection/air22')

time.sleep(2)

browser.execute_script("""
    let hrefs = [], counter = 1;
    setInterval(() => {
        window.scrollBy(0, 800*counter);

    }, 1000);

""")
#div > div:nth-child(1) > div > article > a
hrf=[]
for i in range(10):
    elems = browser.find_elements_by_css_selector(".styles__StyledLink-sc-l6elh8-0.ekTmzq.Asset--anchor")
    links = [elem.get_attribute('href') for elem in elems]
    print(links)
    print("--------------")
    print(len(links))
    time.sleep(2)