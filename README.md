# FlashScore Scrapper

This is a project whose objective is to collect data from the site [Flashscore.com.](https://flashscore.com/)

## Introduction

The program accesses the page of the chosen competition on the website and searches for the id of all matches. Thus, for each id a new web page is opened and the statistics collected, namely:

- Season
- Round
- Date
- Home
- Away
- Score
- Home Gols
- Away Gols
- Home Ball Possession
- Home Goal Attempts
- Away Goal Attempts
- Home Shots on Goal
- Away Shots on Goal
- Home Shots off Goal
- Away Shots off Goal
- Home Blocked Shots
- Away Blocked Shots
- Home Free Kicks
- Away Free Kicks
- Home Corner Kicks
- Away Corner Kicks
- Home Offsides
- Away Offsides
- Home Throw-in
- Away Throw-in
- Home Goalkeeper Saves
- Away Goalkeeper Saves
- Home Fouls
- Away Fouls
- Home Red Cards
- Away Red Cards
- Home Yellow Cards
- Away Yellow Cards
- Home Total Passes
- Away Total Passes
- Home Completed Passes
- Away Completed Passes
- Home Tackles
- Away Tackles
- Home Attacks
- Away Attacks
- Home Dangerous Attacks
- Away Dangerous Attacks
- Home odd
- Draw odd
- Away odd
- Over 2.5
- Under 2.5

**If the site does not offer one of these statistics, it will be left empty.**

## Running

1. Clone this repository.
2. Navigate to the src folder and create a “data” folder.
3. Run:

```python
pip install -r requirements.txt
```

1. Run:

```python
python scrapper_league.py -c <country> -l <league> -s <season>
```

Where the variables country, league and season must be removed from the website url, as in the following example:

In order to obtain statistics for Serie A of the Brazilian championship in the year 2022, we need to access the page with the following url: [https://www.flashscore.com/football/brazil/serie-a-2022](https://www.flashscore.com/football/brazil/serie-a-2022) and for that to happen we need to assign the following values for our variables

- country: brazil
- league: serie-a
- season: 2022

Obs: For some leagues season might be something like “2021/2022”, so just pass season as 2021-2022.

At the end of the execution, 2 files will be generated, a csv and a parquet, inside the data folder containing the statistics of each game of that edition of the league.

You can change the folder where the results will be saved by passing the -d flag and the path.