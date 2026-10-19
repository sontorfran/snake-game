import random

import pygame

pygame.init()


def spawn_food(snake_body):
    food_x = random.randint(0, 29) * 20
    food_y = random.randint(0, 19) * 20
    while (food_x, food_y) in snake_body:
        food_x = random.randint(0, 29) * 20
        food_y = random.randint(0, 19) * 20
    return food_x, food_y


def reset_game():
    snake_x = 100
    snake_y = 100
    snake_length = 1
    score = 0
    direction_x = 1
    direction_y = 0
    game_over = False
    snake_body = []
    food_x, food_y = spawn_food(snake_body)
    return (
        snake_x,
        snake_y,
        snake_length,
        score,
        direction_x,
        direction_y,
        game_over,
        snake_body,
        food_x,
        food_y,
    )


screen = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont(None, 36)
(
    snake_x,
    snake_y,
    snake_length,
    score,
    direction_x,
    direction_y,
    game_over,
    snake_body,
    food_x,
    food_y,
) = reset_game()
clock = pygame.time.Clock()
running = True
game_over_font = pygame.font.SysFont(None, 60)
game_started = False
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, 20, 20))
    keys = pygame.key.get_pressed()
    if not game_started and keys[pygame.K_SPACE]:
        game_started = True
    if keys[pygame.K_RIGHT] and direction_x != -1:
        direction_x = 1
        direction_y = 0
    elif keys[pygame.K_LEFT] and direction_x != 1:
        direction_x = -1
        direction_y = 0
    elif keys[pygame.K_UP] and direction_y != 1:
        direction_x = 0
        direction_y = -1
    elif keys[pygame.K_DOWN] and direction_y != -1:
        direction_x = 0
        direction_y = 1
    if game_started and not game_over:
        snake_x += direction_x * 20
        snake_y += direction_y * 20
        snake_body.append((snake_x, snake_y))
        if len(snake_body) > snake_length:
            snake_body.pop(0)
            print(snake_body)
        if snake_x < 0 or snake_x > 580 or snake_y < 0 or snake_y > 380:
            game_over = True
        snake_head = (snake_x, snake_y)
        if snake_head in snake_body[:-1]:
            game_over = True
        if snake_x == food_x and snake_y == food_y:
            food_x, food_y = spawn_food(snake_body)
            print("Yummy!")
            snake_length += 1
            score += 1
            if score > high_score:
                high_score = score
                with open("highscore.txt", "w") as file:
                    file.write(str(high_score))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    for segment in snake_body:
        pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], 20, 20))
    high_score_text = font.render(f"High score: {high_score}", True, (255, 255, 255))
    screen.blit(high_score_text, (400, 10))
    if game_over:
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (170, 170))
        final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(final_score_text, (200, 230))
    if game_over and keys[pygame.K_r]:
        (
            snake_x,
            snake_y,
            snake_length,
            score,
            direction_x,
            direction_y,
            game_over,
            snake_body,
            food_x,
            food_y,
        ) = reset_game()
    if not game_started:
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(start_text, (170, 180))
    pygame.display.update()
    speed = 5 + score
    clock.tick(speed)
pygame.quit()
