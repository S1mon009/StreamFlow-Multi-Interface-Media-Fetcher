import socket
import time

def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Function tries to connect to the DNS (Google) public server to check the connection.
    Returns True, if you can make a connection, otherwise false.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False
   
def network_required(func):
    """A decorator who checks the function before launching if there is a network connection."""
    def wrapper(*args, **kwargs):
        while not is_connected():
            print("Brak połączenia z siecią. Oczekiwanie na przywrócenie połączenia...")
            time.sleep(5)
        return func(*args, **kwargs)
    return wrapper
