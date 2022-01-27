from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

import time

from selenium.webdriver.support import expected_conditions as EC

import pyotp
import os
from dotenv import load_dotenv

# START import secrets
env_path = '/Users/angusmclauchlan/.secrets/itsolver/automation/fetch-bank-statements/.env'
load_dotenv(dotenv_path=env_path)
square_totp = str(os.getenv("square_totp"))
square_user = str(os.getenv("square_user"))
square_pass = str(os.getenv("square_pass"))
# END import secrets

totp = pyotp.TOTP(square_totp)


options = webdriver.ChromeOptions()
# Path to your chrome profile
options.add_argument(
    "user-data-dir=/Users/angusmclauchlan/Library/Application Support/Google/Chrome")
options.add_experimental_option('useAutomationExtension', False)
prefs = {"download.default_directory": "/Users/angusmclauchlan/Projects/itsolver/fetch-bank-statements"}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(
    executable_path="chromedriver", options=options)
time.sleep(2)
driver.get('https://squareup.com/dashboard/sales/transactions')
time.sleep(3)

if(driver.title == "Sign In"):
    # Login
    try:
        # Enter Username and Password then hit ENTER
        email = WebDriverWait(driver, 6).until(EC.presence_of_element_located(
            (By.ID, "email"))).send_keys(square_user)
        password = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.ID, "password"))).send_keys(square_pass, Keys.ENTER)
    except:
        print('had trouble with entering username & password')
        exit()

    # Enter Temporary One-Time Password and click button
    try:
        otp = totp.now()
        verify_code = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, 'verification-code'))).send_keys(otp, Keys.ENTER)
        time.sleep(3)
    except:
        print('had trouble with entering one-time password')
        exit()
elif(driver.title == "Square Dashboard"):
    print("already signed in")

try:
    # export transactions csv
    print('wait here')
    # btn = WebDriverWait(driver, 3).until(
    #     EC.element_to_be_clickable(By.xpath("//button[text()='Transactions CSV']")))
    # btn_transactions_csv = driver.findElement(
    #     By.xpath("//button[text()='Transactions CSV']"))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Export']"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Transactions CSV']"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Export']"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Items Summary CSV']"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Export']"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Items Detail CSV']"))).click()

except:
    print("Error with clicking 'Transactions CSV' button")

print("end.")
