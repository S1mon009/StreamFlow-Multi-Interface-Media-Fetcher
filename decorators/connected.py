"""
Module providing network-related utilities.

This module defines:
- `is_connected()`: A function to check internet connectivity.
- `network_required`: A decorator that ensures a network connection before executing a function.
"""

import socket
import time

def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Function tries to connect to the DNS (Google) public server to check the connection.
    Returns True, if you can make a connection, otherwise false.
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
        return True
    except (socket.timeout, socket.error):
        return False

def network_required(func):
    """A decorator who checks the function before launching if there is a network connection."""
    def wrapper(*args, **kwargs):
        while not is_connected():
            print("No network connection. Waiting for the reinstatement of the connection ...")
            time.sleep(5)
        return func(*args, **kwargs)
    return wrapper
