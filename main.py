from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    SessionNotCreatedException,
)
from datetime import datetime
from dotenv import load_dotenv
from chromedriver_autoinstaller import install as AutoInstall
import os

load_dotenv()
_email = os.getenv("email")
_pwd = os.getenv("pwd")


def write_file(filename, data):
    if os.path.isfile(filename):
        with open(filename, "a") as f:
            f.write(" " + data)
    else:
        with open(filename, "w") as f:
            f.write(
                "HoneyGain Checker First Active at "
                + print_time().removeprefix("\n").removesuffix(" Status:")
                + "\n"
            )
            f.write(data)


def show_err(context):
    write_file("log.txt", "Error: " + context + "\n")


def print_time():
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d-%H:%M")
    data = "\n" + current_time + " Log start:\n"
    return data


def logininput(driver):
    loginEmail = driver.find_element(by=By.NAME, value="email")
    loginPassword = driver.find_element(by=By.NAME, value="password")
    driver.implicitly_wait(0.5)
    loginEmail.send_keys(_email)
    driver.implicitly_wait(0.5)
    loginPassword.send_keys(_pwd)


write_file("log.txt", print_time())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # hide actual web
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(
    "--ignore-certificate-errors"
)  # prevent certificate errors time out
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# create webdriver
try:
    driver = webdriver.Chrome(options=chrome_options)
except SessionNotCreatedException:
    show_err("SessionNotCreatedException")
    write_file("log.txt", "\n\t Try auto install...\n")
    AutoInstall()
write_file("log.txt", "\tWebDriver Done\n")
driver.get("https://dashboard.honeygain.com")
write_file("log.txt", "\tConnected\n")
driver.implicitly_wait(1)

# cookie acception
blockingBtn = WebDriverWait(driver, timeout=5).until(
    lambda d: d.find_element(
        by=By.XPATH, value='//button[normalize-space()="Accept all"]'
    )
)
blockingBtn.click()
write_file("log.txt", "\tCookie Done\n")
# login
logininput(driver)
# loginPassword = driver.find_element(by=By.NAME, value="password")
# print(loginPassword.text)

loginBtn = WebDriverWait(driver, timeout=5).until(
    lambda d: d.find_element(by=By.CLASS_NAME, value="hg-login-with-email")
)
loginBtn.click()
write_file("log.txt", "\tLogin Done\n")
try:
    checkBtn = WebDriverWait(driver, timeout=5).until(
        lambda d: d.find_element(
            by=By.XPATH, value='//button[normalize-space()="Open Lucky Pot"]'
        )
    )
    checkBtn.click()
    ConsumeBtn = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(by=By.CLASS_NAME, value="bmMrME")
    )
    ConsumeBtn.click()
    write_file("log.txt", "Success\n")
    driver.quit()
    quit()
except NoSuchElementException:
    show_err("CheckBtnNotFound")
except TimeoutException:
    show_err("Timeout")
except ElementClickInterceptedException:
    show_err("ElementClickIntercepted")
write_file("log.txt", "Log Ended\n")
