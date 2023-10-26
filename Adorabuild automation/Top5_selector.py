'''
This script checks if AdoraBuild: Structures is in top5 in its category
(Adventure and RPG + World Gen + Structures) and displays the result
'''

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains


MOD_NAME = "AdoraBuild: Structures"
MOD_LOADER_FORGE = "Forge"
MOD_LOADER_FABRIC = "Fabric"


class Top5Selector:
    def __init__(self):
        self._driver = None


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
            self.select_top_5()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
        finally:
            if self._driver:
                self._driver.quit()


    def select_top_5(self):
        self.choose_minecraft_mods_section()
        self.close_cookies_popup()
        self.choose_popularity_filter()
        self.select_minecraft_filters()
        self.select_forge_filter()
        self.check_if_mod_in_top_5(MOD_LOADER_FORGE)
        self.select_forge_filter()
        self.select_fabric_filter()
        self.check_if_mod_in_top_5(MOD_LOADER_FABRIC)


    def choose_minecraft_mods_section(self):
        # Find the Minecraft image and click it
        minecraft_image = self.driver.find_element(By.XPATH, '(//img[@id="row-image" and @alt="Minecraft game art"])[2]')
        minecraft_image.click()
        time.sleep(3)

        # Find and click the categories button
        categories_button = self.driver.find_element(By.XPATH, '//button[@class="opener"]')
        categories_button.click()
        time.sleep(3)

        # Find and click the Minecraft Mods option
        mods_option = self.driver.find_element(By.XPATH, '//a[@href="/minecraft/search?page=1&pageSize=20&sortType=1&class=mc-mods"]')
        mods_option.click()
        time.sleep(5)


    def close_cookies_popup(self):
        cookies_get_it_button = self.driver.find_element(By.XPATH, '//*[@id="cookiebar-ok"]')
        cookies_get_it_button.click()
        time.sleep(5)


    def choose_popularity_filter(self):
        sort_by_dropdown = self.driver.find_element(By.XPATH, '(//div[@class=" dropdown"])[2]')
        sort_by_dropdown.click()
        time.sleep(5)

        popularity_option = self.driver.find_element(By.XPATH, '//ul[@class="dropdown-list"]/li[text()="Popularity"]')
        popularity_option.click()

        self.driver.execute_script("window.scrollBy(0, 800)", "")
        time.sleep(15)


    def select_minecraft_filters(self):
        # Choose the Adventure and RPG checkbox
        adventure_checkbox = self.driver.find_element(By.XPATH, '//label[text()="Adventure and RPG"]')
        adventure_checkbox.click()
        time.sleep(3)

        # Scroll the inner checkbox container 
        checkbox_container = self.driver.find_element(By.XPATH, '//ul[@id="cats-list-container"]')
        scroll_script = "arguments[0].scrollBy(0, 500);"
        self.driver.execute_script(scroll_script, checkbox_container)
        time.sleep(3)

        # Choose the World Generation checkbox
        world_generation_checkbox = self.driver.find_element(By.XPATH, "//label[text()='World Gen']")
        world_generation_checkbox.click()
        time.sleep(3)

        # Expand the inner checkbox container
        expander = self.driver.find_element(By.XPATH, '(//a[@class="icon-expand-collapse"])[3]')
        expander.click()
        time.sleep(3)

        # Choose the Structures checkbox
        structures_checkbox = self.driver.find_element(By.XPATH, '//label[text()="Structures"]')
        structures_checkbox.click()
        time.sleep(3)

        self.driver.execute_script("window.scrollBy(0, 800)", "")
        time.sleep(10)

        # Choose '1.20.2 version' in the dropdown
        game_version_dropdown = self.driver.find_element(By.XPATH, '(//div[@class=" dropdown"])[1]')
        game_version_dropdown.click()
        time.sleep(5)

        game_version = self.driver.find_element(By.XPATH, '//ul[@class="dropdown-list"]/li[text()="1.20.2"]')
        game_version.click()
        time.sleep(10)

        self.driver.execute_script("window.scrollBy(0, -800)", "")
        time.sleep(10)


    def select_forge_filter(self):
        forge_checkbox = self.driver.find_element(By.XPATH, '//label[@title="Forge"]/input[@type="checkbox"]')
        forge_checkbox.click()
        time.sleep(5)


    # Check if Adorabuild: Structures is presented in Top5 on page
    def check_if_mod_in_top_5(self, loader):
        top5 = self.driver.find_elements(By.XPATH, '//span[@class="ellipsis"]')[:10]

        mod_found = False

        for element in top5:
            if MOD_NAME in element.text:
                mod_found = True
                break

        if mod_found:
            print(f"{MOD_NAME} {loader} is in top 5!")
        else:
            print(f"{MOD_NAME} {loader} is not in top 5!") 


    def select_fabric_filter(self):
        fabric_checkbox = self.driver.find_element(By.XPATH, '//label[@title="Fabric"]/input[@type="checkbox"]')
        fabric_checkbox.click()
        time.sleep(5)


if __name__ == "__main__":
    top5Selector = Top5Selector()
    top5Selector.run()


# AdoraBuild: Structures Forge is in top 5!
# AdoraBuild: Structures Fabric is in top 5!