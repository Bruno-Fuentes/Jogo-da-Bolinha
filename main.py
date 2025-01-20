import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clique na Bolinha")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Font for score and messages
default_font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Game variables
score = 0
time_remaining = 30  # Total game time in seconds
ball_radius = 20
ball_x = random.randint(ball_radius, WIDTH - ball_radius)
ball_y = random.randint(ball_radius, HEIGHT - ball_radius)
ball_visible_time = 2000  # Time in milliseconds
last_ball_time = pygame.time.get_ticks()

level = 1
max_levels = 3
level_completed = False

# Game states
game_running = True
game_active = False
level_transition = False
start_screen_active = True

# Game over message
def show_game_over():
    screen.fill(WHITE)
    game_over_text = large_font.render("Game Over!", True, BLACK)
    score_text = default_font.render(f"Final Score: {score}", True, BLACK)
    restart_text = default_font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

# Start screen
def show_start_screen():
    screen.fill(WHITE)
    title_text = large_font.render("Clique na Bolinha", True, BLACK)
    instructions_text = default_font.render("Press SPACE to Start", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

# Level transition screen
def show_level_transition():
    screen.fill(WHITE)
    level_text = large_font.render(f"Level {level}", True, BLACK)
    instructions_text = default_font.render("Press SPACE to Continue", True, BLACK)
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

while game_running:
    if start_screen_active:
        show_start_screen()

    elif level_transition:
        show_level_transition()

    elif not game_active and not start_screen_active:
        show_game_over()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if start_screen_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_screen_active = False
                game_active = True
                score = 0
                time_remaining = 30
                level = 1
                ball_visible_time = 2000
                last_ball_time = pygame.time.get_ticks()
                start_time = pygame.time.get_ticks()

        if level_transition and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                level_transition = False
                game_active = True
                last_ball_time = pygame.time.get_ticks()
                start_time = pygame.time.get_ticks()

        if not game_active and not start_screen_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                start_screen_active = True
            elif event.key == pygame.K_q:
                game_running = False

        if game_active and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            distance = ((mouse_x - ball_x) ** 2 + (mouse_y - ball_y) ** 2) ** 0.5
            if distance <= ball_radius:
                score += 1
                ball_x = random.randint(ball_radius, WIDTH - ball_radius)
                ball_y = random.randint(ball_radius, HEIGHT - ball_radius)
                last_ball_time = pygame.time.get_ticks()  # Reset ball timer on click

    if game_active:
        # Update ball visibility
        current_time = pygame.time.get_ticks()
        if current_time - last_ball_time > ball_visible_time:
            ball_x = random.randint(ball_radius, WIDTH - ball_radius)
            ball_y = random.randint(ball_radius, HEIGHT - ball_radius)
            last_ball_time = current_time

        # Update remaining time
        time_remaining = 30 - (current_time - start_time) // 1000
        if time_remaining <= 0:
            if level < max_levels:
                level += 1
                ball_visible_time = max(500, ball_visible_time - 500)  # Increase difficulty
                level_transition = True
                game_active = False
            else:
                game_active = False

        # Drawing everything
        screen.fill(WHITE)

        # Draw ball
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        # Draw score and time
        score_text = default_font.render(f"Score: {score}", True, BLACK)
        time_text = default_font.render(f"Time: {time_remaining}s", True, BLACK)
        level_text = default_font.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (WIDTH - 150, 10))
        screen.blit(level_text, (WIDTH // 2 - 50, 10))

        # Update the display
        pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
