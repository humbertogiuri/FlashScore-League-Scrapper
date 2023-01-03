from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import datetime
from time import sleep

def accept_cookies(driver):
    print('Handling with coockies...')
    accept_button = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
    accept_button.click()

def open_all_matchs(driver):
    try:
        while True:
            print('expandindo...')
            
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'event__more.event__more--static'))
            ).click()
            sleep(2)
    
    except TimeoutException:
        print('End of expand matchs...')


def get_all_id_matchs(driver):
    print('Getting all IDs matchs')

    return driver.find_elements(By.CLASS_NAME, 'event__match.event__match--static.event__match--twoLine')


def get_match_stats(id_match):
    print(f'Scrapping Match -> {id_match}')

    match_stats = dict()

    options = Options()
    options.headless
    options.add_argument('--disable-blink-features=AutomationControlled')

    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    driver.get(f'https://www.flashscore.com/match/{id_match}/#/match-summary/match-statistics/0')
    accept_cookies(driver)
    
    tournament_header = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'tournamentHeader__country')))
    
    match_round_element = tournament_header.find_element(By.TAG_NAME, 'a')
    match_stats['Round'] = match_round_element.text.split('ROUND ')[-1]
    
    #Getting All Stats
    all_stats = driver.find_elements(By.CLASS_NAME, 'stat__category')

    #Get Values for each stat (home and away)
    for stat in all_stats:
        stat_name = stat.find_element(By.CLASS_NAME, 'stat__categoryName')
        home_stat = stat.find_element(By.CLASS_NAME, 'stat__homeValue')
        away_stat = stat.find_element(By.CLASS_NAME, 'stat__awayValue')

        match_stats[f'Home {stat_name.text}'] = home_stat.text
        match_stats[f'Away {stat_name.text}'] = away_stat.text
    
    driver.quit()

    return match_stats


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for scrapper specific league')
    parser.add_argument('-c', '--country', type=str, required=True, help='League country. Remember to get the exact name on the flashscore url')
    parser.add_argument('-l', '--league', type=str, required=True, help='League name. Remember to get the exact name on the flashscore url')
    parser.add_argument('-s', '--qtd_seasons', type=int, default=5, help='number of seasons that will be considered')
    parser.add_argument('-y', '--start_year', type=int, default=int(datetime.date.today().year), help='year of the season that you wanna start the scrapper')
    parser.add_argument('-lf', '--log_file', type=str, default='log.txt', help='File name from the log .txt')

    args = parser.parse_args()

    options = Options()
    options.headless
    options.add_argument('--disable-blink-features=AutomationControlled')

    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    
    try:
        driver.get(f"https://www.flashscore.com/football/{args.country}/{args.league}-{args.start_year}/results/")
        accept_cookies(driver)
        sleep(3)
        open_all_matchs(driver)
        matchs_elements = get_all_id_matchs(driver)
        matchs_ids = [x.get_attribute('id').split('_')[-1] for x in matchs_elements]
        match_stats = get_match_stats(matchs_ids[0])
        
        driver.quit()
        

    except Exception as error:
        print(error)
        driver.quit()

    