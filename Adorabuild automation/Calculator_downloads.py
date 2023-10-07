'''
This script calculates the number of mod downloads as of desire date
based on the the average previous number of downloads
'''

import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


MOD_NAME = "AdoraBuild: Structures"


def main():
    global driver
    try:
        driver = setup_chrome_driver()
        click_mod_page()
        close_cookies_popup()
        fill_input_field_adorabuild()
        text_found, downloads_text = search_mod_on_page_and_capture_downloads(MOD_NAME)

        if text_found:
            downloads_no = convert_downloads_to_numbers(downloads_text)
            if downloads_no is not None:
                print("Number of downloads:", downloads_no)

                current_date = datetime.now().strftime("%Y-%m-%d")
                creation_date = "2023-07-02"
                days_between = define_days_between_today_and_creation_date(
                                current_date, creation_date)
                print("Number of days between today and creation date:", days_between)

                average = count_average_per_day(
                            downloads_no, days_between, 
                            current_date, creation_date)

                desire_date = input("Enter the desired date (in format yyyy-mm-dd):")
                futdays_between = define_days_between_today_and_desire_date(
                                    current_date, desire_date)
                print("Number of days between the desired date and today:", futdays_between)

                expected_downloads = int(futdays_between 
                                        * average 
                                        + downloads_no)
                print("Expected amount of downloads:", expected_downloads)
            else:
                print("No download count found")
        else:
            print("Mod not found on the page")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        driver.quit()


def setup_chrome_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.curseforge.com/")
    driver.maximize_window()
    return driver


def click_mod_page():
    minecraft_image = driver.find_element(By.XPATH, '(//img[@id="row-image" and @alt="Minecraft game art"])[2]')
    minecraft_image.click()
    time.sleep(3)

    categories_button = driver.find_element(By.XPATH, '//button[@class="opener"]')
    categories_button.click()
    time.sleep(3)

    mods_option = driver.find_element(By.XPATH, '//a[@href="/minecraft/search?page=1&pageSize=20&sortType=1&class=mc-mods"]')
    mods_option.click()
    time.sleep(3)


def close_cookies_popup():
    cookies_get_it_button = driver.find_element(By.XPATH, '//*[@id="cookiebar-ok"]')
    cookies_get_it_button.click()
    time.sleep(5)


def fill_input_field_adorabuild():
    input_field = driver.find_element(By.XPATH, '//input[@class="search-input-field"]')
    input_field.send_keys(MOD_NAME)

    search_button = driver.find_element(By.XPATH, '//button[@class="btn-single-icon" and @aria-label="Search"]')
    search_button.click()
    time.sleep(5)


# Search Adorabuild:Structures mod on page and capture downloads number 
def search_mod_on_page_and_capture_downloads(MOD_NAME):
    adorabuild = driver.find_elements(By.XPATH, '//span[@class="ellipsis"]')
    text_found = False
    downloads_text = ""

    for element in adorabuild:
        if MOD_NAME in element.text:
            text_found = True
            downloads_element = driver.find_element(By.XPATH, './/li[@class="detail-downloads"]')
            downloads_text = downloads_element.text
            break

    return text_found, downloads_text


# Convert captured number with K/M/B in usual numbers
def convert_downloads_to_numbers(downloads_text):
    downloads_text = downloads_text.strip()
    if downloads_text[-1].upper() == "K":
        return float(downloads_text[:-1]) * 1000
    elif downloads_text[-1].upper() == "M":
        return float(downloads_text[:-1]) * 1000000
    elif downloads_text[-1].upper() == "B":
        return float(downloads_text[:-1]) * 1000000000
    else:
        print("Something wrong with calculations!")
        return None


# Subtract creation mode date from the today date and count the number of days
def define_days_between_today_and_creation_date(current_date, creation_date):
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    creation_date = datetime.strptime(creation_date, "%Y-%m-%d")
    return abs((current_date - creation_date).days)


# Count the average amount of downloads per day
def count_average_per_day(downloads_no, days_between, 
                        current_date, creation_date):
    days_between = define_days_between_today_and_creation_date(
                    current_date, creation_date)
    average = downloads_no / days_between
    return average


# Subtract the today date from the desired date (taken from user input) and count the number of days
def define_days_between_today_and_desire_date(current_date, desire_date):
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    desire_date = datetime.strptime(desire_date, "%Y-%m-%d")
    return abs((desire_date - current_date).days)


if __name__ == "__main__":
    main()