# Pixeleon

**Pixeleon** is a Python library for building and animating sprite-based games in CodeHS's Brython environment. With tools for sprite handling, animations, input processing, and game loops, Pixeleon simplifies creating interactive, web-friendly games.

---

## Features

- **Sprite Management**: Easily create and manage sprite animations.
- **User Input Handling**: Integrate keyboard controls for dynamic gameplay.
- **Game Loop Support**: Smoothly update and redraw screen elements at customizable intervals.
- **Customizable Scaling**: Adjust the display scale for optimal visuals.
- **Color Mapping**: Access a palette for vibrant color use in sprite creation.

---

## Requirements

Pixeleon is designed specifically for CodeHS’s Brython environment. Make sure you have a CodeHS account to run and deploy your Pixeleon-based projects, or have Brython set up in an HTML file. Tutorial here: [Brython Outside of CodeHS](https://codehs.com/tutorial/joianderson/how-to-use-python-graphics-on-your-website)

---

## Getting Started

1. **Set Up CodeHS**  
   Create a new Python project on [CodeHS](https://codehs.com) and select Python 3 Graphics (Brython).

2. **Install Pixeleon**  
   Add the Pixeleon code to your CodeHS project, either by importing the library as a `.py` file or by pasting the Pixeleon code directly.

3. **Initialize the Game**  
   Set up your game window and initialize your main sprites and game objects.

---

## Usage Example

Here’s a simple example to get started with Pixeleon.

```python
from pixeleon import *  # Import the library (assuming Pixeleon code is in pixeleon.py)

# Set the game window size and scaling
WIDTH = 160
HEIGHT = 120
SCALE = 3
set_size(WIDTH * SCALE, HEIGHT * SCALE)

# Create a sprite
placeholder_sprite = {
    "z": 0, "sprite_id": "placeholder", "x": 10, "y": 10, "scale": 1, "frame_index": 0
}

# Add the sprite to the display list
insert_to_plist(placeholder_sprite)

# Game loop
def game_loop():
    # Update logic here
    redraw()

# Initialize and start the game
init()
