from selenium import webdriver
import chromedriver_binary
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from constants import *

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(3)
    driver.get(MAIN_PAGE_URL)
    return driver

def login(driver):
    login_link = driver.find_element_by_css_selector(LOGIN_SELECTOR)
    login_link.click()
    if driver.title == LOGIN_PAGE_TITLE:
        driver.find_element_by_name("login_id").send_keys(YOURS_USERNAME)
        driver.find_element_by_name("login_passwd").send_keys(YOURS_PASS)
        driver.find_element_by_class_name("button_next").click()
        return driver
    else:
        print("couldn't go to login page. exit the program")
        driver.quit()
        exit(-1)

def confirm(driver):
    driver.save_screenshot("confirm_page.png")
    driver.find_element_by_class_name(CONFIRM_BUTTON).click()
    return driver

def select_group_number(driver, num):
    if num > 4:
        print("max is 4!\nyou deserve alone!!")
        num = 1
    elif num < 1:
        print("min is 1!\nyou deserve alone!!")
        num = 1
    select = Select(driver.find_element_by_id("res_num_select"))
    select.select_by_index(num-1)

def main():
    #go to main page
    driver = create_driver()

    #go to login page to login_id
    driver = login(driver)

    #back to main page
    while driver.title != MAIN_PAGE_TITLE:
        driver.back()

    #loop until find table available in main page
    while driver.title == MAIN_PAGE_TITLE:
        dt = datetime.datetime.now()
        #how many at the table
        select_group_number(driver, num=FRIENDS)
        available_tables = driver.find_elements_by_css_selector(AVAILABLE_TABLE_SELECTOR)
        if len(available_tables) != 0:
            driver.save_screenshot("available_table.png")
            available_tables[0].click()
        else:
            print("checked at:"+ str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second))
            time.sleep(2)
            driver.refresh()
            continue

    #go to confirm page
    if driver.title == CONFIRM_PAGE_TITLE:
        driver = confirm(driver)
    else:
        print(driver.title)
        print("something wrong!!\nexit the program... contact Toru")
        driver.quit()
        exit(-1)

    #go to confirmed page
    if driver.title == CONFIRMED_PAGE_TITLE:
        driver.save_screenshot("confirmed_page.png")
        print("congrats!! check your email box now!\nexit the program")
        driver.quit()
    else:
        print("almost there...try again")
        driver.quit()
        exit(-1)

if __name__ == '__main__':
    main()
