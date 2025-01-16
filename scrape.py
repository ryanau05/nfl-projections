from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

PLAYERS_DICT = {}

class Player:
    def __init__(self, name, position, team, age = 0):
        self.name = name
        self.position = position
        self.team = team
        self.age = age

def top_100_players():                                                                      # scrapes the name, position, and team of the top 100 players from the url
    global PLAYERS_DICT
    url = "https://www.sharpfootballanalysis.com/analysis/nfl-top-100-list/"

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    players_list = []
    for row in rows[1:]:
        cells = row.find_all('td')
        info = cells[1].text.strip()
        info = info.split(',')
        name = info[0]
        position = info[1]
        team = info[2]
        players_list.append(Player(name, position, team))
    players_dict = {player.name: player for player in players_list}

    return players_dict

def stats_grabber(name):                                                                    # takes in player name, returns url for their pfr profile
    last_name = name.split(' ')[1]
    last_initial = last_name[0]
    last_name_portion = last_name[0:4]
    first_name = name.split(' ')[0]
    first_name = first_name.replace('.','')
    first_name_portion = first_name[0:2]
    url = 'https://www.pro-football-reference.com/players/' + last_initial + '/' + last_name_portion + first_name_portion + '00.htm'
    # print(url)
    return url

def game_logs(name):                                                                     # takes in player prf profile, returns dict of urls for each year game logs from 2024-decreasing,
    url_log = {}                                                                         # and an array of years available

    p_url = stats_grabber(name)
    test_df = pd.read_html(p_url, header=1, attrs={'id': 'rushing_and_receiving'})[0]
    season = test_df["Season"]
    years = season[pd.to_numeric(season, errors='coerce').between(2000, 2030)].to_numpy()
    years = [int(x) for x in years]

    for year in years:
        url = p_url[:-4]
        url = url + '/gamelog/' + str(year) + '/'
        url_log[year] = url
        # print(url_log[year])
    return url_log

    

def main():
    top_100_players()
    # test = game_logs("Christian McCaffrey")
    # test = game_logs("Saquon Barkley")
    # for i in test:
        # print(test[i])

    print(stats_grabber("Christian McCaffrey"))

main()