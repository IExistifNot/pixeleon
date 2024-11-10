from browser import timer
from .utilities import insert_to_plist, sort_plist, scale_pixel, deep_copy_screen, get_color

# Configuration constants
SCALE = 3
WIDTH = 160
HEIGHT = 120
BG_COLOR = "2"  # Background color code
UP_INT = 30  # Update interval in milliseconds

# Global variables
screen = [[BG_COLOR for _ in range(WIDTH)] for _ in range(HEIGHT)]
previous_screen = deep_copy_screen(screen)  # For detecting changed pixels
sprites = {}  # Dictionary to store sprite data
keys = set()  # Store pressed keys
initialized = False  # Track if initialization has occurred
plist = []  # List of sprite items to render in order

# Color definitions
colors = {
    "0": (255, 0, 0), "1": (0, 255, 0), "2": (0, 0, 255),
    "3": (255, 255, 0), "4": (0, 255, 255), "5": (255, 165, 0),
    "6": (255, 255, 255), "7": (0, 0, 0), "8": (127, 127, 127),
    "9": (127, 0, 127), "a": (165, 42, 42)
}

# Helper functions
def pixel(pscreen, x, y, color):
    """
    Set a pixel color on the display screen.
    """
    for a in range(SCALE):
        for b in range(SCALE):
            scaled_x, scaled_y = scale_pixel(x, y, SCALE)
            pscreen.set_red(scaled_x + a, scaled_y + b, color[0])
            pscreen.set_green(scaled_x + a, scaled_y + b, color[1])
            pscreen.set_blue(scaled_x + a, scaled_y + b, color[2])

def populate_screen():
    """
    Populate the screen buffer based on the current sprites and their frames.
    """
    global screen
    screen = [[BG_COLOR for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for item in plist:
        sprite_frames = sprites[item["sprite_id"]]
        frame = sprite_frames[item["frame_index"]]
        scale = item.get("scale", 1)
        
        for row_idx, row in enumerate(frame):
            for col_idx, color_code in enumerate(row):
                if color_code != "#":
                    x, y = item["x"] + col_idx * scale, item["y"] + row_idx * scale
                    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                        screen[y][x] = color_code

def redraw(pscreen):
    """
    Redraw the screen by updating only the pixels that have changed.
    """
    global previous_screen
    bg_color = get_color(BG_COLOR, colors)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color_code = screen[y][x]
            if previous_screen[y][x] != color_code:
                pixel(pscreen, x, y, get_color(color_code, colors))
    previous_screen = deep_copy_screen(screen)

# Input handlers
def key_down(event):
    keys.add(event.key)
        
def key_up(event):
    keys.discard(event.key)

def is_key_down(key):
    return key in keys

# Game update functions
def update_sprite_position(sprite, dx, dy):
    """
    Update the position of a sprite by dx, dy.
    """
    sprite["x"] += dx
    sprite["y"] += dy

def update_frame(sprite):
    """
    Update the frame index for sprite animation.
    """
    sprite["frame_index"] = (sprite["frame_index"] + 1) % len(sprites[sprite["sprite_id"]])

def update_z(sprite, new_z_value):
    """
    Update the z-value of a sprite and re-sort the rendering list.
    """
    sprite["z"] = new_z_value
    sort_plist(plist)

# Main game loop
def game_loop(pscreen):
    if not initialized:
        return
    populate_screen()
    redraw(pscreen)

# Initialization and setup
def initialize(pscreen, initial_sprites):
    """
    Initialize the game screen, sprites, and start the main loop.
    """
    global initialized, plist
    plist.extend(initial_sprites)
    for sprite in plist:
        insert_to_plist(plist, sprite)
    initialized = True
    timer.set_interval(lambda: game_loop(pscreen), UP_INT)

# Public interface
def add_sprite(sprite_id, x=0, y=0, z=0, scale=1, frame_index=0):
    """
    Add a sprite to the list with specified parameters.
    """
    new_sprite = {
        "sprite_id": sprite_id,
        "x": x,
        "y": y,
        "z": z,
        "scale": scale,
        "frame_index": frame_index
    }
    insert_to_plist(plist, new_sprite)
