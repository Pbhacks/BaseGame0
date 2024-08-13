import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load assets
background_img = pygame.image.load("background.png")
back_scale = pygame.image.load("bgm.jpg")
spaceship_img = pygame.image.load("spaceship.png")
bullet_img = pygame.image.load("bullet.png")
asteroid_img = pygame.image.load("asteroid.png")

# Resize images if needed
spaceship_img = pygame.transform.scale(spaceship_img, (64, 64))
bullet_img = pygame.transform.scale(bullet_img, (31, 39))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

# Load and play background music
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)  # Loop indefinitely

# Load sound effects
# shoot_sound = pygame.mixer.Sound("shoot.wav")  # Uncomment and replace with actual sound file path

# Player settings
player_x = WIDTH // 2 - 32
player_y = HEIGHT - 64 - 10
player_speed = 5

# Bullet settings
bullets = []
bullet_speed = 7

# Asteroid settings
asteroid_speed = 5
asteroids = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Menu state
in_menu = True
paused = False

def draw_player(x, y):
    screen.blit(spaceship_img, (x, y))

def draw_bullet(x, y):
    screen.blit(bullet_img, (x, y))

def draw_asteroid(x, y):
    screen.blit(asteroid_img, (x, y))

def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))

def draw_menu():
    screen.blit(back_scale, (0, 0))
    draw_text("SPACE SHOOTER", 74, WHITE, WIDTH // 2, HEIGHT // 2 - 100)
    draw_text("Press ENTER to Start", 36, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("Press I for Instructions", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    draw_text("Press Q to Quit", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 100)

def draw_instructions():
    screen.blit(back_scale, (0, 0))
    draw_text("INSTRUCTIONS", 74, WHITE, WIDTH // 2, HEIGHT // 2 - 100)
    draw_text("Use ARROW keys to move", 36, WHITE, WIDTH // 2, HEIGHT // 2 - 30)
    draw_text("Press SPACE to shoot", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 30)
    draw_text("Press P to Pause", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 90)
    draw_text("Press ESC to return to Menu", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 150)
    draw_text("Press Q to Quit", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 210)

def game_over():
    screen.fill(BLACK)
    draw_text("GAME OVER", 74, RED, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Press ENTER to return to Menu", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.flip()

def main():
    global player_x, player_y, bullets, asteroids, score, paused, in_menu

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if in_menu:
                    if event.key == pygame.K_RETURN:  # Start game
                        in_menu = False
                        score = 0
                        bullets.clear()
                        asteroids.clear()
                    elif event.key == pygame.K_i:  # Instructions
                        show_instructions = True
                        while show_instructions:
                            draw_instructions()
                            pygame.display.flip()
                            for instruction_event in pygame.event.get():
                                if instruction_event.type == pygame.QUIT:
                                    running = False
                                    show_instructions = False
                                elif instruction_event.type == pygame.KEYDOWN:
                                    if instruction_event.key == pygame.K_ESCAPE:  # Return to menu
                                        show_instructions = False
                                    elif instruction_event.key == pygame.K_q:  # Quit
                                        running = False
                                        show_instructions = False
                    elif event.key == pygame.K_q:  # Quit from menu
                        running = False
                else:
                    if event.key == pygame.K_q:  # Quit from game
                        running = False
                    elif event.key == pygame.K_ESCAPE and not in_menu:  # Return to Menu
                        in_menu = True
                        paused = False

        if in_menu:
            draw_menu()
        else:
            screen.blit(background_img, (0, 0))
            if paused:
                draw_text("PAUSED", 74, WHITE, WIDTH // 2, HEIGHT // 2)
            else:
                # Game logic
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player_x > 0:
                    player_x -= player_speed
                if keys[pygame.K_RIGHT] and player_x < WIDTH - 64:
                    player_x += player_speed
                if keys[pygame.K_SPACE]:
                    bullets.append([player_x + 32 - 4, player_y])
                    # Uncomment if shoot_sound is available
                    # shoot_sound.play()

                if keys[pygame.K_p]:  # Pause/Resume the game
                    paused = not paused
                    pygame.time.delay(200)  # Short delay to prevent rapid toggling

                if not paused:
                    # Move and draw bullets
                    for bullet in bullets[:]:
                        bullet[1] -= bullet_speed
                        if bullet[1] < 0:
                            bullets.remove(bullet)
                        else:
                            draw_bullet(bullet[0], bullet[1])

                    # Create new asteroids
                    if random.randint(1, 20) == 1:
                        asteroid_x = random.randint(0, WIDTH - 50)
                        asteroid_y = -50
                        asteroids.append([asteroid_x, asteroid_y])

                    # Move and draw asteroids
                    for asteroid in asteroids[:]:
                        asteroid[1] += asteroid_speed
                        draw_asteroid(asteroid[0], asteroid[1])
                        if asteroid[1] > HEIGHT:
                            asteroids.remove(asteroid)
                            score += 1
                        if (player_x < asteroid[0] < player_x + 64 or player_x < asteroid[0] + 50 < player_x + 64) and (player_y < asteroid[1] < player_y + 64 or player_y < asteroid[1] + 50 < player_y + 64):
                            game_over()
                            pygame.time.wait(2000)
                            in_menu = True
                            paused = False

                    # Collision detection between bullets and asteroids
                    for bullet in bullets[:]:
                        for asteroid in asteroids[:]:
                            if (bullet[0] > asteroid[0] and bullet[0] < asteroid[0] + 50) and (bullet[1] > asteroid[1] and bullet[1] < asteroid[1] + 50):
                                try:
                                    bullets.remove(bullet)
                                    asteroids.remove(asteroid)
                                    score += 5
                                except ValueError:
                                    pass

                    draw_player(player_x, player_y)
                    display_score(score)

        pygame.display.flip()
        clock.tick(50)  # Reduce frame rate to 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
