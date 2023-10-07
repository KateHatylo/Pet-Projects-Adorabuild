'''
This script extracts the number of modpacks in which AdoraBuild: Structures is included
and saves the results in the txt.file on the desktop
'''

import time
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def main():
    global driver
    try:
        driver = setup_chrome_driver()
        find_adorabuild_page()
        modpacks_no, today_date_str = extract_modpack_info_as_of_today()
        print("Total modpacks count:", modpacks_no, "as of", today_date_str)
        save_info_to_file(modpacks_no, today_date_str)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()


def setup_chrome_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.modpackindex.com/modpacks")
    driver.maximize_window()
    return driver


def find_adorabuild_page():
    finder_section = driver.find_element(By.XPATH, '//a[@href = "/modpack/finder"]')
    finder_section.click()

    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(5)

    input_field = driver.find_element(By.XPATH, '(//input[@class = "select2-search__field"])[2]')
    input_field.send_keys("AdoraBuild: Structures")
    time.sleep(5)
    input_field.send_keys(Keys.ENTER)
    time.sleep(5)

    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(5)

    search_button = driver.find_element(By.XPATH, '//button[@class = "btn bg-blue"]')
    search_button.click()
    time.sleep(5)

    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    time.sleep(5)


def extract_modpack_info_as_of_today():
    modpacks_info = driver.find_element(By.ID, "modpacks-table_info") 
    modpacks_info_text = modpacks_info.text
    sentence = modpacks_info_text.split()
    modpacks_no = sentence[-2]

    today_date = date.today()
    today_date_str = today_date.strftime("%d/%m/%Y")

    return modpacks_no, today_date_str


def save_info_to_file(modpacks_no, today_date_str):
    modpacks_no, today_date_str = extract_modpack_info_as_of_today()
    desktop_path = "C:/Users/PENGUIN/Desktop/"
    file_path = desktop_path + "modpacks_count.txt"
    with open(file_path, "a") as file:
        file.write(f"Total modpacks count: {modpacks_no} as of {today_date_str}\n")
    
    
if __name__ == "__main__":
    main()