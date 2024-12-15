import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TREASURE_COLOR = (255, 223, 0)

# Grid settings
cols, rows = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt Game")

# Player settings
player_x, player_y = 0, 0
player1_x, player1_y = random.randint(0, cols - 1), random.randint(0, rows - 1)
player_color = BLUE
player1_color = GREEN



# Generate random obstacles and treasure
def generate_grid():
    obstacles = []
    for _ in range(20):  # Generate 20 random obstacles
        obstacles.append((random.randint(0, cols - 1), random.randint(0, rows - 1)))

    # Ensure treasure doesn't overlap with obstacles
    treasure = (random.randint(0, cols - 1), random.randint(0, rows - 1))
    while treasure in obstacles:
        treasure = (random.randint(0, cols - 1), random.randint(0, rows - 1))

    return obstacles, treasure


obstacles, treasure = generate_grid()

# Game loop variables
running = True
clock = pygame.time.Clock()


# Draw grid
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))


# Draw game elements
def draw_elements():
    # Draw obstacles
    for (x, y) in obstacles:
        pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw treasure
    pygame.draw.rect(screen, TREASURE_COLOR, (treasure[0] * GRID_SIZE, treasure[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw player
    pygame.draw.rect(screen, player_color, (player_x * GRID_SIZE, player_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Main game loop
while running:
    screen.fill(WHITE)
    draw_grid()
    draw_elements()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= 1
    if keys[pygame.K_DOWN] and player_y < rows - 1:
        player_y += 1
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 1
    if keys[pygame.K_RIGHT] and player_x < cols - 1:
        player_x += 1

    # Check for treasure collision
    if (player_x, player_y) == treasure:
        print("You found the treasure!")
        running = False

    # Check for obstacle collision
    if (player_x, player_y) in obstacles:
        print("You hit an obstacle! Game over.")
        running = False

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
