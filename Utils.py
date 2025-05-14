import random
from typing import *
import sys

# Move cursor to the beginning of the line and clear it
def clear_previous_line(iterations=1):
    for _ in range(iterations):
        sys.stdout.write('\033[F\033[2K')
        sys.stdout.flush()


# Define ANSI color codes
ANSI_COLORS = {
    "blue": "\033[34m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "light_gray": "\033[37m",
    "dark_gray": "\033[90m",
    "white": "\033[97m",
    "black": "\033[30m",
    "reset": "\033[0m"
}

GENERIC_NAMES=["ALICE", "BOB", "CAROL", "DOUGLAS", "ERIC", "FRED", "GARY", "HANNA"] 

def color_text(color, text):
    """
    Wraps the given text with the ANSI escape code for the specified color.
    
    Parameters:
    - color (str): The name of the color. Must be a key in ANSI_COLORS.
    - text (str): The text to color.
    
    Returns:
    - str: The colored text.
    """
    color_code = ANSI_COLORS.get(color.lower(), "")
    reset_code = ANSI_COLORS["reset"]
    return f"{color_code}{text}{reset_code}"

def clear():
    """
    Clear the console. 
    """
    print("\033[2J\033[H", end="")

