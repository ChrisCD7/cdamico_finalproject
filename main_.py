# File Created By Chris DAmico

''' 
Sources
- Automate the Boring Stuff
- Chat GPT
- https://www.youtube.com/watch?v=gRLHr664tXA
- https://github.com/techwithtim/Beautiful-Soup-Tutorial/blob/
- https://automatetheboringstuff.com/2e/chapter12/

Goals:
Create screen scraper that...
finds player stats (mlb),
averages them into career stats, 
has a interface through pg
'''

import pygame
import requests
from bs4 import BeautifulSoup

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((800, 700))
font = pygame.font.Font(None, 50)

# Function to scrape player's career stats
def scrape_career_stats(player_name):
    # Format player name for the URL
    player_name = player_name.replace(" ", "_")
    url = f"https://www.baseball-reference.com/players/{player_name[0]}/{player_name.lower()[:5]}{player_name.lower()[5:]}01.shtml"

    # Send a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the table containing career stats
        table = soup.find("table", {"id": "batting_standard"})

        if table:
            # Extract the table rows
            rows = table.find_all("tr")

            # Extract the column headers
            headers = [th.text for th in rows[0].find_all("th")]

            # Extract the career stats
            career_stats = [td.text for td in rows[-1].find_all("td")]

            # Create a dictionary with the stats and headers
            stats_dict = dict(zip(headers, career_stats))

            return stats_dict

    return None

# Pygame loop
running = True
player_name = ""
stats = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Scrape career stats for the player
                stats = scrape_career_stats(player_name)
                player_name = ""  # Clear the player name input
            elif event.key == pygame.K_BACKSPACE:
                # Remove the last character from the player name input
                player_name = player_name[:-1]
            else:
                # Append the typed character to the player name input
                player_name += event.unicode

    # Display the player name input
    screen.fill((255, 255, 255))
    input_text = font.render("Player Name: " + player_name, True, (0, 0, 0))
    screen.blit(input_text, (20, 20))

    if stats:
        y = 60
        for key, value in stats.items():
            text = font.render(f"{key}: {value}", True, (0, 0, 0))
            screen.blit(text, (20, y))
            y += 20

    pygame.display.flip()

pygame.quit()
