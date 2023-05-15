import pygame
from pybaseball import playerid_lookup, player_stats

pygame.init()

# Set up the Pygame window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("MLB.com Scraper")

# Set up the Pygame font
font = pygame.font.Font(None, 28)

def get_player_career_stats(player_name):
    """Retrieves the career stats for the given player using pybaseball."""

    # Search for the player by name
    player_lookup = playerid_lookup(player_name)
    if player_lookup.empty:
        print(f"No results found for '{player_name}'")
        return None
    player_id = player_lookup.iloc[0]['key_mlbam']

    # Get the player's career stats
    stats = player_stats(player_id)
    if stats is None:
        print(f"No stats found for '{player_name}'")
        return None

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
                # Retrieve and display career stats for the player
                stats = get_player_career_stats(player_name)
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
