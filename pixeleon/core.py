from browser import timer
from .utilities import insert_to_plist, sort_plist, scale_pixel, deep_copy_screen, get_color
from .game_loop import game_loop
from assets.sprites import sprites

# Configuration constants
SCALE = 3 # Screen display will be scaled by this factor. Will not affect proportions.
WIDTH = 180
HEIGHT = 120
BG_COLOR = "2" # can be any color in the colors dictionary aside from #
initialized = False # Track if initialization has occured
RETRY_LIMIT = 10  # Max retries
retry_count = 0
redraw_retry_count = 0
UP_INT = 30 # intervals for game updates in ms
keys = set() # Store pressed keys

# Global variables
screen = [[BG_COLOR for _ in range(WIDTH)] for _ in range(HEIGHT)]
previous_screen = deep_copy_screen(screen)  # For detecting changed pixels
plist = []  # List of sprite items to render in order

pscreen = Image("https://codehs.com/uploads/9be41a87f652a94836a19635bdc5f733")
pscreen.set_size(WIDTH*SCALE,HEIGHT*SCALE)
pscreen.set_position(0,0)
add(pscreen)

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

# redraw screen
def redraw():
    global screen, screen2, redraw_retry_count
    if redraw_retry_count >= RETRY_LIMIT:
        print("Redraw failed after max retries.")
        return
    populate_screen()
    bg_color = colors[BG_COLOR]  # Cache BG color
    try:
        for a in range(HEIGHT):
            for b in range(WIDTH):
                color_code = screen[a][b]
                if screen2[a][b] != color_code:  # Only update changed pixels
                    pixel(b, a, colors.get(color_code, bg_color))
        previous_screen = deep_copy_screen(screen)
        redraw_retry_count = 0  # Reset retry count on successful redraw
    except Exception as e:
        redraw_retry_count += 1
        print(f"Error while redrawing screen: {e}. Reattempting in 10ms...")
        timer.set_timeout(redraw, 10)

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
    sort_plist()

# Main game loop
def game_loop():
    if not initialized:
        return
    populate_screen()
    redraw()

# Initialization and setup
def initialize(initial_sprites):
    global pscreen
    """
    Initialize the game screen, sprites, and start the main loop.
    """
    global initialized, plist
    plist.extend(initial_sprites)
    for sprite in plist:
        insert_to_plist(sprite)
    initialized = True
    timer.set_interval(lambda: game_loop, UP_INT)

def add_sprite(sprite_id, frames):
    """
    Add a new sprite or modify an existing one with the given frames.
    """
    sprites[sprite_id] = frames

def remove_sprite(sprite_id):
    """
    Remove a sprite by its sprite_id.
    """
    if sprite_id in sprites:
        del sprites[sprite_id]
