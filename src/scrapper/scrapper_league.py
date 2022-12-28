from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import time

def get_by_round(driver):
    all_divs = driver.find_elements(By.CSS_SELECTOR, 'div')
    
    for div in all_divs:
        if div.text == 'BY ROUND':
            return div
    
    return None

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
    
    #Getting the button by round and pressing
    by_round = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/main/div[1]/div[3]/div[1]/div[5]/div/div[1]/div[2]'))
            )
    by_round.click()

    