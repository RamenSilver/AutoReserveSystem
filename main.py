from selenium import webdriver
import chromedriver_binary
import time
import datetime
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from constants import *
import re

r = re.compile("[1-9]$")

def print_congrats_message():
    sleeping = 1

    print("        CCCCCCCCCCCCC     OOOOOOOOO     NNNNNNNN        NNNNNNNN        GGGGGGGGGGGGGRRRRRRRRRRRRRRRRR                  AAA         TTTTTTTTTTTTTTTTTTTTTTT   SSSSSSSSSSSSSSS")
    time.sleep(sleeping)
    print("     CCC::::::::::::C   OO:::::::::OO   N:::::::N       N::::::N     GGG::::::::::::GR::::::::::::::::R                A:::A        T:::::::::::::::::::::T SS:::::::::::::::S")
    time.sleep(sleeping)
    print("  C:::::CCCCCCCC::::CO:::::::OOO:::::::ON:::::::::N     N::::::N  G:::::GGGGGGGG::::GRR:::::R     R:::::R            A:::::::A      T:::::TT:::::::TT:::::TS:::::S     SSSSSSS")
    time.sleep(sleeping)
    print(" C:::::C       CCCCCCO::::::O   O::::::ON::::::::::N    N::::::N G:::::G       GGGGGG  R::::R     R:::::R           A:::::::::A     TTTTTT  T:::::T  TTTTTTS:::::S            ")
    time.sleep(sleeping)
    print("C:::::C              O:::::O     O:::::ON:::::::::::N   N::::::NG:::::G                R::::R     R:::::R          A:::::A:::::A            T:::::T        S:::::S            ")
    time.sleep(sleeping)
    print("C:::::C              O:::::O     O:::::ON::::::N N::::N N::::::NG:::::G    GGGGGGGGGG  R:::::::::::::RR          A:::::A   A:::::A          T:::::T          SS::::::SSSSS    ")
    time.sleep(sleeping)
    print("C:::::C              O:::::O     O:::::ON::::::N   N:::::::::::NG:::::G    GGGGG::::G  R::::R     R:::::R      A:::::AAAAAAAAA:::::A        T:::::T               SSSSSS::::S ")
    time.sleep(sleeping)
    print("C:::::C              O:::::O     O:::::ON::::::N    N::::::::::NG:::::G        G::::G  R::::R     R:::::R     A:::::::::::::::::::::A       T:::::T                    S:::::S")
    time.sleep(sleeping)
    print(" C:::::C       CCCCCCO::::::O   O::::::ON::::::N     N:::::::::N G:::::G       G::::G  R::::R     R:::::R    A:::::AAAAAAAAAAAAA:::::A      T:::::T                    S:::::S")
    print("  C:::::CCCCCCCC::::CO:::::::OOO:::::::ON::::::N      N::::::::N  G:::::GGGGGGGG::::GRR:::::R     R:::::R   A:::::A             A:::::A   TT:::::::TT      SSSSSSS     S:::::S")
    print("   CC:::::::::::::::C OO:::::::::::::OO N::::::N       N:::::::N   GG:::::::::::::::GR::::::R     R:::::R  A:::::A               A:::::A  T:::::::::T      S::::::SSSSSS:::::S")
    print("     CCC::::::::::::C   OO:::::::::OO   N::::::N        N::::::N     GGG::::::GGG:::GR::::::R     R:::::R A:::::A                 A:::::A T:::::::::T      S:::::::::::::::SS ")
    print("        CCCCCCCCCCCCC     OOOOOOOOO     NNNNNNNN         NNNNNNN        GGGGGG   GGGGRRRRRRRR     RRRRRRRAAAAAAA                   AAAAAAATTTTTTTTTTT       SSSSSSSSSSSSSSS   ")

def create_driver():
    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(10)
    driver.get(MAIN_PAGE_URL)
    return driver

def login(driver):
    login_link = driver.find_element_by_css_selector(LOGIN_SELECTOR)
    login_link.click()
    if driver.title == LOGIN_PAGE_TITLE:
        driver.find_element_by_name("login_id").send_keys(YOURS_USERNAME[RESERVER])
        driver.find_element_by_name("login_passwd").send_keys(YOURS_PASS[RESERVER])
        driver.find_element_by_class_name("button_next").click()
        return driver
    else:
        print("couldn't go to login page. exit the program")
        driver.quit()
        exit(-1)

def confirm(driver):
    driver.find_element_by_class_name(CONFIRM_BUTTON).click()
    return driver

def get_max_friends(lst):
    index_manager = 0
#セルリアンで12時台の予約をしたい場合
    #for i in range(1,4):
#セルリアンで13時台の予約をしたい場合
    #for i in range(4,7):
#フクラスで12時台の予約をしたい場合
    #for i in range(1,5):
#フクラスで13時台の予約をしたい場合
    for i in range(5,9):
#何時でも構わない場合
    #for i in range(1,15):
    #for i in range(4,7):
        if lst[4*i].find("残") >= 0:
            index_manager += 1
        max_friends = r.search(lst[4*i+index_manager])
        if max_friends:
            return int(max_friends.group())
    return 0

def select_group_number(driver, num):
    print(num)
    if num > 2:
        print("max is 2!\nyou deserve a pair!!")
        num = 2
    elif num < 1:
        print("min is 1!\nyou deserve alone!!")
        num = 1
    element =  WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.ID, "res_num_select")))
    select = Select(element)
    select.select_by_index(num-1)
    return driver

def procceed_main_page(driver, selector_list):
    driver.implicitly_wait(2)
    while driver.title == MAIN_PAGE_TITLE:
        element =  WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "sub_plan_id_select")))
        select = Select(element)
#セルリアンのみで予約場合、
        #select.select_by_index(1)
#フクラスのみで予約する場合、
        select.select_by_index(2)
#セルリアンでもフクラスでもどちらでも構わない場合、
        #select.select_by_index(0)
        time.sleep(2)
        for selector in selector_list:
            print(selector)
            available_tables = driver.find_elements_by_css_selector(selector)
            if len(available_tables) != 0:
                try:
                    #how many at the table
                    lst = driver.find_element_by_css_selector(selector[:72]).text.splitlines()
                    max_friends = get_max_friends(lst)
                    print(lst)
#最低予約人数が1人の場合、
                    #if max_friends < 1:
#最低予約人数が2人の場合、
                    if max_friends < 2:
                        print("looking for more than 2 ppl")
                        continue
                    driver = select_group_number(driver, max_friends)
                    print(available_tables[0])
                    available_tables[0].click()
                except:
                    print("Avaialble tables are more than one")
                    continue
        else:
            driver.refresh()
            time.sleep(1)
        day = 0
 #       if dt.hour >= 11 and dt.minute >= 0:
 #           print("program finished at {}:{}".format(dt.hour,dt.minute))
 #           break
    return driver

def go_back_to_main(driver):
    if not driver.title == MAIN_PAGE_TITLE:
        driver.get(MAIN_PAGE_URL)
    return driver

def main():
    selector_list = WEEK_AVAILABLE_TABLE_SELECTOR[START_DAY:END_DAY]
    print(selector_list)
    reserved_successfully = False
    #go to main page
    driver = create_driver()

    #go to login page to login_id
    driver = login(driver)
    #back to main page
    driver = go_back_to_main(driver)

    while reserved_successfully == False:

        #loop until find table available in main page
        driver = procceed_main_page(driver, selector_list)
        driver.implicitly_wait(2)
        try:
#            if driver.title == MAIN_PAGE_TITLE:
#                break
            #go to confirm page
            if driver.title == CONFIRM_PAGE_TITLE:
                driver = confirm(driver)

            #go to confirmed page
            if driver.title == CONFIRMED_PAGE_TITLE:
                print_congrats_message()
                print("check your email box now!\nexit the program")
                reserved_successfully = True
            else:
                dt = datetime.datetime.now()
                print("somebody took your table, retry at {}:{}".format(dt.hour,dt.minute))
                driver = go_back_to_main(driver)
        except:
            dt = datetime.datetime.now()
            print("something was wrong, retry at {}:{}".format(dt.hour,dt.minute))
            driver = go_back_to_main(driver)



if __name__ == '__main__':
    main()
