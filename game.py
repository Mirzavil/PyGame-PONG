import pygame
import random
import time

# Screen setup: Define the dimensions of the game window
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# Color definitions: RGB values for black and white
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Speed settings for paddles and ball
PADDLE_SPEED = 400
BALL_SPEED = 400


def selection(screen, font):
    # Function to display the game menu and handle user selection
    screen.fill(COLOR_BLACK)

    title = font.render("PONG", True, COLOR_WHITE)
    single_player = font.render("1. Single Player", True, COLOR_WHITE)
    multiplayer = font.render("2. Two Players", True, COLOR_WHITE)

    # Positioning the menu items on the screen
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    single_rect = single_player.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    multi_rect = multiplayer.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

    # Rendering the menu items on the screen
    screen.blit(title, title_rect)
    screen.blit(single_player, single_rect)
    screen.blit(multiplayer, multi_rect)
    pygame.display.flip()

    return single_rect, multi_rect


def main():
    # Main function to initialize the game and run the game loop
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")

    # Font settings for displaying text
    font = pygame.font.SysFont("Consolas", 50)
    small_font = pygame.font.SysFont("Consolas", 30)

    single_rect, multi_rect = selection(screen, font)
    menu_active = True
    single_player = True

    while menu_active:
        # Event handling for menu selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if single_rect.collidepoint(mouse_pos):
                    single_player = True
                    menu_active = False
                elif multi_rect.collidepoint(mouse_pos):
                    single_player = False
                    menu_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    single_player = True
                    menu_active = False
                elif event.key == pygame.K_2:
                    single_player = False
                    menu_active = False

    # Paddles: Create rectangles for the paddles
    paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, 10, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 - 50, 10, 100)

    paddle_1_move = 0
    paddle_2_move = 0

    # Ball: Create a rectangle for the ball and set its initial speed
    ball_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 20, 20)
    ball_speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
    ball_speed_y = random.choice([-BALL_SPEED / 1.5, BALL_SPEED / 1.5])

    # Scores: Initialize player scores
    score_1 = 0
    score_2 = 0

    game_paused = False
    clock = pygame.time.Clock()

    def update_ai_paddle(paddle_rect, ball_rect, delta_time):
        # Function to control the AI paddle movement based on the ball's position
        if ball_rect.centery > paddle_rect.centery + 10:
            return PADDLE_SPEED
        elif ball_rect.centery < paddle_rect.centery - 10:
            return -PADDLE_SPEED
        return 0

    while True:
        delta_time = clock.tick(60) / 1000.0
        screen.fill(COLOR_BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                # Control paddle 1 with W/S keys
                if event.key == pygame.K_w:
                    paddle_1_move = -PADDLE_SPEED
                if event.key == pygame.K_s:
                    paddle_1_move = PADDLE_SPEED
                if not single_player:
                    # Control paddle 2 with UP/DOWN keys if in multiplayer mode
                    if event.key == pygame.K_UP:
                        paddle_2_move = -PADDLE_SPEED
                    if event.key == pygame.K_DOWN:
                        paddle_2_move = PADDLE_SPEED

                # Pause and resume game with SPACE key
                if event.key == pygame.K_SPACE and game_paused:
                    game_paused = False
                    ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    ball_speed_x = random.choice([-BALL_SPEED, BALL_SPEED])
                    ball_speed_y = random.choice([-BALL_SPEED / 1.5, BALL_SPEED / 1.5])

            if event.type == pygame.KEYUP:
                # Stop paddle movement when keys are released
                if event.key in (pygame.K_w, pygame.K_s):
                    paddle_1_move = 0
                if not single_player and event.key in (pygame.K_UP, pygame.K_DOWN):
                    paddle_2_move = 0

        if game_paused:
            # Display pause message when the game is paused
            pause_text = small_font.render("Press SPACE to continue", True, COLOR_WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(pause_text, pause_rect)
            pass
        else:
            # Update paddle positions based on movement
            paddle_1_rect.y += paddle_1_move * delta_time
            if single_player:
                paddle_2_move = update_ai_paddle(paddle_2_rect, ball_rect, delta_time)
                paddle_2_rect.y += paddle_2_move * delta_time
            else:
                paddle_2_rect.y += paddle_2_move * delta_time

            # Clamp paddles to stay within screen bounds
            paddle_1_rect.y = max(0, min(SCREEN_HEIGHT - paddle_1_rect.height, paddle_1_rect.y))
            paddle_2_rect.y = max(0, min(SCREEN_HEIGHT - paddle_2_rect.height, paddle_2_rect.y))

            # Move ball and handle collisions
            ball_rect.x += ball_speed_x * delta_time
            ball_rect.y += ball_speed_y * delta_time

            # Bounce ball off top and bottom edges
            if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
                ball_speed_y *= -1

            # Handle paddle collisions and increase ball speed slightly
            if ball_rect.colliderect(paddle_1_rect) and ball_speed_x < 0:
                ball_speed_x *= -1.05
                ball_speed_y += random.uniform(-50, 50)
            if ball_rect.colliderect(paddle_2_rect) and ball_speed_x > 0:
                ball_speed_x *= -1.05
                ball_speed_y += random.uniform(-50, 50)

            # Score logic: Check if the ball goes out of bounds and update scores
            if ball_rect.left <= 0:
                score_2 += 1
                game_paused = True
            elif ball_rect.right >= SCREEN_WIDTH:
                score_1 += 1
                game_paused = True

        # Draw paddles, ball, and score on the screen
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)
        pygame.draw.ellipse(screen, COLOR_WHITE, ball_rect)
        pygame.draw.aaline(screen, COLOR_WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        score_text = font.render(f"{score_1}   {score_2}", True, COLOR_WHITE)
        text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_text, text_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()