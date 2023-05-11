import pygame
import requests
from bs4 import BeautifulSoup

pygame.init()

# Set up the Pygame window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Baseball Reference Scraper")

# Set up the Pygame font
font = pygame.font.Font(None, 28)

def scrape_career_stats(player_name):
    """Scrapes the career stats for the given player from Baseball Reference."""

    # Construct the URL for the player's page on Baseball Reference
    base_url = "https://www.baseball-reference.com"
    search_url = base_url + "/search/search.fcgi"
    search_params = {"search": player_name}
    response = requests.get(search_url, params=search_params)
    soup = BeautifulSoup(response.content, "html.parser")
    search_results = soup.find_all("div", {"class": "search-item-name"})
    if len(search_results) == 0:
        print(f"No results found for '{player_name}'")
        return None
    player_path = search_results[0].find("a")["href"]
    player_url = base_url + player_path

    # Scrape the player's career stats
    response = requests.get(player_url)
    soup = BeautifulSoup(response.content, "html.parser")
    stats_table = soup.find("table", {"id": "batting"})
    if stats_table is None:
        print(f"No stats found for '{player_name}'")
        return None
    stats = {}
    rows = stats_table.find_all("tr")
    for row in rows:
        cells = row.find_all(["th", "td"])
        if len(cells) > 1:
            key = cells[0].get_text()
            value = cells[-1].get_text()
            stats[key] = value

    return stats

# Set up the Pygame input
player_name = ""
player_name_surface = font.render(player_name, True, (0, 0, 0))
player_name_rect = player_name_surface.get_rect()
player_name_rect.x = 20
player_name_rect.y = 20

# Pygame loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Remove the last character from the player name
                player_name = player_name[:-1]
            elif event.key == pygame.K_RETURN:
                # Scrape and display career stats for the player
                stats = scrape_career_stats(player_name)
                if stats:
                    # Clear the player name input
                    player_name = ""

                    # Display the stats
                    screen.fill((255, 255, 255))
                    y = 20
                    for key, value in stats.items():
                        text = font.render(f"{key}: {value}", True, (0, 0, 0))
                        screen.blit(text, (20, y))
                        y += 20

                    pygame.display.flip()
            else:
                # Add the pressed character to the player name
                player_name += event.unicode
            player_name_surface = font.render(player_name, True, (0, 0, 0))

    # Clear the screen and draw the player name input
    screen.fill((255, 255, 255))
    screen.blit(player_name_surface, player_name_rect)

    pygame.display.update()
