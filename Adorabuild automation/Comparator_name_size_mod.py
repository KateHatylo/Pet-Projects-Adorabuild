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


MOD_NAME = "AdoraBuild: Structures"
DOWNLOAD_DIR = "C:\\Users\\PENGUIN\\Downloads\\"


class Comparator:
    def __init__(self):
        self._driver = None
        self.file_size_text = None
        self.file_name_text = None
        self.actual_file_path = None
        self.actual_file_name = None


    @property
    def driver(self):
        if self._driver:
            return self._driver
        if self._driver is None:
            self._initialize_driver()
            return self._driver

    def _initialize_driver(self):
        if self._driver is None:
            # Avoid blocking while downloading files
            chrome_options = self._create_chrome_options()
            self._driver = webdriver.Chrome(options=chrome_options)

            self._driver.get("https://www.curseforge.com/")
            self._driver.maximize_window()

    def _create_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
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

        return chrome_options


    def run(self):
        try:
            self.compare_name_size()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        finally:
            if self._driver:
                self._driver.quit()


    def compare_name_size(self):
        self.find_mod_page()
        self.search_mod_on_page()
        self.find_and_choose_the_newest_version()
        self.catch_mod_size_on_website()
        self.catch_mod_name_on_website()
        self.download_file()
        self.get_latest_downloaded_file()
        self.check_downloaded_file_name()
        self.compare_file_names()
        self.catch_and_convert_downloaded_file_size()
        self.compare_sizes()


    def find_mod_page(self):
        minecraft_image = self.driver.find_element(By.XPATH, '(//img[@id="row-image" and @alt="Minecraft game art"])[2]')
        minecraft_image.click()
        time.sleep(3)

        input_field = self.driver.find_element(By.XPATH, '//input[@class="search-input-field"]')
        input_field.send_keys(MOD_NAME)
        input_field.send_keys(Keys.RETURN)
        time.sleep(3)


    def search_mod_on_page(self):
        adorabuild_name = self.driver.find_elements(By.XPATH, '//span[@class="ellipsis"]')
        text_found = False
        downloads_text = ""

        for element in adorabuild_name:
            if MOD_NAME in element.text:
                text_found = True
                adorabuild_proj = self.driver.find_element(By.XPATH, './/div[@class=" project-card"]')
                adorabuild_proj.click()
                break
        if not text_found:
            print("Mod not found on the page")
        time.sleep(5)


    def find_and_choose_the_newest_version(self):
        files_button = self.driver.find_element(By.XPATH, '//a[text() = "Files"]')
        files_button.click()
        time.sleep(3)

        game_version_dropdown = self.driver.find_element(By.XPATH, '(//div[@class=" select-dropdown"])[1]')
        game_version_dropdown.click()
        time.sleep(3)

        game_version = self.driver.find_element(By.XPATH, '//div[@class=" select-dropdown"]//li[text()="1.20.2"]')
        game_version.click()
        time.sleep(3)

        mod_loader_dropdown = self.driver.find_element(By.XPATH, '(//div[@class=" select-dropdown"])[2]')
        mod_loader_dropdown.click()
        time.sleep(3)

        mod_loader = self.driver.find_element(By.XPATH, '//ul[@class="dropdown-list"]/li[contains(text(),"Forge")]')
        mod_loader.click()
        time.sleep(3)

        newest_mod_row = self.driver.find_element(By.XPATH, '//a[@class="file-row"]')
        newest_mod_row.click()
        time.sleep(3)


    def catch_mod_size_on_website(self):
        file_size = self.driver.find_element(By.XPATH, '//li[@class="detail-size"]')
        self.file_size_text = file_size.text
        print(self.file_size_text)
        time.sleep(3)


    def catch_mod_name_on_website(self):
        file_name = self.driver.find_element(By.XPATH, '//section[@class="section-file-name"]/p')
        self.file_name_text = file_name.text
        print(self.file_name_text)
        time.sleep(3)


    def download_file(self):
        download_button = self.driver.find_element(By.XPATH, '(//button[@class="btn-cta download-cta"])[2]')
        download_button.click()
        time.sleep(30)


    def get_latest_downloaded_file(self):
        files = os.listdir(DOWNLOAD_DIR)
        matching_files = [f for f in files if self.file_name_text in f]

        if matching_files:
            matching_files.sort(key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)))
            latest_file = matching_files[-1]
            self.actual_file_path = os.path.join(DOWNLOAD_DIR, latest_file)


    def check_downloaded_file_name(self):
        self.actual_file_name = os.path.basename(self.actual_file_path)


    def compare_file_names(self):
        if self.file_name_text in self.actual_file_name:
            print(f"Files have the same name!")
        else:
            print(f"Names are different")


    def catch_and_convert_downloaded_file_size(self):
        if self.actual_file_path:
            actual_file_size = os.path.getsize(self.actual_file_path)
            kb_actual_size = actual_file_size / 1024
            self.kb_actual_size_rounded = round(kb_actual_size, 2)
        else:
            print(f"No matching downloaded file found.")


    def compare_sizes(self):
        file_size_text_float = float(self.file_size_text.rstrip(' KB'))
        if file_size_text_float == self.kb_actual_size_rounded:
            print(f"Files have the same size!")
        else:
            print(f"Sizes are different")


if __name__ == "__main__":
    comparator = Comparator()
    comparator.run()

# 305.23 KB
# adorabuild-structures-1.20.2-forge-1.1.0.jar
# File path: C:\Users\PENGUIN\Downloads\adorabuild-structures-1.20.2-forge-1.1.0.jar
# Files are similar!
# Files have the same size!