from bisect import bisect_left

def insert_to_plist(new):
    global plist
    """
    Insert a new dictionary into plist based on its "z" key value to maintain a sorted order.

    Args:
        plist (list): List of dictionaries, each containing a "z" key.
        new (dict): New dictionary to insert, containing a "z" key.
    """
    index = bisect_left([item["z"] for item in plist], new["z"])
    plist.insert(index, new)


def sort_plist():
    global plist
    """
    Sort plist in place by the "z" key of each dictionary.

    Args:
        plist (list): List of dictionaries to sort by "z" key.
    """
    plist.sort(key=lambda item: item["z"])


def scale_pixel(x, y, scale):
    """
    Scale pixel coordinates by a given factor.

    Args:
        x (int): X coordinate of the pixel.
        y (int): Y coordinate of the pixel.
        scale (int): Scaling factor.

    Returns:
        tuple: Scaled (x, y) coordinates.
    """
    return x * scale, y * scale


def deep_copy_screen(screen):
    """
    Create a deep copy of a 2D screen list.

    Args:
        screen (list of lists): Original screen list.

    Returns:
        list of lists: Deep copy of the screen list.
    """
    return [row[:] for row in screen]


def get_color(color_code):
    """
    Get RGB values for a given color code.

    Args:
        color_code (str): The code representing a color (e.g., "0" for red).
        colors_dict (dict): Dictionary of color codes and their RGB values.

    Returns:
        tuple: RGB values for the color code.
    """
    return colors.get(color_code, (0, 0, 0))  # Default to black if color code not found

