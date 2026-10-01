import pygame
import sys
import random

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
CELL_SIZE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Game 🐍")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 64)

MARGIN = 100
GRID_WIDTH = (WIDTH - 2*MARGIN) // CELL_SIZE * CELL_SIZE
GRID_HEIGHT = (HEIGHT - 2*MARGIN) // CELL_SIZE * CELL_SIZE
game_rect = pygame.Rect(MARGIN, MARGIN, GRID_WIDTH, GRID_HEIGHT)

start_x = game_rect.left + GRID_WIDTH // 2 // CELL_SIZE * CELL_SIZE
start_y = game_rect.top + GRID_HEIGHT // 2 // CELL_SIZE * CELL_SIZE
snake = [(start_x, start_y)]
direction = 'RIGHT'

foods = []
food_count = 1
score = 0
high_score = 0

button_size = 85
button_gap = 25
center_x = WIDTH // 2
bottom_y = HEIGHT - button_size * 2 - 240

buttons = {
    'UP': pygame.Rect(center_x - button_size // 2, bottom_y - button_size - button_gap, button_size, button_size),
    'DOWN': pygame.Rect(center_x - button_size // 2, bottom_y + button_size + button_gap, button_size, button_size),
    'LEFT': pygame.Rect(center_x - button_size - button_gap, bottom_y, button_size, button_size),
    'RIGHT': pygame.Rect(center_x + button_gap, bottom_y, button_size, button_size),
}

def spawn_foods(count):
    new_foods = []
    for _ in range(count):
        while True:
            x = random.randint(game_rect.left // CELL_SIZE, (game_rect.right - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(game_rect.top // CELL_SIZE, (game_rect.bottom - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            pos = (x, y)
            if pos not in snake and pos not in new_foods:
                new_foods.append(pos)
                break
    return new_foods

def move_snake(snake, direction, grow=False):
    x, y = snake[0]
    if direction == 'UP':
        new_head = (x, y - CELL_SIZE)
    elif direction == 'DOWN':
        new_head = (x, y + CELL_SIZE)
    elif direction == 'LEFT':
        new_head = (x - CELL_SIZE, y)
    elif direction == 'RIGHT':
        new_head = (x + CELL_SIZE, y)

    new_head = (new_head[0] // CELL_SIZE * CELL_SIZE, new_head[1] // CELL_SIZE * CELL_SIZE)
    snake.insert(0, new_head)

    if not grow:
        snake.pop()

    return snake

def check_collision(snake):
    head = snake[0]
    if not game_rect.collidepoint(head):
        return True
    if head in snake[1:]:
        return True
    return False

def draw_background():
    for x in range(game_rect.left, game_rect.right, CELL_SIZE):
        for y in range(game_rect.top, game_rect.bottom, CELL_SIZE):
            color = GREEN if (x//CELL_SIZE + y//CELL_SIZE) % 2 == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

def draw_buttons():
    for dir, rect in buttons.items():
        pygame.draw.rect(screen, GRAY, rect)
        label = font.render(dir[0], True, WHITE)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

def show_score():
    score_text = font.render(f"Score: {score}   High Score: {high_score}", True, WHITE)
    rect = score_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(score_text, rect)

def show_game_over():
    global high_score, food_count
    if score > high_score:
        high_score = score
    text = font.render(".Game Over.", True, RED)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    food_count = 1

def show_start_screen():
    screen.fill(GRAY)
    
    title_text = font.render("Created by Sina banihashem", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)

    start_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 100)
    pygame.draw.rect(screen, DARK_GREEN, start_button)
    
    start_text = font.render("Start", True, WHITE)
    start_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_rect)

    pygame.display.flip()
    return start_button

# نمایش صفحه‌ی شروع
game_started = False
start_button = show_start_screen()
while not game_started:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                game_started = True

# شروع بازی
foods = spawn_foods(food_count)
running = True
while running:
    screen.fill(BLACK)
    draw_background()
    show_score()
    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for dir, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    if dir == 'UP' and direction != 'DOWN':
                        direction = 'UP'
                    elif dir == 'DOWN' and direction != 'UP':
                        direction = 'DOWN'
                    elif dir == 'LEFT' and direction != 'RIGHT':
                        direction = 'LEFT'
                    elif dir == 'RIGHT' and direction != 'LEFT':
                        direction = 'RIGHT'

    grow = False
    head = snake[0]
    if head in foods:
        foods.remove(head)
        score += 1
        food_count += 1
        grow = True
        foods += spawn_foods(food_count)

    snake = move_snake(snake, direction, grow)

    if check_collision(snake):
        show_game_over()
        snake = [(start_x, start_y)]
        direction = 'RIGHT'
        foods = spawn_foods(food_count)
        score = 0

    for segment in snake:
        pygame.draw.rect(screen, WHITE, (*segment, CELL_SIZE, CELL_SIZE))

    for food in foods:
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
sys.exit()