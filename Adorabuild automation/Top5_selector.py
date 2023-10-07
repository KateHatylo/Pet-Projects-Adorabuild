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


def main():
    global driver
    try:
        driver = setup_chrome_driver()
        choose_minecraft_mods_section()
        close_cookies_popup()
        choose_popularity_filter()
        select_minecraft_filters()

        select_forge_filter()
        text_found_forge = check_if_mod_in_top_5(MOD_NAME)
        if text_found_forge:
            print(f"{MOD_NAME} {MOD_LOADER_FORGE} is in top 5!")
        else:
            print(f"{MOD_NAME} {MOD_LOADER_FORGE} is not in top 5!")

        unselect_forge_select_fabric()
        text_found_fabric = check_if_mod_in_top_5(MOD_NAME)
        if text_found_fabric:
            print(f"{MOD_NAME} {MOD_LOADER_FABRIC} is in top 5!")
        else:
            print(f"{MOD_NAME} {MOD_LOADER_FABRIC} is not in top 5!")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        driver.quit()


def setup_chrome_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.curseforge.com/")
    driver.maximize_window()
    return driver


def choose_minecraft_mods_section():
    # Find the Minecraft image and click it
    minecraft_image = driver.find_element(By.XPATH, '(//img[@id="row-image" and @alt="Minecraft game art"])[2]')
    minecraft_image.click()
    time.sleep(3)

    # Find and click the categories button
    categories_button = driver.find_element(By.XPATH, '//button[@class="opener"]')
    categories_button.click()
    time.sleep(3)

    # Find and click the Minecraft Mods option
    mods_option = driver.find_element(By.XPATH, '//a[@href="/minecraft/search?page=1&pageSize=20&sortType=1&class=mc-mods"]')
    mods_option.click()
    time.sleep(5)


def close_cookies_popup():
    cookies_get_it_button = driver.find_element(By.XPATH, '//*[@id="cookiebar-ok"]')
    cookies_get_it_button.click()
    time.sleep(5)


def choose_popularity_filter():
    sort_by_dropdown=driver.find_element(By.XPATH, '(//div[@class=" dropdown"])[2]')
    sort_by_dropdown.click()
    time.sleep(5)

    popularity_option = driver.find_element(By.XPATH, '//ul[@class="dropdown-list"]/li[text()="Popularity"]')
    popularity_option.click()

    driver.execute_script("window.scrollBy(0, 800)", "")
    time.sleep(15)


def select_minecraft_filters():
    # Choose the Adventure and RPG checkbox
    adventure_checkbox = driver.find_element(By.XPATH, '//label[text()="Adventure and RPG"]')
    adventure_checkbox.click()
    time.sleep(3)

    # Scroll the inner checkbox container 
    checkbox_container = driver.find_element(By.XPATH, '//ul[@id="cats-list-container"]')
    scroll_script = "arguments[0].scrollBy(0, 500);"
    driver.execute_script(scroll_script, checkbox_container)
    time.sleep(3)

    # Choose the World Generation checkbox
    world_generation_checkbox = driver.find_element(By.XPATH, "//label[text()='World Gen']")
    world_generation_checkbox.click()
    time.sleep(3)

    # Expand the inner checkbox container
    expander = driver.find_element(By.XPATH, '(//a[@class="icon-expand-collapse"])[3]')
    expander.click()
    time.sleep(3)

    # Choose the Structures checkbox
    structures_checkbox = driver.find_element(By.XPATH, '//label[text()="Structures"]')
    structures_checkbox.click()
    time.sleep(3)

    # Scroll the page
    driver.execute_script("window.scrollBy(0, 800)", "")
    time.sleep(10)

    # Choose '1.20.2 version' in the dropdown
    game_version_dropdown = driver.find_element(By.XPATH, '(//div[@class=" dropdown"])[1]')
    game_version_dropdown.click()
    time.sleep(5)

    game_version = driver.find_element(By.XPATH, '//ul[@class="dropdown-list"]/li[text()="1.20.2"]')
    game_version.click()
    time.sleep(10)

    driver.execute_script("window.scrollBy(0, -800)", "")
    time.sleep(10)


def select_forge_filter():
    forge_checkbox = driver.find_element(By.XPATH, '//label[@title="Forge"]/input[@type="checkbox"]')
    forge_checkbox.click()
    time.sleep(5)


# Check if Adorabuild: Structures is presented in Top5 on page (Forge loader)
def check_if_mod_in_top_5(MOD_NAME):
    top5 = driver.find_elements(By.XPATH, '//span[@class="ellipsis"]')[:10]

    for element in top5:
        if MOD_NAME in element.text:
            return True

    return False
  

# Check if Adorabuild: Structures is presented in Top5 on page (Fabric loader)
def unselect_forge_select_fabric():
    select_forge_filter()
    fabric_checkbox = driver.find_element(By.XPATH, '//label[@title="Fabric"]/input[@type="checkbox"]')
    fabric_checkbox.click()
    time.sleep(5)


if __name__ == "__main__":
    main()


# AdoraBuild: Structures Forge is in top 5!
# AdoraBuild: Structures Fabric is in top 5!