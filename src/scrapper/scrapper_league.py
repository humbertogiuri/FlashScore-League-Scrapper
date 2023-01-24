from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
import undetected_chromedriver as uc
import argparse
import pandas as pd

def get_new_driver():
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--headless")

    service = ChromeService(executable_path=ChromeDriverManager().install())

    driver = uc.Chrome(service=service, options=options)

    return driver

def accept_cookies(driver):
    print('Handling with coockies...')
    accept_button = WebDriverWait(driver, 10).until(
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
    def get_odds():
        print('Getting Odds Win or Lose...')
        driver = get_new_driver()

        driver.get(f'https://www.flashscore.com/match/{id_match}/#/odds-comparison/1x2-odds/full-time')
        odds_win = WebDriverWait(driver, 5).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, 'oddsCell__odd  '))
                )
        
        home = odds_win[0].find_element(By.TAG_NAME, 'span').text
        draw = odds_win[1].find_element(By.TAG_NAME, 'span').text
        away = odds_win[2].find_element(By.TAG_NAME, 'span').text
        
        print('Getting Over/Under 2.5...')
        driver.get(f'https://www.flashscore.com/match/{id_match}/#/odds-comparison/over-under/full-time')
        
        gols_ou = WebDriverWait(driver, 5).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, 'ui-table__row'))
                )

        target_value = "2.5"
        gols_2_5 = next((elem for elem in gols_ou if elem.find_element(By.CLASS_NAME, 'oddsCell__noOddsCell').text == target_value), None)
        
        gols_2_5_odds = [elem.text for elem in gols_2_5.find_elements(By.TAG_NAME, 'span')]     
        
        odds = {
            'Home odd': home,
            'Draw odd': draw,
            'Away odd': away,
            'Over 2.5': gols_2_5_odds[1],
            'Under 2.5': gols_2_5_odds[2]
        }

        driver.quit()
        return odds

    print(f'Scrapping Match -> {id_match}')

    match_stats = dict()

    driver = get_new_driver()

    driver.get(f'https://www.flashscore.com/match/{id_match}/#/match-summary/match-statistics/0')
    accept_cookies(driver)
    
    tournament_header = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'tournamentHeader__country')))
    
    match_round_element = tournament_header.find_element(By.TAG_NAME, 'a')
    match_stats['Round'] = match_round_element.text.split('ROUND ')[-1]
    
    match_stats['Date'] = driver.find_element(By.CLASS_NAME, 'duelParticipant__startTime')\
                                    .find_element(By.TAG_NAME, 'div').text

    teams_names = driver.find_elements(By.CLASS_NAME, 'participant__participantName.participant__overflow')
    
    match_stats['Home'] = teams_names[1].text
    match_stats['Away'] = teams_names[-1].text
    
    score_text = driver.find_element(By.CLASS_NAME, 'detailScore__wrapper').text
    score_text = score_text.replace('\n', ' ')
    teams_gols = score_text.split(' - ')

    match_stats['Score'] = score_text
    match_stats['Home Gols'] = teams_gols[0]
    match_stats['Away Gols'] = teams_gols[-1]

    #Getting All Stats
    all_stats = driver.find_elements(By.CLASS_NAME, 'stat__category')
    
    #Get Values for each stat (home and away)
    for stat in all_stats:
        stat_name = stat.find_element(By.CLASS_NAME, 'stat__categoryName')
        home_stat = stat.find_element(By.CLASS_NAME, 'stat__homeValue')
        away_stat = stat.find_element(By.CLASS_NAME, 'stat__awayValue')

        match_stats[f'Home {stat_name.text}'] = home_stat.text
        match_stats[f'Away {stat_name.text}'] = away_stat.text

    match_stats.update(get_odds())
    
    driver.quit()
    
    return match_stats

def get_all_season_matchs(ids, season, columns):
    df_matchs = pd.DataFrame([], columns=columns)
    qtd_matchs = len(ids)

    for i, match_id in enumerate(matchs_ids):
        print(f'Match {i + 1}/{qtd_matchs}')

        match_stats = get_match_stats(match_id)
        df_match_stats = pd.DataFrame([match_stats], columns=columns)

        df_matchs = pd.concat([df_matchs, df_match_stats], ignore_index=True)
        sleep(random.randint(1, 4))
        
    df_matchs['Season'] = season

    return df_matchs
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for scrapper specific league')
    parser.add_argument('-c', '--country', type=str, required=True, help='League country. Remember to get the exact name on the flashscore url')
    parser.add_argument('-l', '--league', type=str, required=True, help='League name. Remember to get the exact name on the flashscore url')
    parser.add_argument('-s', '--season', type=str, required=True, help='Season that will be scrapper')
    parser.add_argument('-d', '--data_path', type=str, default='./data', help='Path to save the results')

    args = parser.parse_args()
    
    columns = [
        'Season',
        'Round',
        'Date',
        'Home',
        'Away',
        'Score',
        'Home Gols',
        'Away Gols',
        'Home Ball Possession',
        'Away Ball Possession',
        'Home Goal Attempts',
        'Away Goal Attempts',
        'Home Shots on Goal',
        'Away Shots on Goal',
        'Home Shots off Goal',
        'Away Shots off Goal',
        'Home Blocked Shots',
        'Away Blocked Shots',
        'Home Free Kicks',
        'Away Free Kicks', 
        'Home Corner Kicks',
        'Away Corner Kicks', 
        'Home Offsides',
        'Away Offsides', 
        'Home Throw-in',
        'Away Throw-in',
        'Home Goalkeeper Saves',
        'Away Goalkeeper Saves', 
        'Home Fouls',
        'Away Fouls', 
        'Home Red Cards',
        'Away Red Cards', 
        'Home Yellow Cards',
        'Away Yellow Cards',
        'Home Total Passes',
        'Away Total Passes',
        'Home Completed Passes',
        'Away Completed Passes',
        'Home Tackles',
        'Away Tackles',
        'Home Attacks',
        'Away Attacks',
        'Home Dangerous Attacks',
        'Away Dangerous Attacks',
        'Home odd',
        'Draw odd',
        'Away odd',
        'Over 2.5',
        'Under 2.5'
    ]
    
    try:
        driver = get_new_driver()

        print(f'{args.country} -> {args.league}-{args.season}')
        driver.get(f"https://www.flashscore.com/football/{args.country}/{args.league}-{args.season}/results/")
        
        accept_cookies(driver)
        
        sleep(3)

        open_all_matchs(driver)
        matchs_elements = get_all_id_matchs(driver)
        matchs_ids = [x.get_attribute('id').split('_')[-1] for x in matchs_elements]
        
        df_season = get_all_season_matchs(ids=matchs_ids, season=args.season, columns=columns)
        driver.quit()

        print('Saving Data (csv)...')
        df_season.to_csv(f'{args.data_path}/{args.country}-{args.league}-{args.season}.csv', index=False)
        print('Saving Data (parquet)...')
        df_season.to_parquet(f'{args.data_path}/{args.country}-{args.league}-{args.season}.parquet', index=False)
        
    except OSError as error:
        print('Inappropriate path file')

    except Exception as error:
        print('Error while scrapping...')
        print(error)
        driver.quit()
    
    finally:
        print('Scrapping End!')

    