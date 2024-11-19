from bisect import bisect_left
from browser import timer

SCALE = 6 # Screen display will be scaled by this factor. Will not affect proportions.
WIDTH = 80
HEIGHT = 60
BG_COLOR = "2" # can be any color in the colors dictionary aside from #
INIT = False
RETRY_LIMIT = 10  # Max retries
retry_count = 0
redraw_retry_count = 0
UP_INT = 50 # intervals for game updates in ms
keys = set()

set_size(WIDTH * SCALE,HEIGHT * SCALE)
# spritelists should use these values to create an image, and use # or another symbol to skip a spot
# order is 0:red, 1:green, 2:blue, 3:yellow, 4:cyan, 5:orange, 6:white, 7:black, 8:gray, 9:purple, a:brown
colors = {"0":(255,0,0), "1":(0,255,0), "2":(0,0,255), "3":(255,255,0), "4":(0,255,255), "5":(255,165,0), "6":(255,255,255), "7":(0,0,0), "8":(127,127,127), "9":(127,0,127), "a":(165,42,42)}

# create a grid for representing screen values in the form of a spritelist
screen = [[BG_COLOR for _ in range(WIDTH)] for _ in range(HEIGHT)]
screen2 = [row[:] for row in screen]  # Explicit deep copy at the start

pscreen = Image("https://codehs.com/uploads/9be41a87f652a94836a19635bdc5f733")
pscreen.set_size(WIDTH*SCALE,HEIGHT*SCALE)
pscreen.set_position(0,0)
add(pscreen)

# Define animated sprites with each frame as a list of lists
# a value for a spritelist can be quickly created at https://codehs.com/sandbox/blahajay/img-to-tuple
sprites = {
    "billy": (
        (
            ("#","#","7","7","7","7","#","#"), # smile
            ("#","7","1","1","1","1","7","#"),
            ("7","1","7","1","1","7","1","7"),
            ("7","1","1","1","1","1","1","7"),
            ("7","1","7","1","1","7","1","7"),
            ("7","1","1","7","7","1","1","7"),
            ("#","7","1","1","1","1","7","#"),
            ("#","#","7","7","7","7","#","#")
        ),
        (
            ("#","#","7","7","7","7","#","#"), # flat
            ("#","7","8","8","8","8","7","#"),
            ("7","8","7","8","8","7","8","7"),
            ("7","8","8","8","8","8","8","7"),
            ("7","8","8","8","8","8","8","7"),
            ("7","8","7","7","7","7","8","7"),
            ("#","7","8","8","8","8","7","#"),
            ("#","#","7","7","7","7","#","#")
        ),
        (
            ("#","#","7","7","7","7","#","#"), # frown
            ("#","7","2","2","2","2","7","#"),
            ("7","2","7","2","2","7","2","7"),
            ("7","2","2","2","2","2","2","7"),
            ("7","2","2","7","7","2","2","7"),
            ("7","2","7","2","2","7","2","7"),
            ("#","7","2","2","2","2","7","#"),
            ("#","#","7","7","7","7","#","#")
        )
    ),
    "smiley": (
        (
            ("#", "#", "3", "3", "3", "3", "#", "#"),
            ("#", "3", "7", "#", "#", "7", "3", "#"),
            ("3", "3", "#", "#", "#", "#", "3", "3"),
            ("3", "3", "7", "#", "#", "7", "3", "3"),
            ("3", "3", "#", "#", "#", "#", "3", "3"),
            ("3", "#", "3", "#", "#", "3", "#", "3"),
            ("#", "3", "#", "3", "3", "#", "3", "#"),
            ("#", "#", "3", "3", "3", "3", "#", "#")
        ),
    )
}

letters = {
    "a":(
        (0,1,1,0),
        (1,0,0,1),
        (1,1,1,1),
        (1,0,0,1),
        (1,0,0,1)
    ),
    "b":(
        (1,1,1,0),
        (1,0,0,1),
        (1,1,1,0),
        (1,0,0,1),
        (1,1,1,0),
    ),
    "c": (
        (0,1,1,1),
        (1,0,0,0),
        (1,0,0,0),
        (1,0,0,0),
        (0,1,1,1)
    ),
    "d": (
        (1,1,1,0),
        (1,0,0,1),
        (1,0,0,1),
        (1,0,0,1),
        (1,1,1,0)
    ),
    "e": (
        (1,1,1),
        (1,0,0),
        (1,1,1),
        (1,0,0),
        (1,1,1)
    ),
    "f": (
        (1,1,1,1),
        (1,0,0,0),
        (1,1,1,1),
        (1,0,0,0),
        (1,0,0,0)
    ),
    "g": (
        (0,1,1,1),
        (1,0,0,0),
        (1,0,1,1),
        (1,0,0,1),
        (0,1,1,0)
    ),
    "h": (
        (1,0,1),
        (1,0,1),
        (1,1,1),
        (1,0,1),
        (1,0,1)
    ),
    "i": (
        (1,1,1),
        (0,1,0),
        (0,1,0),
        (0,1,0),
        (1,1,1)
    ),
    "j": (
        (1,1,1,1),
        (0,0,0,1),
        (0,0,0,1),
        (0,0,0,1),
        (1,1,1,0)
    ),
    "k": (
        (1,0,0,1),
        (1,0,1,0),
        (1,1,0,0),
        (1,0,1,0),
        (1,0,0,1)
    ),
    "l": (
        (1,0,0,),
        (1,0,0,),
        (1,0,0,),
        (1,0,0,),
        (1,1,1,)
    ),
    "m": (
        (0,1,0,1,0),
        (1,0,1,0,1),
        (1,0,1,0,1),
        (1,0,1,0,1),
        (1,0,1,0,1)
    ),
    "n": (
        (1,0,0,1),
        (1,1,0,1),
        (1,1,1,1),
        (1,0,1,1),
        (1,0,0,1)
    ),
    "o": (
        (0,1,1,0),
        (1,0,0,1),
        (1,0,0,1),
        (1,0,0,1),
        (0,1,1,0)
    ),
    "p": (
        (1,1,1,0),
        (1,0,0,1),
        (1,1,1,0),
        (1,0,0,0),
        (1,0,0,0)
    ),
    "q": (
        (0,1,1,0),
        (1,0,0,1),
        (1,0,0,1),
        (1,0,1,1),
        (0,1,1,1)
    ),
    "r": (
        (1,1,1,0),
        (1,0,0,1),
        (1,1,1,0),
        (1,0,1,0),
        (1,0,0,1)
    ),
    "s": (
        (0,1,1,1),
        (1,0,0,0),
        (0,1,1,0),
        (0,0,0,1),
        (1,1,1,0)
    ),
    "t": (
        (1,1,1),
        (0,1,0),
        (0,1,0),
        (0,1,0),
        (0,1,0)
    ),
    "u": (
        (1,0,0,1),
        (1,0,0,1),
        (1,0,0,1),
        (1,0,0,1),
        (0,1,1,0)
    ),
    "v": (
        (1,0,0,0,1),
        (1,0,0,0,1),
        (1,0,0,0,1),
        (0,1,0,1,0),
        (0,0,1,0,0)
    ),
    "w": (
        (1,0,1,0,1),
        (1,0,1,0,1),
        (1,0,1,0,1),
        (1,0,1,0,1),
        (0,1,0,1,0)
    ),
    "x": (
        (1,0,1),
        (1,0,1),
        (0,1,0),
        (1,0,1),
        (1,0,1)
    ),
    "y": (
        (1,0,1),
        (1,0,1),
        (0,1,0),
        (0,1,0),
        (0,1,0)
    ),
    "z": (
        (1,1,1,1,1),
        (0,0,0,1,0),
        (0,0,1,0,0),
        (0,1,0,0,0),
        (1,1,1,1,1)
    ),
    " ": (
        (0,),
        (0,),
        (0,),
        (0,),
        (0,),
    ),
    ".": (
        (0,),
        (0,),
        (0,),
        (0,),
        (1,)
    ),
    ",": (
        (0,),
        (0,),
        (0,),
        (1,),
        (1,)
    ),
    "!": (
        (1,),
        (1,),
        (1,),
        (0,),
        (1,)
    ),
    "?": (
        (1,1,0),
        (0,0,1),
        (0,1,0),
        (0,0,0),
        (0,1,0)
    ),
    "0": (
        (0,1,1,0),
        (1,0,0,1),
        (1,1,1,1),
        (1,0,0,1),
        (0,1,1,0)
    ),
    "1": (
        (0,1,0),
        (1,1,0),
        (0,1,0),
        (0,1,0),
        (1,1,1)
    ),
    "2": (
        (0,1,1,0),
        (1,0,0,1),
        (0,0,1,0),
        (0,1,0,0),
        (1,1,1,1)
    ),
    "3": (
        (1,1,0),
        (0,0,1),
        (1,1,0),
        (0,0,1),
        (1,1,0)
    ),
    "4": (
        (1,0,1),
        (1,0,1),
        (1,1,1),
        (0,0,1),
        (0,0,1)
    ),
    "5": (
        (1,1,1),
        (1,0,0),
        (1,1,1),
        (0,0,1),
        (1,1,0)
    ),
    "6": (
        (0,1,1),
        (1,0,0),
        (1,1,1),
        (1,0,1),
        (1,1,1)
    ),
    "7": (
        (1,1,1,1),
        (0,0,0,1),
        (0,0,1,0),
        (0,1,0,0),
        (1,0,0,0)
    ),
    "8": (
        (0,1,1,0),
        (1,0,0,1),
        (0,1,1,0),
        (1,0,0,1),
        (0,1,1,0)
    ),
    "9": (
        (0,1,1,0),
        (1,0,0,1),
        (0,1,1,1),
        (0,0,1,0),
        (0,1,0,0)
    )
}

# `plist` references sprite IDs and frame indexes
# z, sprite, x, y, scale, and frame values
class BaseSprite:
    def __init__(self, x=0, y=0, z=0, sprite="smiley", frame_index=0, scale=1, animation_delay=UP_INT):
        self.x = x
        self.y = y
        self.z = z
        self.sprite = sprite
        self.frame_index = frame_index
        self.scale = scale
        self.animation_delay = animation_delay
        self.cached_sprite = None
        self.cached_id = None
        self.animation = None
       
    def update_frame(self):
        self.frame_index = (self.frame_index + 1) % len(sprites[self.sprite])

    def update_z(self, new_z, lst):
        self.z = new_z
        sort_list(lst)  # Ensure `sort_list` is defined to sort by `z`

    def start_animation(self, time=None):
        if time is None:
            time = self.animation_delay
        self.animation = timer.set_interval(self.update_frame, time)
    def stop_animation(self):
        if self.animation:
            timer.clear_interval(self.animation)
            self.animation = None  # Reset animation state

class Sprite(BaseSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_z(self, new_z):
        super().update_z(new_z, plist)

    def insert_to_plist(self):
        insert_to_list(self, plist)

class UI(BaseSprite):
    def __init__(self, x=0, y=0, z=0, is_text=False, sprite="smiley", color="7", frame_index=0, scale=1, animation_delay=UP_INT):
        super().__init__(x, y, z, sprite, frame_index, scale, animation_delay)
        self.is_text = is_text
        self.color = color

    def update_z(self, new_z):
        super().update_z(new_z, uilist)

    def insert_to_uilist(self):
        insert_to_list(self, uilist)
# Sprite class format is x, y, z, sprite, frame_index, scale, animation_delay
# UI class is x, y, z, is_text, sprite, color, frame_index, scale, animation_delay
# create lists of what needs to be written in order
plist = []
uilist = []

def pixel(x,y,color):
    for a in range(SCALE):
        for b in range(SCALE):
            pscreen.set_red(x*SCALE+a,y*SCALE+b,color[0])
            pscreen.set_green(x*SCALE+a,y*SCALE+b,color[1])
            pscreen.set_blue(x*SCALE+a,y*SCALE+b,color[2])

def text_to_sprite(text, color):
    spr = [[] for _ in range(5)]  # Initialize with five rows
    for char in text:
        if char in letters:
            for a in range(5):
                for b in range(len(letters[char][0])):
                    spr[a].append(color if letters[char][a][b] == 1 else "#")
                spr[a].extend(("#", "#"))  # Space between characters
        else:
            print(f"Character {char} unable to be found.")
    return spr

def insert_to_list(new, list):
    # Find the correct insertion index for the new dictionary based on the "z" key
    index = bisect_left([pair.z for pair in list], new.z)
    # Insert the new dictionary at the identified index
    list.insert(index, new)

def sort_list(list):
    # Sort plist by the "z" value of each dictionary
    list.sort(key=lambda item: item.z)

# Populate screen based on `plist` with scaling support and frame index for animation
def populate_screen():
    global screen
    screen = [[BG_COLOR] * WIDTH for _ in range(HEIGHT)]  # Reset screen

    # Process `plist` items
    for item in plist:
        sprite = sprites[item.sprite][item.frame_index] if item.cached_id != item.sprite + str(item.frame_index) else item.cached_sprite
        if item.cached_id != item.sprite + str(item.frame_index):
            item.cached_sprite = sprite
            item.cached_id = item.sprite + str(item.frame_index)
        
        for a, row in enumerate(sprite):
            for b, color_code in enumerate(row):
                if color_code != "#":
                    start_y, start_x = item.y + a * item.scale, item.x + b * item.scale
                    for dy in range(item.scale):
                        for dx in range(item.scale):
                            y, x = start_y + dy, start_x + dx
                            if 0 <= y < HEIGHT and 0 <= x < WIDTH:
                                screen[y][x] = color_code

    # Process `uilist` items
    for item in uilist:
        sprite = (text_to_sprite(item.sprite, item.color) if item.is_text else sprites[item.sprite][item.frame_index]) if item.cached_id != item.sprite + ("" if item.is_text else str(item.frame_index)) else item.cached_sprite
        if item.cached_id != item.sprite + ("" if item.is_text else str(item.frame_index)):
            item.cached_sprite = sprite
            item.cached_id = item.sprite + ("" if item.is_text else str(item.frame_index))
        
        for a, row in enumerate(sprite):
            for b, color_code in enumerate(row):
                if color_code != "#":
                    start_y, start_x = item.y + a * item.scale, item.x + b * item.scale
                    for dy in range(item.scale):
                        for dx in range(item.scale):
                            y, x = start_y + dy, start_x + dx
                            if 0 <= y < HEIGHT and 0 <= x < WIDTH:
                                screen[y][x] = color_code

# redraw the screen
def redraw():
    global screen, screen2, redraw_retry_count
    if redraw_retry_count >= RETRY_LIMIT:
        print("Redraw failed after max retries.")
        return
    populate_screen()
    bg_color = colors[BG_COLOR]  # Cache BG color once per frame
    try:
        for a in range(HEIGHT):
            for b in range(WIDTH):
                color_code = screen[a][b]
                if screen2[a][b] != color_code:  # Only update changed pixels
                    pixel(b, a, colors.get(color_code, bg_color))
        # Only copy screen to screen2 if no exceptions occurred
        screen2 = [row[:] for row in screen]  # Deep copy
        redraw_retry_count = 0  # Reset retry count on successful redraw
    except Exception as e:
        redraw_retry_count += 1
        print(f"Error while redrawing screen: {e}. Reattempting in 10ms...")
        timer.set_timeout(redraw, 10)


def game_loop():
    if not INIT:
        return  # Stop if not initialized
    update_game()
    redraw()

def key_down(event):
    global keys
    keys.add(event.key)
       
def key_up(event):
    global keys
    keys.discard(event.key)

def is_key_down(key):
    return key in keys

def update_game():
    # Update game logic here, such as moving characters or changing sprites
    pass

add_key_down_handler(key_down)
add_key_up_handler(key_up)

# Initialize the screen with initial sprites
def init():
    global INIT, retry_count, input_active
    if retry_count >= RETRY_LIMIT:
        print("Initialization failed after max retries.")
        return
    elif retry_count == 0:
        print("Beginning initialization. Please be patient.")
    populate_screen()
    try:
        for a in range(HEIGHT):
            for b in range(WIDTH):
                pixel(b, a, colors[screen[a][b]])
        screen2 = [row[:] for row in screen]  # Deep copy for initial screen
        print("Initialized!")
        INIT = True
        input_active = True  # Enable input once initialized
        retry_count = 0
        timer.set_interval(game_loop, UP_INT)  # Start the game loop, pausing for UP_INT ms (defaults to 30).
    except Exception as e:
        if str(e) != "'NoneType' object has no attribute 'data'":
            print(f"Something went wrong during initialization: {e}. Retrying in 100ms...")
        retry_count += 1
        timer.set_timeout(init, 100)
