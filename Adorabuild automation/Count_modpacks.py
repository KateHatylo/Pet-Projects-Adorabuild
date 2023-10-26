'''
This script extracts the number of modpacks in which AdoraBuild: Structures is included
and saves the results in the txt.file on the desktop
'''


import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class ModpackScraper:
    def __init__(self):
        self._driver = None


    @property
    def driver(self):
        if self._driver:
            return self._driver
        if self._driver is None:
            self._driver = webdriver.Chrome()
            self._driver.get("https://www.modpackindex.com/modpacks")
            self._driver.maximize_window()
            return self._driver


    def run(self):
        try:
            self.check_modpack_number()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        finally:
            if self._driver:
                self._driver.quit()


    def check_modpack_number(self):
            self.find_adorabuild_page()
            self.extract_modpack_info()
            self.extract_today_date()
            self.show_info()
            self.save_info_to_file()


    def find_adorabuild_page(self):
        finder_section = self.driver.find_element(By.XPATH, '//a[@href = "/modpack/finder"]')
        finder_section.click()

        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(5)

        input_field = self.driver.find_element(By.XPATH, '(//input[@class = "select2-search__field"])[2]')
        input_field.send_keys("AdoraBuild: Structures")
        time.sleep(5)
        input_field.send_keys(Keys.ENTER)
        time.sleep(5)

        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(5)

        search_button = self.driver.find_element(By.XPATH, '//button[@class = "btn bg-blue"]')
        search_button.click()
        time.sleep(5)

        self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(5)


    def extract_modpack_info(self):
        modpacks_info = self.driver.find_element(By.ID, "modpacks-table_info")
        modpacks_info_text = modpacks_info.text
        sentence = modpacks_info_text.split()
        self.modpacks_no = sentence[-2]


    def extract_today_date(self):
        today_date = date.today()
        self.today_date_str = today_date.strftime("%d/%m/%Y")


    def show_info(self):
        print (f"Total modpacks count: {self.modpacks_no} as of {self.today_date_str}.")


    def save_info_to_file(self):
        desktop_path = "C:/Users/PENGUIN/Desktop/"
        file_path = desktop_path + "modpacks_count.txt"
        with open(file_path, "a") as file:
            file.write(f"Total modpacks count: {self.modpacks_no} as of {self.today_date_str}\n")


if __name__ == "__main__":
    scraper = ModpackScraper()
    scraper.run()