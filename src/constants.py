from pathlib import Path

# Path
PATH = str(Path.cwd())[:len(str(Path.cwd()))-3]
#PATH = "C:/Users/Elias/Downloads/Pygame-Chess-Engine-master/Pygame-Chess-Engine-master"

# Screen dimensions
HEIGHT = 1200
WIDTH = 1200

# Board dimensions
ROWS = 8
COLS = 8
SQSIZE = WIDTH // COLS

# Game Information
FPS = 144

# options
SCREEN_DIMENSIONS = (WIDTH, HEIGHT)

# Singleplayer
STOCKFISH_ELO = 1800

# Multiplayer
SERVER_IP = "localhost"
PORT = 5555