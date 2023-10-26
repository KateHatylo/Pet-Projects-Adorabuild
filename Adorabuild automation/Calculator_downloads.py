'''
This script calculates the number of mod downloads as of desire date
based on the the average previous number of downloads
'''


import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


MOD_NAME = "AdoraBuild: Structures"


class DownloadsCalculator:
    def __init__(self):
        self._driver = None
        self.downloads_text = None
        self.downloads_no = None
        self.days_between = None
        self.average = None


    @property
    def driver(self):
        if self._driver:
            return self._driver
        if self._driver is None:
            self._driver = webdriver.Chrome()
            self._driver.get("https://www.curseforge.com/")
            self._driver.maximize_window()
            return self._driver


    def run(self):
        try:
            self.calculate_downloads()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        finally:
            if self._driver:
                self._driver.quit()


    def calculate_downloads(self):
        self.click_mod_page()
        self.close_cookies_popup()
        self.fill_input_field_adorabuild()
        self.search_mod_on_page_and_capture_downloads()
        self.convert_downloads_to_numbers()
        self.define_days_between_today_and_creation_date()
        self.count_average_per_day()
        self.define_days_between_today_and_desire_date()
        self.count_expected_downloads()


    def click_mod_page(self):
        minecraft_image = self.driver.find_element(By.XPATH, '(//img[@id="row-image" and @alt="Minecraft game art"])[2]')
        minecraft_image.click()
        time.sleep(3)

        categories_button = self.driver.find_element(By.XPATH, '//button[@class="opener"]')
        categories_button.click()
        time.sleep(3)

        mods_option = self.driver.find_element(By.XPATH, '//a[@href="/minecraft/search?page=1&pageSize=20&sortType=1&class=mc-mods"]')
        mods_option.click()
        time.sleep(3)


    def close_cookies_popup(self):
        cookies_get_it_button = self.driver.find_element(By.XPATH, '//*[@id="cookiebar-ok"]')
        cookies_get_it_button.click()
        time.sleep(5)


    def fill_input_field_adorabuild(self):
        input_field = self.driver.find_element(By.XPATH, '//input[@class="search-input-field"]')
        input_field.send_keys(MOD_NAME)

        search_button = self.driver.find_element(By.XPATH, '//button[@class="btn-single-icon" and @aria-label="Search"]')
        search_button.click()
        time.sleep(5)


    def search_mod_on_page_and_capture_downloads(self):
        adorabuild = self.driver.find_elements(By.XPATH, '//span[@class="ellipsis"]')
        downloads_text = None
        text_found = False

        for element in adorabuild:
            if MOD_NAME in element.text:
                text_found = True
                downloads_element = self.driver.find_element(By.XPATH, './/li[@class="detail-downloads"]')
                downloads_text = downloads_element.text
                break

        if text_found:
            self.downloads_text = downloads_text
        else:
            print("Mod not found on the page.")
                        

    def convert_downloads_to_numbers(self):
        downloads_text = self.downloads_text
        downloads_text = downloads_text.strip()
        if downloads_text[-1].upper() == "K":
            self.downloads_no = float(downloads_text[:-1]) * 1000
        elif downloads_text[-1].upper() == "M":
            self.downloads_no = float(downloads_text[:-1]) * 1000000
        elif downloads_text[-1].upper() == "B":
            self.downloads_no = float(downloads_text[:-1]) * 1000000000
        else:
            print(f"Something wrong with calculations!")


    def define_days_between_today_and_creation_date(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.days_between = abs((datetime.strptime(current_date, "%Y-%m-%d") - datetime(2023, 7, 2)).days)
        print(f"Number of days between today and creation date: {self.days_between}")


    def count_average_per_day(self):
        self.average = self.downloads_no / self.days_between


    def define_days_between_today_and_desire_date(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        desire_date = input(f"Enter the desired date (in format yyyy-mm-dd):")
        futdays_between = abs((datetime.strptime(desire_date, "%Y-%m-%d") - datetime.strptime(current_date, "%Y-%m-%d")).days)
        print(f"Number of days between the desired date and today: {futdays_between}")


    def count_expected_downloads(self):
        if self.downloads_no is not None and self.days_between is not None:
            expected_downloads = int(self.days_between * self.average + self.downloads_no)
            print(f"Expected amount of downloads: {expected_downloads}")
        else:
            print(f"Cannot calculate expected downloads due to missing data.")


if __name__ == "__main__":
    calculator = DownloadsCalculator()
    calculator.run()