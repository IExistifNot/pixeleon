# __init__.py

# Import core functionalities from different modules
from .core import Screen, Sprite, COLORS, initialize, redraw
from .game_loop import GameLoop, handle_key_down, handle_key_up
from .utilities import insert_to_plist, sort_plist

# Define __all__ to specify what is publicly accessible
__all__ = [
    "Screen",
    "Sprite",
    "COLORS",
    "initialize",
    "redraw",
    "GameLoop",
    "handle_key_down",
    "handle_key_up",
    "insert_to_plist",
    "sort_plist"
]

# Set the package metadata
__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"  # Assuming you've chosen MIT license
