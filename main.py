# File created by Chris D'Amico

'''
Goals:
Create screen scraper that...
finds player stats (mlb),
averages them into career stats, 
has a interface through pygame
'''


import webbrowser
import pygame as pg
import os
import requests

from settings import *
# from https://automatetheboringstuff.com/2e/chapter12/
from bs4 import BeautifulSoup


res = requests.get('https://www.baseball-reference.com')
type(res)
res.raise_for_status()
playFile = open('bsblref.txt', 'wb')
for chunk in res.iter_content(100000):
    playFile.write(chunk)
playFile.close()

class Requests('requests.models.Response'):
    res.status_code == requests.codes.ok
    True
    len(res.text)
    178981
    print(res.text[:250])

url = "https://www.baseball-reference.com/leagues/MLB/2021.shtml"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table", {"id": "team_pitching"})
player_name = table.find("tbody").find("tr").find("td", {"data-stat": "player"}).find("a").text
print(player_name)
