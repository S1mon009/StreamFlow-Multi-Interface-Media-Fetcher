"""
Module providing a utility function for the console.

This module defines the `clear_console()` function, which clears the terminal screen 
on both Windows and Unix-based systems.
"""

import os

def clear_console():
    """
    Clears the console screen.

    Works for both Windows ('cls') and Unix-based ('clear') operating systems.
    """

    os.system('cls' if os.name == 'nt' else 'clear')
