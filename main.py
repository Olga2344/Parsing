from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
from time import sleep

client = MongoClient('127.0.0.1', 27017)
db = client['db_mail']
mail_ru = db.mail_ru

service= Service('chromedriver.exe')
driver= webdriver.Chrome(service=service)
driver.get('https://account.mail.ru/')
#driver.maximize_window()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "input-0-2-77")))
login=driver.find_element(By.CLASS_NAME, "input-0-2-77")
login.send_keys("study.ai_172@mail.ru")
login.send_keys(Keys.ENTER)
pswd = driver.find_element(By.NAME, "password")
pswd.send_keys("NextPassword172#")
pswd.send_keys(Keys.ENTER)
action = ActionChains(driver)

mail_url=driver.find_elements(By.LINK_TEXT, '/inbox/0:')
#print(mail_url)

mails = driver.find_elements(By.CLASS_NAME, 'llc__container')
#print(len(mails))

link_list = []
check = None
while True:
    mails = driver.find_elements(By.CLASS_NAME, 'llc__container')
    if mails[-1] == check:
        break
    for link in mails:
        if link:
            elem = link.get_attribute('href')
            if elem not in link_list:
                link_list.append(elem)
        check = mails[-1]
        action.move_to_element(check)
        action.perform()
        sleep(3)

letter_information = {}
for link in link_list:
    driver.get(link)
    letter_information = {
        'author': driver.find_element(By.XPATH, "//div[@class='letter__author']/span").text,
        'letter__author': driver.find_element(By.XPATH, "//div[@class='letter__author']/span").get_attribute('title'),
        'email_date': driver.find_element(By.XPATH, "//div[@class='letter__author']/div").text,
        'email_title': driver.find_element(By.TAG_NAME, 'h2').text,
        'link': link}
        mail_ru.insert_one(letter_information)



