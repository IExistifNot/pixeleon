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
from pixeleon.main import *  # Import the library

# Set the game window size and scaling
WIDTH = 160
HEIGHT = 120
SCALE = 3
set_size(WIDTH * SCALE, HEIGHT * SCALE)

# Create some sprites
# Sprite class format is x, y, z, sprite, frame_index, scale, animation_delay
billy = Sprite(0,0,0,"billy") # billy and smiley are included with the base code!
smiley = Sprite(3,3,1,"smiley")
# UI class is x, y, z, is_text, sprite, color, frame_index, scale, animation_delay
numbers = UI(0, 10, 0, True, "0123456789", "6")
hello = UI(0,16,1,True,"hello, world! %", "6")

# Add the sprites to the display list
billy.insert_to_plist() # Sprites go in plist
smiley.insert_to_plist()
numbers.insert_to_uilist() # UI goes in uilist (renders on top of plist)
hello.insert_to_uilist()

# Maybe change their z
billy.update_z(3)

# Maybe start an animation
billy.start_animation(1000)

# Define a game loop
def update_game():
    # Update game logic here, such as moving characters or changing sprites
    if input_active:
        if is_key_down("a") or is_key_down("ArrowLeft"):
            billy.x += -5
        if is_key_down("d") or is_key_down("ArrowRight"):
            billy.x += 5
        if is_key_down("w") or is_key_down("ArrowUp"):
            billy.y += -5
        if is_key_down("s") or is_key_down("ArrowDown"):
            billy.y += 5
        if is_key_down(" "):
            if billy.animation != None:
                billy.stop_animation()
            else:
                billy.start_animation(1000)

# Initialize and start the game
init()
