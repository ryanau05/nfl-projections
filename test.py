import pandas as pd
import numpy as np
import random
import time

url = 'https://www.pro-football-reference.com/players/B/BarkSa00.htm'

test_df = pd.read_html(url, header=1, attrs={'id': 'rushing_and_receiving'})[0]
season = test_df["Season"]
years = season[pd.to_numeric(season, errors='coerce').between(2000, 2030)].to_numpy()