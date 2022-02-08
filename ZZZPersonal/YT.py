from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


driver = webdriver.Chrome(ChromeDriverManager().install())
web = webdriver.Chrome()
web.get('http://instagram.com')
time.sleep(5)