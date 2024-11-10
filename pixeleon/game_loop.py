from browser import timer
from pixeleon.core import update_game, redraw

UP_INT = 30  # Interval for game updates (milliseconds)

def game_loop():
    """
    Main loop for the game. This will be called at regular intervals (UP_INT).
    It checks if the game is initialized, and if not, it will stop the loop.
    Then it updates the game and redraws the screen.
    """
    if not initialized:
        return  # Stop the loop if not initialized
    update_game()  # Update the game logic (movement, state, etc.)
    redraw()  # Redraw the screen (only changes since the last frame)
