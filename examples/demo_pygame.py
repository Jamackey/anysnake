"""
Snake Game Demo using pygame

This script demonstrates how to use the `SnakeGame` class from the
`anysnake` package for pygame.

For this example, we're using SnakeGame.get_matrix() to retrieve
the snake data in the main pygame loop. This is instead of using
the built in callback function.

Run this script to see a simple pygame version of the Snake game.
"""
import pygame
from anysnake import SnakeGame

# Define rect cell sizes
cell_size = 40
cell_pad = 2

# Create snake game class
snake = SnakeGame(grid=(10, 10), interval=.5, start_len=2)
snake.start()

# Setup pygame
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("AnySnake Snake Game - Esc to close")

# Setup running loop
running = True
while running:
    # Close all if pygame is quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            snake.join()

    # If SnakeGame is stopped, close pygame
    if snake.stop is True:
        running = False

    # Key press is usually done here, but is handled
    # by SnakeGame

    # Fill screen with white bg
    screen.fill('white')

    # Create cells using the snake matrix (flipped in the Y)
    for n, row in enumerate(snake.get_matrix(flip_y=True)):
        for i, column in enumerate(row):
            rect_size = ((n * cell_size) + cell_pad,
                         (i * cell_size) + cell_pad,
                         cell_size-(cell_pad*2),
                         cell_size-(cell_pad*2))
            if column == 0:
                colour = 'grey'
            elif column == 1:
                colour = 'green'
            else:
                colour = 'orange'
            pygame.draw.rect(screen, colour, rect_size)

    # Update pygame
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
