# Constants for 5x6 board
COLS, ROWS = 5, 6
WIDTH, HEIGHT = 640, 740
BOARD_WIDTH = 500
BOARD_HEIGHT = 600
SQUARE_SIZE = BOARD_WIDTH // COLS
MARGIN_X = (WIDTH - BOARD_WIDTH) // 2
MARGIN_Y = (HEIGHT - BOARD_HEIGHT) // 2 - 20
PIECE_FONT_SIZE = SQUARE_SIZE - 20

# Color themes (16 themes as per the original design)
THEMES = {
    "Classic Wood": {"light": (240, 217, 181), "dark": (181, 136, 99)},
    "Modern Blue": {"light": (173, 216, 230), "dark": (100, 100, 150)},
    "Tournament Green": {"light": (180, 255, 180), "dark": (139, 69, 19)},
    "Classic Mahogany": {"light": (205, 133, 63), "dark": (139, 69, 19)},
    "Royal Azure": {"light": (100, 149, 237), "dark": (65, 105, 225)},
    "Emerald Elite": {"light": (144, 238, 144), "dark": (34, 139, 34)},
    "Vintage Walnut": {"light": (210, 180, 140), "dark": (160, 82, 45)},
    "Marble Luxury": {"light": (220, 220, 220), "dark": (169, 169, 169)},
    "Premium Rosewood": {"light": (188, 143, 143), "dark": (165, 42, 42)},
    "Carbon Fiber": {"light": (80, 80, 80), "dark": (40, 40, 40)},
    "Arctic Aurora": {"light": (173, 216, 230), "dark": (135, 206, 250)},
    "Desert Dunes": {"light": (244, 164, 96), "dark": (210, 105, 30)},
    "Cherry Blossom": {"light": (255, 182, 193), "dark": (219, 112, 147)},
    "Oceanic Depth": {"light": (64, 224, 208), "dark": (0, 139, 139)},
    "Volcanic Obsidian": {"light": (255, 69, 0), "dark": (139, 0, 0)},
    "Zen Garden": {"light": (152, 251, 152), "dark": (107, 142, 35)}
}

# Chess pieces (Unicode)
PIECES = {
    'white': {'king': '♔', 'queen': '♕', 'rook': '♖', 
              'bishop': '♗', 'knight': '♘', 'pawn': '♙'},
    'black': {'king': '♚', 'queen': '♛', 'rook': '♜', 
              'bishop': '♝', 'knight': '♞', 'pawn': '♟'}
}

# Colors
BACKGROUND_COLOR = (50, 50, 70)
MENU_BACKGROUND = (40, 40, 60)
BUTTON_COLOR = (80, 80, 120)
STATUS_BAR_COLOR = (40, 40, 60)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 100, 100)
VALID_MOVE_COLOR = (247, 247, 105)
COORDINATES_COLOR = (200, 200, 200)
GOLD_COLOR = (255, 215, 0)

# Font settings (not initialized here)
TITLE_FONT_NAME = "georgia"
TITLE_FONT_SIZE = 48
MENU_FONT_NAME = "arial"
MENU_FONT_SIZE = 32
STATUS_FONT_NAME = "arial"
STATUS_FONT_SIZE = 24
PIECE_FONT_NAME = "segoe ui symbol"
THEME_FONT_NAME = "arial"
THEME_FONT_SIZE = 18

# Game states
MAIN_MENU = "main_menu"
SETUP_MENU = "setup_menu"
GAME = "game"
THEME_MENU = "theme_menu"