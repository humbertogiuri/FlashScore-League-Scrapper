from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
from time import sleep

def scroll_page(driver, speed=8):
    current_scroll_position, new_height= 0, 1

    while current_scroll_position <= new_height/2:
        current_scroll_position += speed
        driver.execute_script(f'window.scrollTo(0, {current_scroll_position});')
        new_height = driver.execute_script('return document.body.scrollHeight')

def move_to_element(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for scrapper specific league')
    parser.add_argument('-c', '--country', type=str, required=True, help='League country. Remember to get the exact name on the sofascore url')
    parser.add_argument('-l', '--league', type=str, required=True, help='League name. Remember to get the exact name on the sofascore url')
    parser.add_argument('-i', '--id', type=int, required=True, help='League id. Remember to get the exact id on the sofascore url')
    parser.add_argument('-s', '--qtd_seasons', type=int, default=5, help='number of seasons that will be considered')
    parser.add_argument('-lf', '--log_file', type=str, default='log.txt', help='File name from the log .txt')

    args = parser.parse_args()

    options = Options()
    options.headless
    options.add_argument('--disable-blink-features=AutomationControlled')

    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    try:
        driver.get(f'https://www.sofascore.com/tournament/football/{args.country}/{args.league}/{args.id}')
    
        seasons_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div/button'))
                )
        seasons_button.click()
        #Getting the total of seasons possibles
        seasons_ul = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div[1]/ul'))
                )
        seasons = seasons_ul.find_elements(By.CSS_SELECTOR, 'li')
        seasons_button.click()
        
        #use to load all elements
        scroll_page(driver=driver)

        #Getting the button by round and pressing
        by_round = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/main/div/div[3]/div[1]/div[5]/div/div[1]/div[2]'))                                                
                )
        move_to_element(driver, by_round)
        by_round.click()

        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        total_rounds_button = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)\
                            .until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[3]/div[1]/div[5]/div/div[2]/div/div/div[1]/div/div[1]/div[2]/button')))
                            
        total_rounds_button.click()
        sleep(100)
        driver.quit()

    except Exception as error:
        print(error)
        driver.quit()

    