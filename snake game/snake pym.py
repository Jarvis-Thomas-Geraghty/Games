import pygame
import random
import sys

def load_highscore(filename="highscore.txt"):
    try:
        with open(filename, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(score, filename="highscore.txt"):
    with open(filename, "w") as f:
        f.write(str(score))



# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1450, 900
cell_size = 50
cols = width // cell_size
rows = height // cell_size

# Colors
black = (125, 75, 0)

# Set up screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("W O R M")
clock = pygame.time.Clock()

# Load and scale images
snake_img = pygame.image.load("worm 2.png")
snake_img = pygame.transform.scale(snake_img, (cell_size, cell_size))

background_img = pygame.image.load("dirt.png")
background_img = pygame.transform.scale(background_img, (width, height))

food_img = pygame.image.load("appel.png")
food_img = pygame.transform.scale(food_img, (cell_size, cell_size))

# Load music and sound
pygame.mixer.init()
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound("crunch.wav")
death_sound = pygame.mixer.Sound("explosion.wav")

start_sound = pygame.mixer.Sound("321.mp3")


def countdown():
    font = pygame.font.SysFont(None, 72)
    for i in range(3, 0, -1):
        screen.blit(background_img, (0, 0))  # Optional: show background
        text = font.render(f"Starting in {i}...", True, (255, 255, 255))
        rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        
        
def score():
    font = pygame.font.SysFont(None, 72)
    for i in range(3, 0, -1):
        screen.blit(background_img, (0, 0))  # Optional: show background
        text = font.render(f"Score:  {i}...", True, (255, 255, 255))
        rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        
        
        
# Draw sprite function
def draw_sprite(image, position):
    rect = pygame.Rect(position[0]*cell_size, position[1]*cell_size, cell_size, cell_size)
    screen.blit(image, rect)
def draw_score(score):
    font = pygame.font.SysFont(None, 48)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (20, 20))



# Game Over screen with buttons
def game_over(score):
    death_sound.play()

    highscore = load_highscore()
    if score > highscore:
        save_highscore(score)
        highscore = score  

    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 48)

    game_over_text = font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 120))

    # Display current and high score
    score_text = small_font.render(f"Score: {score}", True, (255, 255, 255))
    highscore_text = small_font.render(f"High Score: {highscore}", True, (255, 255, 0))

    # [rest of your button and event loop code]
    
 



    # Buttons
    button_width, button_height = 200, 60
    play_again_rect = pygame.Rect((width // 2 - button_width - 20, height // 2 + 50), (button_width, button_height))
    quit_rect = pygame.Rect((width // 2 + 20, height // 2 + 50), (button_width, button_height))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_rect)
        score_text = small_font.render(f"Final Score: {score}", True, (255, 255, 255))
        highscore_text = small_font.render(f"High score: {highscore} ", True, (0, 200, 0))
        highscore_rect = highscore_text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(highscore_text, highscore_rect)                             
        score_rect = score_text.get_rect(center=(width // 2, height // 2))
        screen.blit(score_text, score_rect)

        # Draw buttons
        pygame.draw.rect(screen, (0, 255, 0), play_again_rect)
        pygame.draw.rect(screen, (255, 0, 0), quit_rect)

        play_again_text = small_font.render('Play Again', True, (0, 0, 0))
        quit_text = small_font.render('Quit', True, (0, 0, 0))

        screen.blit(play_again_text, play_again_text.get_rect(center=play_again_rect.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_again_rect.collidepoint(event.pos):
                    main()  # Restart the game
                    return
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Main game loop
def main():
    global snake, snake_dir, food

    # Reset game state
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

        # Move snake
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        if (new_head[0] < 0 or new_head[0] >= cols or
            new_head[1] < 0 or new_head[1] >= rows or
            new_head in snake):
            game_over(score)

            return  # Exit this game instance

        snake.insert(0, new_head)

        # Check food collision
        if new_head == food:
            food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            eat_sound.play()
            score = score + 1
        else:
            snake.pop()

        # Draw background and game objects
        screen.blit(background_img, (0, 0))
        draw_sprite(food_img, food)
        for segment in snake:
            draw_sprite(snake_img, segment)
        draw_score(score)
        pygame.display.flip()
        clock.tick(10)

# Start the game
main()
