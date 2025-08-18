"""
Snake Game Demo

This script demonstrates how to use the `SnakeGame` class from the
`anysnake` package with a custom output callback.

The `output` function receives the game state as a NumPy ndarray,
converts it into a human-readable string format, and prints the grid
to the console. All zeros in the matrix are replaced with spaces to
create a clearer display.

Run this script to see a simple ASCII rendering of the Snake game.
"""
from anysnake import SnakeGame


def output(matrix):
    """Get matrix data from SnakeGame"""
    # Flush the cmd
    print('\n' * 50)

    print('Use Esc to exit game')

    # Convert the matrix from numpy array to str where 0s are ' '
    matrix = matrix.astype(str)
    matrix[matrix == '0'] = ' '

    # Print converted matrix
    print(matrix)


snake = SnakeGame(grid=(6, 6), interval=.5, start_len=2, callback=output)
snake.start()
