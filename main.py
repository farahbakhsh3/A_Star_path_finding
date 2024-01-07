import sys

import numpy as np
import pygame

import AStar

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 25
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_LINE_COLOR = (150, 150, 150)
START_COLOR = (255, 0, 0)
END_COLOR = (0, 255, 0)
PATH_COLOR = (255, 255, 0)
HINT_COLOR = (0, 255, 255)

# Values
WHITE_VALUE = 0
BLACK_VALUE = 1
find_path = False
path = None
allow_diagonal_movement = True

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finder")

# Initialize grid as a NumPy array
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

# Start and end points
start_point = (0, 0)
end_point = (grid.shape[0] - 1, grid.shape[1] - 1)

# Drawing mode
drawing_mode = 'draw'  # 'draw' or 'erase'

# Fonts
font = pygame.font.Font(None, 36)

# hints
hint = ("(D) :: Draw walls \n (E) : Erase walls \n (Q) :: Change diagonal movement \n"
        "(C) :: Clear maze \n (R) :: Run A* Path Finder \n (F) :: Start Point \n (S) :: End Point"
        +"\n\n (Space) :: Close hint")

# Main loop
drawing = False
running = True
show_hint = True

def draw_text(text, font, color, x, y):
    lines = text.split("\n")  # Split the text into lines
    y_offset = 0

    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y + y_offset)
        screen.blit(text_surface, text_rect)
        y_offset += 30  # Adjust the vertical spacing between lines

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            gridX, gridY = mouseX // CELL_SIZE, mouseY // CELL_SIZE
            if drawing_mode == 'draw':
                if 0 <= gridY < GRID_SIZE and 0 <= gridX < GRID_SIZE:
                    grid[gridY, gridX] = BLACK_VALUE
            elif drawing_mode == 'erase':
                if 0 <= gridY < GRID_SIZE and 0 <= gridX < GRID_SIZE:
                    grid[gridY, gridX] = WHITE_VALUE
            elif drawing_mode == 'set_start':
                if 0 <= gridY < GRID_SIZE and 0 <= gridX < GRID_SIZE:
                    start_point = (gridY, gridX)
                    grid[gridY, gridX] = WHITE_VALUE
            elif drawing_mode == 'set_end':
                if 0 <= gridY < GRID_SIZE and 0 <= gridX < GRID_SIZE:
                    end_point = (gridY, gridX)
                    grid[gridY, gridX] = WHITE_VALUE
            if drawing_mode == 'draw' or drawing_mode == 'erase':
                drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION and drawing:
            mouseX, mouseY = event.pos
            gridX, gridY = mouseX // CELL_SIZE, mouseY // CELL_SIZE
            if drawing_mode == 'draw':
                if 0 <= gridY < GRID_SIZE and 0 <= gridX < GRID_SIZE:
                    grid[gridY, gridX] = BLACK_VALUE
            elif drawing_mode == 'erase':
                if 0 <= gridY < GRID_SIZE and 0 <= gridX < GRID_SIZE:
                    grid[gridY, gridX] = WHITE_VALUE
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                drawing_mode = 'erase'
            elif event.key == pygame.K_d:
                drawing_mode = 'draw'
            elif event.key == pygame.K_s:
                drawing_mode = 'set_start'
            elif event.key == pygame.K_f:
                drawing_mode = 'set_end'
            elif event.key == pygame.K_c:
                grid.fill(WHITE_VALUE)
                find_path = False
            elif event.key == pygame.K_r:
                a_star = AStar.AStar(grid, start_point, end_point)
                path = a_star.astar(allow_diagonal_movement)
                if path is not None:
                    print(len(path), path)
                    find_path = True
                else:
                    find_path = False
            elif event.key == pygame.K_q:
                allow_diagonal_movement = not allow_diagonal_movement
            elif event.key == pygame.K_SPACE:
                show_hint = not show_hint

    # Draw message
    if show_hint:
        draw_text(hint, font, HINT_COLOR, WIDTH // 2, HEIGHT // 3)
    else:
        # Draw the grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                color = WHITE if grid[y, x] == WHITE_VALUE else BLACK_VALUE
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw finded path with A* algorithm
        if find_path:
            for point in path:
                pygame.draw.rect(screen, PATH_COLOR,
                                 (point[1] * CELL_SIZE, point[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw start and end points
        if start_point:
            pygame.draw.rect(screen, START_COLOR,
                             (start_point[1] * CELL_SIZE, start_point[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if end_point:
            pygame.draw.rect(screen, END_COLOR,
                             (end_point[1] * CELL_SIZE, end_point[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            pygame.draw.line(screen, GRID_LINE_COLOR,
                             (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 1)
            pygame.draw.line(screen, GRID_LINE_COLOR,
                             (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 1)

    pygame.display.flip()
    pygame.time.Clock().tick(100)

# Quit Pygame
pygame.quit()
sys.exit()
