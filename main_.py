# File Created By Chris DAmico

''' 
Sources
- https://www.youtube.com/watch?v=gRLHr664tXA
- https://github.com/techwithtim/Beautiful-Soup-Tutorial/blob/
- https://automatetheboringstuff.com/2e/chapter12/
- https://github.com/toddrob99/MLB-StatsAPI
- https://mlb.com
- https://basball-reference.com


Goals:
Create screen scraper that...
finds player stats (mlb),
averages them into career stats, 
has a interface through pg
'''

import pygame
import requests
from bs4 import BeautifulSoup


pygame.init()

# Set up the Pygame window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Baseball-Reference Scraper")

# Set up the Pygame font
font = pygame.font.Font(None, 24)

def scrape_player_stats(player_name):
    """Scrapes the player's career stats from Baseball-Reference."""

    # Format the player's name for the URL
    formatted_name = player_name.lower().replace(" ", "-")

    # Construct the URL for the player's page on Baseball-Reference
    base_url = "https://www.baseball-reference.com"
    player_url = f"{base_url}/players/{formatted_name[0]}/{formatted_name}.shtml"

    # Send a GET request to the player's URL
    response = requests.get(player_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table with career stats
    stats_table = soup.find("table", {"id": "batting_standard"})

    if stats_table is None:
        print(f"No career stats found for '{player_name}'")
        return None

    # Extract the header row and data rows from the table
    header_row = stats_table.find("thead").find("tr")
    data_rows = stats_table.find("tbody").find_all("tr")

    # Extract the column names from the header row
    column_names = [th.get_text() for th in header_row.find_all("th")]

    # Extract the stats for each season from the data rows
    stats = []
    for row in data_rows:
        season_stats = {}
        cells = row.find_all("td")
        for i, cell in enumerate(cells):
            column_name = column_names[i]
            season_stats[column_name] = cell.get_text()
        stats.append(season_stats)

    return stats

# Set up the Pygame input
input_text = ""
input_rect = pygame.Rect(300, 250, 200, 30)
input_active = False

# Pygame loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Scrape and display career stats for the player
                player_stats = scrape_player_stats(input_text)
                input_text = ""
                input_active = False

            elif event.key == pygame.K_BACKSPACE:
                # Remove the last character from the input text
                input_text = input_text[:-1]
            else:
                # Add the pressed character to the input text
                input_text += event.unicode

    # Clear the screen
    screen.fill((255, 255, 255))

    # Render the input box
    pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)
    input_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))
    
    if player_stats:
        # Render the player's career stats
        y = 300
        for season in player_stats:
            season_text = ""
            for key, value in season.items():
                season_text += f"{key}: {value} "
            season_surface = font.render(season_text, True, (0, 0, 0))
            screen.blit(season_surface, (100, y))
            y += 30
    player_stats()
    pygame.display.update()
