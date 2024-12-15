import pygame
import random
import time

# Game configuration
GRID_SIZE = 10
CELL_SIZE = 50
OBSTACLE_COUNT = 15
USER_COLOR = (0, 0, 255)
AI_COLOR = (255, 0, 0)
GOAL_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (128, 128, 128)
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (200, 200, 200)
USER_TIME_LIMIT = 10
AI_TIME_LIMIT = 1

# Initialize pygame
pygame.init()

# Screen dimensions (These depend on GRID_SIZE and CELL_SIZE)
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Runner")

# Load images
MENU_BACKGROUND = pygame.image.load('menu_background.jpg')
MENU_BACKGROUND = pygame.transform.scale(MENU_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

USER_IMAGE = pygame.image.load('user_icon.png')
AI_IMAGE = pygame.image.load('ai_icon.png')
GOAL_IMAGE = pygame.image.load('goal_icon.png')

# Resize images to fit the grid cell
USER_IMAGE = pygame.transform.scale(USER_IMAGE, (CELL_SIZE, CELL_SIZE))
AI_IMAGE = pygame.transform.scale(AI_IMAGE, (CELL_SIZE, CELL_SIZE))
GOAL_IMAGE = pygame.transform.scale(GOAL_IMAGE, (CELL_SIZE, CELL_SIZE))

# Font
font = pygame.font.Font(None, 36)

def draw_grid(grid, user, ai, goal):
    screen.fill(BACKGROUND_COLOR)

    # Draw the grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, rect)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)

    # Draw goal
    goal_rect = pygame.Rect(goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(GOAL_IMAGE, goal_rect.topleft)  # Draw the goal image

    # Draw user
    user_rect = pygame.Rect(user[0] * CELL_SIZE, user[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(USER_IMAGE, user_rect.topleft)  # Draw the user image

    # Draw AI
    ai_rect = pygame.Rect(ai[0] * CELL_SIZE, ai[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(AI_IMAGE, ai_rect.topleft)  # Draw the AI image

def generate_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    # Add obstacles
    for _ in range(OBSTACLE_COUNT):
        while True:
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if grid[y][x] == 0:
                grid[y][x] = 1
                break

    return grid

def is_valid_move(position, grid):
    x, y = position
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[y][x] == 0

def get_ai_move(ai_pos, user_pos, grid):
    possible_moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    best_move = ai_pos
    min_distance = float('inf')

    for dx, dy in possible_moves:
        new_pos = (ai_pos[0] + dx, ai_pos[1] + dy)
        if is_valid_move(new_pos, grid):
            distance = abs(new_pos[0] - user_pos[0]) + abs(new_pos[1] - user_pos[1])
            if distance < min_distance:
                min_distance = distance
                best_move = new_pos

    return best_move

def main_menu():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Draw the menu background
        screen.blit(MENU_BACKGROUND, (0, 0))  # Position the background at (0, 0)

        # Render menu text
        title_text = font.render("Maze Runner", True, (255, 255, 255))
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        exit_text = font.render("Press ESC to Exit", True, (255, 255, 255))

        # Display the title and buttons
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT * 3 // 4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False  # Start the game when SPACE is pressed
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def draw_countdown(time_remaining):
    countdown_text = font.render(f"Time: {time_remaining}s", True, (255, 255, 255))
    screen.blit(countdown_text, (10, 10))

def user_turn(user, grid, ai, goal):
    start_time = time.time()
    while time.time() - start_time < USER_TIME_LIMIT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_pos = (user[0], user[1] - 1)
            if is_valid_move(new_pos, grid):
                return new_pos
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_pos = (user[0], user[1] + 1)
            if is_valid_move(new_pos, grid):
                return new_pos
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_pos = (user[0] - 1, user[1])
            if is_valid_move(new_pos, grid):
                return new_pos
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_pos = (user[0] + 1, user[1])
            if is_valid_move(new_pos, grid):
                return new_pos

        time_remaining = USER_TIME_LIMIT - int(time.time() - start_time)
        draw_grid(grid, user, ai, goal)
        draw_countdown(time_remaining)
        pygame.display.flip()
    return user  # No move made within time limit

def ai_turn(ai, user, grid):
    time.sleep(AI_TIME_LIMIT)
    return get_ai_move(ai, user, grid)

def main():
    # Main game variables
    grid = generate_grid()

    while True:
        goal = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if grid[goal[1]][goal[0]] == 0:
            break

    while True:
        user = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if grid[user[1]][user[0]] == 0 and user != goal:
            break

    while True:
        ai = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if grid[ai[1]][ai[0]] == 0 and ai != goal and ai != user:
            break

    running = True
    while running:
        # User's turn
        user = user_turn(user, grid, ai, goal)

        # Check for win/loss conditions
        if user == goal:
            print("You reached the goal! You win.")
            running = False
        elif user == ai:
            print("AI caught you! You lose.")
            running = False

        # AI's turn
        ai = ai_turn(ai, user, grid)

        # Check for win/loss conditions
        if user == ai:
            print("AI caught you! You lose.")
            running = False

        draw_grid(grid, user, ai, goal)
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()  # Show main menu
    main()  # Start the game