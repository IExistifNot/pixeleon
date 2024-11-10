# Import core functionalities from different modules
from .core import Screen, Sprite, initialize, redraw
from .game_loop import GameLoop, handle_key_down, handle_key_up
from .utilities import insert_to_plist, sort_plist
from .config import SCALE, WIDTH, HEIGHT, BG_COLOR, RETRY_LIMIT, UP_INT, colors

# Define __all__ to specify what is publicly accessible
__all__ = [
    "Screen",
    "Sprite",
    "initialize",
    "redraw",
    "GameLoop",
    "handle_key_down",
    "handle_key_up",
    "insert_to_plist",
    "sort_plist",
    "SCALE",
    "WIDTH",
    "HEIGHT",
    "BG_COLOR",
    "RETRY_LIMIT",
    "UP_INT",
    "colors"
]

# Set the package metadata
__version__ = "1.0.0"
__author__ = "Jack Tiedemann"
__license__ = "MIT"  # Assuming you've chosen MIT license
