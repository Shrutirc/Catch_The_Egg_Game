import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Eggs")

# Font setup
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 48)

# Load and scale images
nest_img = pygame.image.load("nest.png")
nest_img = pygame.transform.scale(nest_img, (80, 50))

egg_img = pygame.image.load("egg.png")
egg_img = pygame.transform.scale(egg_img, (30, 40))

# Level configuration
level_config = {
    "Beginner": {"egg_speed": 3, "egg_count": 1, "nest_speed": 7},
    "Intermediate": {"egg_speed": 5, "egg_count": 2, "nest_speed": 9},
    "Expert": {"egg_speed": 7, "egg_count": 3, "nest_speed": 11}
}

# --- Level Selection ---
def select_level():
    levels = list(level_config.keys())
    selected_index = 0
    selecting = True

    while selecting:
        screen.fill((255, 255, 255))
        title = big_font.render("Select Difficulty Level", True, (0, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, level in enumerate(levels):
            color = (255, 0, 0) if i == selected_index else (0, 0, 0)
            label = font.render(level, True, color)
            screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 150 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(levels)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    selecting = False
                    return levels[selected_index]

# --- Main Game ---
def run_game(level):
    config = level_config[level]
    egg_speed = config["egg_speed"]
    egg_count = config["egg_count"]
    nest_speed = config["nest_speed"]

    # Nest (player)
    player_width = 80
    player_height = 50
    player_x = WIDTH // 2
    player_y = HEIGHT - player_height - 10

    # Eggs
    eggs = []
    for _ in range(egg_count):
        eggs.append({
            "x": random.randint(0, WIDTH - 30),
            "y": random.randint(-150, -40)
        })

    # Score and lives
    score = 0
    lives = 3
    game_over = False
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= nest_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += nest_speed

            for egg in eggs:
                egg["y"] += egg_speed
                screen.blit(egg_img, (egg["x"], egg["y"]))

                # Collision
                if (
                    player_y < egg["y"] + 40 and
                    player_y + player_height > egg["y"] and
                    player_x < egg["x"] + 30 and
                    player_x + player_width > egg["x"]
                ):
                    score += 1
                    egg["y"] = random.randint(-150, -40)
                    egg["x"] = random.randint(0, WIDTH - 30)
                elif egg["y"] > HEIGHT:
                    lives -= 1
                    egg["y"] = random.randint(-150, -40)
                    egg["x"] = random.randint(0, WIDTH - 30)
                    if lives == 0:
                        game_over = True

            screen.blit(nest_img, (player_x, player_y))
            screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))
            screen.blit(font.render(f"Lives: {lives}", True, (0, 0, 0)), (10, 40))
        else:
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# ---- Run It All ----
level = select_level()
run_game(level)
