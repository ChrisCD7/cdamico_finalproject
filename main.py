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
import bs4

from settings import *
# from https://automatetheboringstuff.com/2e/chapter12/
from bs4 import BeautifulSoup


URL = 'https://www.baseball-reference.com'

# get info from website
res = requests.get(URL)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
# print(type(soup))
# print(soup)
elem = soup.select('div')
# print(len(elem))
print(str(elem))
# dump into excel

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table", {"id": "team_pitching"})
player_name = table.find("tbody").find("tr").find("td", {"data-stat": "player"}).find("a").text
print(player_name)
