import pygame
import random

# Set up the game window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wandering on the Street")

# Load the background image
background_image = pygame.image.load("background.png")  # Replace "background.png" with the path to your background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize the font module

# Set up the player
cat_image = pygame.image.load("cat.png")  # Replace "cat.png" with the path to your player image
cat_width = 200  # Desired width of the player image
cat_height = 180  # Desired height of the player image
cat_image = pygame.transform.scale(cat_image, (cat_width, cat_height))
cat_rect = cat_image.get_rect()
cat_rect.centerx = WIDTH // 2 - 300
cat_rect.centery = HEIGHT // 2 + 200

# Set up the hearts
heart_images = [
    pygame.image.load("fullheart.png"),  # Replace "fullheart.png" with the path to your heart image that increases HP
    pygame.image.load("halfheart.png"),  # Replace "halfheart.png" with the path to your heart image that decreases HP
]
heart_width = 80  # Desired width of the heart image
heart_height = 80  # Desired height of the heart image
heart_images = [
    pygame.transform.scale(image, (heart_width, heart_height))
    for image in heart_images
]
hearts = []

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game variables
hp = 100
score = 0

# Set up the heart speed
heart_speed = 5

# Set up the heart spawn variables
spawn_timer = 0
spawn_interval = 500  # Spawn a new heart every 500 milliseconds

# Function to spawn a new heart
def spawn_heart():
    num_hearts = random.randint(1, 3)  # Random number of hearts between 1 and 3
    spawned_hearts = []
    for _ in range(num_hearts):
        heart_image = random.choice(heart_images)
        heart_rect = heart_image.get_rect()
        heart_rect.centerx = WIDTH
        heart_rect.centery = random.randint(30, HEIGHT - 30)
        spawned_hearts.append({"image": heart_image, "rect": heart_rect})
    return spawned_hearts

# Function to handle collisions
def handle_collisions():
    global hp, score
    for heart in hearts:
        if cat_rect.colliderect(heart["rect"]):
            if heart["image"] == heart_images[1]:  # Empty heart decreases HP
                hp -= 10
            elif heart["image"] == heart_images[0] and hp < 100:  # Full heart increases HP up to 100
                hp += 10
            hearts.remove(heart)
            break

# Font for title text
title_font = pygame.font.SysFont(None, 80)

# Font for game over text
game_over_font = pygame.font.SysFont(None, 80)

# Font for buttons
button_font = pygame.font.SysFont(None, 32)

# Load the button click sound effect
button_sound = pygame.mixer.Sound("Blop Sound.mp3")  # Replace "Blop Sound.mp3" with the path to your sound effect file

# Create the "Start" button
start_text = button_font.render("Start", True, (0, 0, 0))
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# Create the "Restart" button
restart_text = button_font.render("Restart", True, (0, 0, 0))
restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# Create the "Quit" button
quit_text = button_font.render("Quit", True, (0, 0, 0))
quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

# Game states
START_SCREEN = 0
GAME_SCREEN = 1
GAME_OVER_SCREEN = 2
current_screen = START_SCREEN

# Initialize the mixer module
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load("Rinne - Letter.mp3")  # Replace "Rinne - Letter.mp3" with the path to your music file
pygame.mixer.music.play(-1)  # Play the background music in a loop

# Adjust the volume of the background music
pygame.mixer.music.set_volume(0.5)  # Adjust the volume level as needed


# Game loop
running = True
is_jumping = False
jump_count = 10
spawn_timer = 0
spawn_interval = 500  # Spawn a new heart every 500 milliseconds
game_over = False
game_started = False
start_time = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == START_SCREEN and start_rect.collidepoint(event.pos):
                current_screen = GAME_SCREEN
                game_started = True
                button_sound.play()  # Play the button click sound effect
            elif current_screen == GAME_OVER_SCREEN:
                if restart_rect.collidepoint(event.pos):
                    current_screen = GAME_SCREEN
                    game_started = True
                    button_sound.play()  # Play the button click sound effect
                elif quit_rect.collidepoint(event.pos):
                    running = False
                    button_sound.play()  # Play the button click sound effect
        elif event.type == pygame.KEYDOWN:
            if current_screen == GAME_SCREEN and event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True

    if current_screen == START_SCREEN:
    # Draw the start screen
        win.blit(background_image, (0, 0))
        win.blit(start_text, start_rect)

    # Draw the title text
        title_text = title_font.render("Wandering on the Street", True, (0, 0, 0))
        title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT//2))
        win.blit(title_text, title_text_rect)

        pygame.display.flip()  # Update the game display

    
    elif current_screen == GAME_SCREEN:
        if game_started:
            # Initialize game variables
            hp = 100
            score = 0
            hearts = []
            spawn_timer = 0
            game_over = False
            game_started = False
            start_time = pygame.time.get_ticks()

        # Update the player
        if is_jumping:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                cat_rect.y -= (jump_count ** 2) * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Spawn new hearts
        spawn_timer += clock.get_rawtime()
        if spawn_timer >= spawn_interval:
            hearts.extend(spawn_heart())
            spawn_timer = 0

        # Update the hearts
        for heart in hearts:
            heart["rect"].x -= heart_speed
            if heart["rect"].right < 0:
                hearts.remove(heart)

        # Draw the background
        win.blit(background_image, (0, 0))

        # Draw the player
        win.blit(cat_image, cat_rect)

        # Draw the hearts
        for heart in hearts:
            win.blit(heart["image"], heart["rect"])

        # Draw the HP and score
        hp_text = pygame.font.SysFont(None, 24).render(f"HP: {int(hp)}", True, (0, 0, 0))
        score_text = pygame.font.SysFont(None, 24).render(f"Score: {score}", True, (0, 0, 0))
        win.blit(hp_text, (10, 10))
        win.blit(score_text, (10, 40))

        # Handle collisions
        handle_collisions()

        # Check if HP reaches 0
        if hp <= 0:
            game_over = True
            current_screen = GAME_OVER_SCREEN

        pygame.display.flip()  # Update the game display

    elif current_screen == GAME_OVER_SCREEN:
        # Display game over text
        game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 ))
        win.blit(game_over_text, game_over_text_rect)

        # Draw the restart and quit buttons
        win.blit(restart_text, restart_rect)
        win.blit(quit_text, quit_rect)

        pygame.display.flip()  # Update the game display

    clock.tick(60)

    if current_screen == GAME_SCREEN and game_started:
        # Calculate elapsed time in seconds
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

     # Update the hp (decrease by 0.5 every second) if the game is not over
    if not game_over:
        hp -= 0.1

        # Limit the HP within the range of 0 to 100
        hp = max(0, min(hp, 100))

        # Update the score (increase by 1 every second)
        score += 1

# Quit the game
pygame.quit()
