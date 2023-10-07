'''
This script compares the file name and size of jar file on website
with downloaded one. Through filters I choose the latest version of
mode on CurseForge website and download it to my Downloads folder.
'''

import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = None
MOD_NAME = "AdoraBuild: Structures"
DOWNLOAD_DIR = "C:\\Users\\PENGUIN\\Downloads\\"


def main():
    global driver
    try:
        chrome_options = setup_chrome_driver()
        find_mod_page(MOD_NAME)
        search_mod_on_page(MOD_NAME)
        find_and_choose_the_newest_version()
        file_size_text = catch_mod_size_on_website()
        file_name_text = catch_mod_name_on_website()
        download_file()

        actual_file_path = get_latest_downloaded_file(DOWNLOAD_DIR, file_name_text)
        if actual_file_path:
            print("File path:", actual_file_path)   # Retrieve the latest file from a directory that matches my pattern    
        else:
            print("No matching downloaded file found.")   

        actual_file_name = check_downloaded_file_name(actual_file_path)  # Extract the filename (without the path)

        compare_file_names(file_name_text, actual_file_name)

        kb_size_rounded = catch_and_convert_downloaded_file_size(actual_file_path)  # Remove "KB" from file_size_text and convert it to a float
        if kb_size_rounded is not None:
            compare_sizes(file_size_text, kb_size_rounded)  # Compare sizes

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()


def setup_chrome_driver():
    global driver
    chrome_options = webdriver.ChromeOptions()

    # Avoid blocking while downloading files
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--safebrowsing-disable-download-protection")
    chrome_options.add_argument("--ignore-certificate-errors")

    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.prompt_for_download": "false",
        "download.directory_upgrade": "true",
        "download.default_directory": DOWNLOAD_DIR,
        "safebrowsing.enabled": "false"
    }

    # Avoid parsing Certificate problems
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.curseforge.com/")
    driver.maximize_window()
    time.sleep(5)
    return chrome_options
    

def find_mod_page(MOD_NAME):
    minecraft_image = driver.find_element(By.XPATH, '(//img[@id="row-image" and @alt="Minecraft game art"])[2]')
    minecraft_image.click()
    time.sleep(3)

    input_field = driver.find_element(By.XPATH, '//input[@class="search-input-field"]')
    input_field.send_keys(MOD_NAME)
    time.sleep(2)
    input_field.send_keys(Keys.ENTER)
    time.sleep(3)


def search_mod_on_page(MOD_NAME):
    adorabuild_name = driver.find_elements(By.XPATH, '//span[@class="ellipsis"]')
    text_found = False
    downloads_text = ""

    for element in adorabuild_name:
        if MOD_NAME in element.text:
            text_found = True
            adorabuild_proj = driver.find_element(By.XPATH, './/div[@class=" project-card"]')
            adorabuild_proj.click()
            break
    if not text_found:
        print("Mod not found on page")
    time.sleep(5)


def find_and_choose_the_newest_version():
    files_button = driver.find_element(By.XPATH, '//a[text() = "Files"]')
    files_button.click()
    time.sleep(3)

    game_version_dropdown = driver.find_element(By.XPATH, '(//div[@class=" select-dropdown"])[1]')
    game_version_dropdown.click()
    time.sleep(3)

    game_version = driver.find_element(By.XPATH, '//div[@class=" select-dropdown"]//li[text()="1.20.2"]')
    game_version.click()
    time.sleep(3)

    mod_loader_dropdown = driver.find_element(By.XPATH, '(//div[@class=" select-dropdown"])[2]')
    mod_loader_dropdown.click()
    time.sleep(3)

    mod_loader = driver.find_element(By.XPATH, '//ul[@class="dropdown-list"]/li[contains(text(),"Forge")]')
    mod_loader.click()
    time.sleep(3)

    newest_mod_row = driver.find_element(By.XPATH, '//a[@class="file-row"]')
    newest_mod_row.click()
    time.sleep(3)


def catch_mod_size_on_website():
    file_size = driver.find_element(By.XPATH, '//li[@class="detail-size"]')
    file_size_text = file_size.text
    print(file_size_text)
    time.sleep(3)
    return file_size.text

def catch_mod_name_on_website():
    file_name = driver.find_element(By.XPATH, '//section[@class="section-file-name"]/p')
    file_name_text = file_name.text
    print(file_name_text)
    time.sleep(3)
    return file_name_text

def download_file():

    download_button = driver.find_element(By.XPATH, '(//button[@class="btn-cta download-cta"])[2]')
    download_button.click()
    time.sleep(30)


def get_latest_downloaded_file(DOWNLOAD_DIR, file_name_text):
    files = os.listdir(DOWNLOAD_DIR)
    matching_files = [f for f in files if file_name_text in f]

    if matching_files:
        matching_files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)))  # Sort matching_files by modification time
        latest_file = matching_files[-1]  # Get the latest file from the sorted list
        return os.path.join(DOWNLOAD_DIR, latest_file)  # Build the full path to the latest file

    return None
 

def check_downloaded_file_name(actual_file_path):
    actual_file_name = os.path.basename(actual_file_path)
    return actual_file_name


def compare_file_names(file_name_text, actual_file_name):
    if file_name_text in actual_file_name:
        print("Files are similar!")
    else:
        print("Names are different")


def catch_and_convert_downloaded_file_size(actual_file_path):
    if actual_file_path:
        actual_file_size = os.path.getsize(actual_file_path)
        kb_actual_size = actual_file_size / 1024  # Convert bytes to kilobytes
        kb_actual_size_rounded = round(kb_actual_size, 2)  # Round to one decimal place
        return kb_actual_size_rounded
    else:
        print("No matching downloaded file found.")
        return None


def compare_sizes(file_size_text, kb_actual_size_rounded):
    file_size_text_float = float(file_size_text.rstrip(' KB'))
    if file_size_text_float == kb_actual_size_rounded:
        print("Files have the same size!")
    else:
        print("Sizes are different")


if __name__ == "__main__":
    main()


# 305.23 KB
# adorabuild-structures-1.20.2-forge-1.1.0.jar
# File path: C:\Users\PENGUIN\Downloads\adorabuild-structures-1.20.2-forge-1.1.0.jar
# Files are similar!
# Files have the same size!