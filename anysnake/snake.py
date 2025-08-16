"""anysnake/snake.py"""

import time
from threading import Thread
from typing import Callable, Optional
from dataclasses import dataclass

import numpy as np
from pynput import keyboard

Function = Callable[[int], None]


@dataclass
class Grid:
    """Grid class"""
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    grid: tuple
    matrix: np.ndarray


@dataclass
class Snake:
    """Snake class"""
    x: int
    y: int
    dir: str
    old_dir: str
    tail: list
    tail_len: int


class SnakeGame:
    """SnakeGame class for building Snake on ANYTHING"""
    def __init__(
            self,
            grid: tuple[int, int],
            interval: float,
            start_len: int = 1,
            callback: Optional[Function] = None,
            ) -> None:
        """
        Initialise the Snake Game with the following values

        Args:
            grid: Grid size (x, y)
            interval: Update interval in seconds
            start_len: Starting length of snake. Defaults to 1.
            callback: Callback method to call when updating game.
                If None, get the matrix via SnakeGame.matrix
        """
        # Create grid
        self.grid = Grid(
            min_x=0,
            min_y=0,
            max_x=grid[0],
            max_y=grid[1],
            grid=grid,
            matrix=None
            )

        # Create Snake
        self.snake = Snake(
            x=int(self.grid.max_x/2),
            y=int(self.grid.max_y/2),
            dir='',
            old_dir='',
            tail=[],
            tail_len=start_len,
            )

        # Start fruits
        self.fruit_bool = False
        self.fruit_coord = (-1, -1)

        # Running variables
        self.callback = callback
        self.update_interval = interval
        self.stop = False

    def start(self):
        """Starts the game and builds display and keyboard thread"""
        self.stop = False

        display_thread = Thread(target=self.update)
        display_thread.start()

        listner = keyboard.Listener(on_press=self.on_press,
                                    on_release=self.on_release)
        listner.start()

    def print_display(self):
        """Print the snakegame matrix and debug info to console"""
        print("\n" * 10)
        for i in np.rot90(self.grid.matrix):
            print(i)
        print('Snake Head:', (self.snake.x, self.snake.y))
        print('Snake Tail:', self.snake.tail)
        print('Fruit coord:', self.fruit_coord)
        print('New_dir:', self.snake.dir, '- Old_dir:', self.snake.old_dir)

    def update(self):
        """Main snake update loop"""
        while self.stop is False:
            self.grid.matrix = self.get_empty_grid()
            self.update_snake()
            self.update_fruits()
            # self.print_display()
            self.callback(np.rot90(self.grid.matrix))
            time.sleep(self.update_interval)

    def get_empty_grid(self):
        """Resets the grid to 0s"""
        return np.zeros(self.grid.grid, dtype=np.uint)

    def update_fruits(self):
        """Updates the fruits in the game"""
        # Create fruit
        if self.fruit_bool is False:
            coords = np.argwhere(self.grid.matrix == 0)
            rand_idx = np.random.choice(len(coords))
            self.fruit_coord = tuple(coords[rand_idx])
            self.fruit_bool = True

        # If the snake eats it, make a new fruit
        if (self.snake.x, self.snake.y) == self.fruit_coord:
            self.snake.tail_len += 1
            self.fruit_bool = False
            return

        # Display fruit
        self.grid.matrix[self.fruit_coord[0]][self.fruit_coord[1]] = 2

    def update_snake(self):
        """Updates the snake and tail in the game"""
        # Move snake
        if self.snake.dir == 'up':
            self.snake.y += 1
        elif self.snake.dir == 'down':
            self.snake.y -= 1
        elif self.snake.dir == 'left':
            self.snake.x -= 1
        elif self.snake.dir == 'right':
            self.snake.x += 1

        # Save direction snake has went last
        self.snake.old_dir = self.snake.dir

        # Wrap snake around grid
        self.snake.y = self.snake.y % self.grid.max_y
        self.snake.x = self.snake.x % self.grid.max_x

        # If not moved yet, add snake head and return
        if self.snake.dir == '':
            self.grid.matrix[self.snake.x][self.snake.y] = 1
            self.snake.tail = [(self.snake.x, self.snake.y)]
            return

        # Test if in tail
        if (self.snake.x, self.snake.y) in self.snake.tail[1:]:
            self.stop = True

        # Create tail
        self.snake.tail = [(self.snake.x, self.snake.y)] + self.snake.tail
        self.snake.tail = self.snake.tail[:self.snake.tail_len + 1]

        # Add snake tail to matrix
        for tail_pixel in self.snake.tail:
            self.grid.matrix[tail_pixel] = 1

    def set_dir(self, direction):
        """Set the next snake direction"""
        # Check new snake direction against last snake direction
        for invalid_dir in [('left', 'right'), ('up', 'down')]:
            if self.snake.old_dir in invalid_dir and direction in invalid_dir:
                return

        # Write direction
        self.snake.dir = direction

    def on_press(self, key):
        """Keyboard callback for pressed keys"""

    def on_release(self, key):
        """Keyboard callback for released keys"""
        try:
            if key.char == 'a':
                self.set_dir('left')
            elif key.char == 'd':
                self.set_dir('right')
            elif key.char == 'w':
                self.set_dir('up')
            elif key.char == 's':
                self.set_dir('down')
        except AttributeError:
            pass

        if key == keyboard.Key.esc:
            self.stop = True
        elif key == keyboard.Key.up:
            self.set_dir('up')
        elif key == keyboard.Key.down:
            self.set_dir('down')
        elif key == keyboard.Key.left:
            self.set_dir('left')
        elif key == keyboard.Key.right:
            self.set_dir('right')
