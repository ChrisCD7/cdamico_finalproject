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
import bs4
import requests
from settings import *
from bs4 import BeautifulSoup



# Initialize pygame and set up the window
pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("MLB Player Stats")

# Set up the font and colors for text
font = pg.font.SysFont(None, 30)
text_color = pg.Color("black")

# Ask for player's name input
player_name = input("Enter an MLB player's name: ")

# Create the URL to search for the player's stats
url = "https://www.baseball-reference.com/search/search.fcgi?search=" + player_name.replace(" ", "+")

# Make the request and parse the response HTML
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the link to the player's page
player_link = soup.find("ul", {"class": "searchlist"}).find("strong").find("a").get("href")

# Create the URL for the player's stats page
player_url = "https://www.baseball-reference.com" + player_link

# Make the request for the player's stats and parse the response HTML
player_response = requests.get(player_url)
player_soup = BeautifulSoup(player_response.content, "html.parser")

# Find the player's stats table and print the table headers
stats_table = player_soup.find("table", {"id": "batting_standard"})
headers = stats_table.find_all("th")
for header in headers:
    print(header.text, end="\t")

print()

# Find the player's stats rows and print the statistics
stats_rows = stats_table.find("tbody").find_all("tr")
for row in stats_rows:
    cells = row.find_all("td")
    for cell in cells:
        print(cell.text, end="\t")
    print()



