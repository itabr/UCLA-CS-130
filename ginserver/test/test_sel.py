from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument("--test-type");
options.add_argument("--start-maximized");
options.add_argument("--disable-web-security");
options.add_argument("--allow-file-access-from-files");
options.add_argument("--allow-running-insecure-content");
options.add_argument("--allow-cross-origin-auth-prompt");
options.add_argument("--allow-file-access");

driver = webdriver.Chrome(executable_path="./chromedriver",chrome_options=options)

# test homepage
driver.get("http://127.0.0.1:8080/")
time.sleep(10)
driver.find_element_by_id('workplace').click()
time.sleep(10)

# test wrokpalace
driver.get("http://127.0.0.1:8080/workplace/test")
elem = driver.find_element_by_class_name("CodeMirror-code")
contents = driver.find_element_by_id("editor").get_attribute('value')
time.sleep(10)

# test tag botton
driver.find_element_by_id('TagBtn').click()
time.sleep(10)
driver.close()