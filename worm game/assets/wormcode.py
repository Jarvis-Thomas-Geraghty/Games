import random
import sys
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1600, 800

# Set up screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("W O R M")
clock = pygame.time.Clock()

# Load and store unscaled images
snake_img_orig = pygame.image.load("wormbody.png")
background_img = pygame.image.load("dirt.png")
food_img_orig = pygame.image.load("appel.png")

# Scale background
background_img = pygame.transform.scale(background_img, (width, height))

# Load music and sound
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound("crunch.wav")
death_sound = pygame.mixer.Sound("explosion.wav")
start_sound = pygame.mixer.Sound("321.mp3")

# High score functions
def load_highscore(filename="snakehigh1.txt"):
    try:
        with open(filename, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(score, filename="snakehigh1.txt"):
    with open(filename, "w") as f:
        f.write(str(score))

# Game modes
modes = {
     "Very Easy": {"cell_size": 100, "tick": 1},
    "Easy": {"cell_size": 80, "tick": 4},
    "Medium": {"cell_size": 50, "tick": 7},
    "Hard": {"cell_size": 40, "tick": 10}
}

def select_mode():
    font = pygame.font.SysFont(None, 60)
    mode_buttons = []
    spacing = 100
    start_y = height // 2 - (len(modes) * spacing) // 2

    for i, mode in enumerate(modes):
        rect = pygame.Rect(width // 2 - 150, start_y + i * spacing, 300, 60)
        mode_buttons.append((mode, rect))

    while True:
        screen.blit(background_img, (0, 0))
        title = font.render("Choose a Game Mode", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(width // 2, 100)))

        for mode, rect in mode_buttons:
            pygame.draw.rect(screen, (0, 100, 200), rect)
            text = font.render(mode, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for mode, rect in mode_buttons:
                    if rect.collidepoint(event.pos):
                        return modes[mode]

def countdown():
    font = pygame.font.SysFont(None, 72)
    for i in range(3, 0, -1):
        screen.blit(background_img, (0, 0))
        text = font.render(f"Starting in {i}...", True, (255, 255, 255))
        rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(1000)

def draw_sprite(image, position, cell_size):
    rect = pygame.Rect(position[0]*cell_size, position[1]*cell_size, cell_size, cell_size)
    screen.blit(image, rect)

def draw_score(score):
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (20, 20))

def game_over(score):
    death_sound.play()

    # Only load once
    highscore = load_highscore()
    if score > highscore:
        save_highscore(score)
        highscore = score

    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 48)

    game_over_text = font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 120))

    final_score_text = small_font.render(f"Final Score: {score}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(width // 2, height // 2))

    highscore_text = small_font.render(f"High Score: {highscore}", True, (0, 200, 0))
    highscore_rect = highscore_text.get_rect(center=(width // 2, height // 2 - 50))

    button_width, button_height = 200, 60
    play_again_rect = pygame.Rect(width // 2 - button_width - 20, height // 2 + 50, button_width, button_height)
    quit_rect = pygame.Rect(width // 2 + 20, height // 2 + 50, button_width, button_height)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(highscore_text, highscore_rect)
        screen.blit(final_score_text, final_score_rect)

        pygame.draw.rect(screen, (0, 255, 0), play_again_rect)
        pygame.draw.rect(screen, (255, 0, 0), quit_rect)

        play_again_label = small_font.render('Play Again', True, (0, 0, 0))
        quit_label = small_font.render('Quit', True, (0, 0, 0))

        screen.blit(play_again_label, play_again_label.get_rect(center=play_again_rect.center))
        screen.blit(quit_label, quit_label.get_rect(center=quit_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_rect.collidepoint(event.pos):
                    main()
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def main():
    global cell_size

    settings = select_mode()
    cell_size = settings["cell_size"]
    tick_speed = settings["tick"]

    cols = width // cell_size
    rows = height // cell_size

    # Rescale sprites based on selected mode
    snake_img = pygame.transform.scale(snake_img_orig, (cell_size, cell_size))
    food_img = pygame.transform.scale(food_img_orig, (cell_size, cell_size))

    score = 0
    snake = [(cols // 2, rows // 2)]
    snake_dir = (0, -1)
    food = (random.randint(0, cols - 1), random.randint(0, rows - 1))

    start_sound.play()
    countdown()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, 1):
                    snake_dir = (0, -1)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -1):
                    snake_dir = (0, 1)
                elif event.key == pygame.K_LEFT and snake_dir != (1, 0):
                    snake_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-1, 0):
                    snake_dir = (1, 0)

        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        if (new_head[0] < 0 or new_head[0] >= cols or
            new_head[1] < 0 or new_head[1] >= rows or
            new_head in snake):
            game_over(score)
            return

        snake.insert(0, new_head)
        if new_head == food:
            food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            eat_sound.play()
            score += 1
        else:
            snake.pop()

        screen.blit(background_img, (0, 0))
        draw_sprite(food_img, food, cell_size)
        for segment in snake:
            draw_sprite(snake_img, segment, cell_size)
        draw_score(score)
        pygame.display.flip()
        clock.tick(tick_speed)

main()