# anysnake

`anysnake` is a super basic snake game that allows you to play it on any device with a Python API and a matrix display.
This could be LED's on the front of a network switch, oscilloscope or even plumb it straight into pygame.

## Installation

Install via pip:

```bash
pip install anysnake
```

Or install from source:

```bash
git clone https://github.com/yourusername/anysnake.git
cd anysnake
pip install -e .
```

## Usage

```python
from anysnake import SnakeGame

def output(matrix):
    """Get matrix data from SnakeGame"""
    print('\n' * 10)
    print(matrix)

snake = SnakeGame(grid=(6, 6), interval=1, start_len=2, callback=output)
snake.start()

```

## Contributing

Contributions are encouraged. Try this and send your crazy snake games to feature in our anysnake project.
For any issues please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
