import pygame
import sys
from pygame.locals import *

pygame.init()

# Constants
WIDTH, HEIGHT = 640, 740
BOARD_SIZE = 560
MARGIN = 40
SQUARE_SIZE = BOARD_SIZE // 8
PIECE_FONT_SIZE = SQUARE_SIZE - 20

# Color themes
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

# Fonts
TITLE_FONT = pygame.font.SysFont("georgia", 48, bold=True)
MENU_FONT = pygame.font.SysFont("arial", 32)
STATUS_FONT = pygame.font.SysFont("arial", 24)
PIECE_FONT = pygame.font.SysFont("segoe ui symbol", PIECE_FONT_SIZE)
THEME_FONT = pygame.font.SysFont("arial", 20)

class MiniChess:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ChessChamp")
        
        self.state = "main_menu"  # main_menu, game, theme_menu
        self.current_theme = "Classic Wood"
        self.current_player = "white"
        self.selected_square = None
        self.valid_moves = []
        self.move_history = []
        self.history_index = -1
        
        self.board = self.setup_board()
        self.board_history = [self.copy_board()]
        
    def setup_board(self):
        """Initialize the chess board with pieces"""
        board = [[None]*8 for _ in range(8)]
        
        # Pawns
        for col in range(8):
            board[1][col] = ('black', 'pawn')
            board[6][col] = ('white', 'pawn')
        
        # Other pieces
        back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col, piece in enumerate(back_row):
            board[0][col] = ('black', piece)
            board[7][col] = ('white', piece)
            
        return board
    
    def copy_board(self):
        """Create a deep copy of the current board state"""
        return [row.copy() for row in self.board]
    
    def draw_main_menu(self):
        """Draw the main menu screen"""
        self.screen.fill((50, 50, 70))
        
        # Title
        title = TITLE_FONT.render("MiniChess", True, (255, 215, 0))
        title_rect = title.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        # Menu options
        mouse_pos = pygame.mouse.get_pos()
        options = ["New Game", "Quit"]
        
        for i, option in enumerate(options):
            rect = pygame.Rect(WIDTH//2 - 100, 250 + i*80, 200, 50)
            color = (80, 80, 120) if rect.collidepoint(mouse_pos) else (50, 50, 80)
            
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, (200, 200, 255), rect, 2, border_radius=10)
            
            text = MENU_FONT.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    def draw_theme_menu(self):
        """Draw the theme selection menu"""
        self.screen.fill((40, 40, 60))
        
        # Title
        title = MENU_FONT.render("Board Theme", True, (255, 255, 255))
        self.screen.blit(title, (20, 20))
        
        # Theme options in 2 columns
        mouse_pos = pygame.mouse.get_pos()
        theme_names = list(THEMES.keys())
        half = len(theme_names) // 2
        
        for i, theme in enumerate(theme_names):
            col = 0 if i < half else 1
            row = i if i < half else i - half
            
            x = 20 + col * (WIDTH//2 - 10)
            y = 80 + row * 40
            
            # Checkbox
            checkbox = pygame.Rect(x, y + 5, 20, 20)
            pygame.draw.rect(self.screen, (200, 200, 200), checkbox, 2)
            
            if theme == self.current_theme:
                pygame.draw.rect(self.screen, (100, 255, 100), checkbox.inflate(-4, -4))
            
            # Theme name
            text = THEME_FONT.render(theme, True, (255, 255, 255))
            self.screen.blit(text, (x + 30, y))
            
            # Hover effect
            option_rect = pygame.Rect(x, y, WIDTH//2 - 30, 30)
            if option_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (80, 80, 120, 100), option_rect, border_radius=5)
        
        # Back button
        back_rect = pygame.Rect(20, HEIGHT - 60, 100, 40)
        pygame.draw.rect(self.screen, (80, 80, 120), back_rect, border_radius=5)
        back_text = THEME_FONT.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, (back_rect.centerx - 25, back_rect.centery - 10))
        
        pygame.display.flip()
    
    def draw_game(self):
        """Draw the game board and interface"""
        theme = THEMES[self.current_theme]
        self.screen.fill((50, 50, 70))
        
        # Draw board
        for row in range(8):
            for col in range(8):
                x = MARGIN + col * SQUARE_SIZE
                y = MARGIN + row * SQUARE_SIZE
                
                # Square color
                if (row, col) == self.selected_square:
                    color = (255, 100, 100)
                elif (row, col) in self.valid_moves:
                    color = (247, 247, 105)
                elif (row + col) % 2 == 0:
                    color = theme["light"]
                else:
                    color = theme["dark"]
                
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw piece
                piece = self.board[row][col]
                if piece:
                    color, type = piece
                    text = PIECE_FONT.render(PIECES[color][type], True, 
                                           (255, 255, 255) if color == 'white' else (50, 50, 50))
                    self.screen.blit(text, (x + SQUARE_SIZE//2 - text.get_width()//2, 
                                          y + SQUARE_SIZE//2 - text.get_height()//2))
        
        # Draw coordinates
        for i in range(8):
            # Letters at bottom
            letter = chr(97 + i)
            text = STATUS_FONT.render(letter, True, (200, 200, 200))
            self.screen.blit(text, (MARGIN + i*SQUARE_SIZE + SQUARE_SIZE//2 - 5, 
                                  MARGIN + 8*SQUARE_SIZE + 10))
            
            # Numbers on left
            number = str(8 - i)
            text = STATUS_FONT.render(number, True, (200, 200, 200))
            self.screen.blit(text, (10, MARGIN + i*SQUARE_SIZE + SQUARE_SIZE//2 - 10))
        
        # Draw status bar
        status_bar = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)
        pygame.draw.rect(self.screen, (40, 40, 60), status_bar)
        
        # Turn indicator
        turn_text = STATUS_FONT.render(f"{self.current_player.capitalize()}'s turn", True, (255, 255, 255))
        self.screen.blit(turn_text, (20, HEIGHT - 30))
        
        # Undo/Redo buttons
        undo_rect = pygame.Rect(WIDTH - 220, HEIGHT - 35, 80, 30)
        redo_rect = pygame.Rect(WIDTH - 120, HEIGHT - 35, 80, 30)
        
        pygame.draw.rect(self.screen, (80, 80, 120), undo_rect, border_radius=5)
        pygame.draw.rect(self.screen, (80, 80, 120), redo_rect, border_radius=5)
        
        undo_text = STATUS_FONT.render("📄 Undo", True, (255, 255, 255))
        redo_text = STATUS_FONT.render("🍀 Redo", True, (255, 255, 255))
        
        self.screen.blit(undo_text, (undo_rect.centerx - undo_text.get_width()//2, 
                                   undo_rect.centery - undo_text.get_height()//2))
        self.screen.blit(redo_text, (redo_rect.centerx - redo_text.get_width()//2, 
                                   redo_rect.centery - redo_text.get_height()//2))
        
        # Theme button
        theme_rect = pygame.Rect(WIDTH - 350, HEIGHT - 35, 110, 30)
        pygame.draw.rect(self.screen, (80, 80, 120), theme_rect, border_radius=5)
        theme_text = STATUS_FONT.render("Themes", True, (255, 255, 255))
        self.screen.blit(theme_text, (theme_rect.centerx - theme_text.get_width()//2, 
                                    theme_rect.centery - theme_text.get_height()//2))
        
        pygame.display.flip()
    
    def get_valid_moves(self, row, col):
        """Get valid moves for the piece at (row, col)"""
        # Simplified movement rules for demonstration
        piece = self.board[row][col]
        if not piece:
            return []
        
        color, type = piece
        moves = []
        
        if type == 'pawn':
            direction = -1 if color == 'white' else 1
            # Forward move
            if 0 <= row + direction < 8 and not self.board[row + direction][col]:
                moves.append((row + direction, col))
            # Captures
            for dc in [-1, 1]:
                if 0 <= col + dc < 8 and 0 <= row + direction < 8:
                    target = self.board[row + direction][col + dc]
                    if target and target[0] != color:
                        moves.append((row + direction, col + dc))
        
        elif type in ['rook', 'queen']:
            # Horizontal and vertical moves
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                for i in range(1, 8):
                    r, c = row + dr*i, col + dc*i
                    if not (0 <= r < 8 and 0 <= c < 8):
                        break
                    target = self.board[r][c]
                    if not target:
                        moves.append((r, c))
                    else:
                        if target[0] != color:
                            moves.append((r, c))
                        break
        
        elif type in ['bishop', 'queen']:
            # Diagonal moves
            for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                for i in range(1, 8):
                    r, c = row + dr*i, col + dc*i
                    if not (0 <= r < 8 and 0 <= c < 8):
                        break
                    target = self.board[r][c]
                    if not target:
                        moves.append((r, c))
                    else:
                        if target[0] != color:
                            moves.append((r, c))
                        break
        
        elif type == 'knight':
            # Knight moves
            for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), 
                          (1,-2), (1,2), (2,-1), (2,1)]:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = self.board[r][c]
                    if not target or target[0] != color:
                        moves.append((r, c))
        
        elif type == 'king':
            # King moves
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < 8 and 0 <= c < 8:
                        target = self.board[r][c]
                        if not target or target[0] != color:
                            moves.append((r, c))
        
        return moves
    
    def handle_click(self, pos):
        """Handle mouse clicks on the game board"""
        x, y = pos
        if not (MARGIN <= x < MARGIN + 8*SQUARE_SIZE and 
                MARGIN <= y < MARGIN + 8*SQUARE_SIZE):
            return
        
        col = (x - MARGIN) // SQUARE_SIZE
        row = (y - MARGIN) // SQUARE_SIZE
        
        # If no square is selected
        if self.selected_square is None:
            piece = self.board[row][col]
            if piece and piece[0] == self.current_player:
                self.selected_square = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)
        
        # If a square is already selected
        else:
            selected_row, selected_col = self.selected_square
            
            # Clicked on same square - deselect
            if (row, col) == self.selected_square:
                self.selected_square = None
                self.valid_moves = []
            
            # Clicked on valid move
            elif (row, col) in self.valid_moves:
                # Save current state for undo
                self.move_history.append((self.selected_square, (row, col)))
                self.history_index += 1
                
                # Move the piece
                self.board[row][col] = self.board[selected_row][selected_col]
                self.board[selected_row][selected_col] = None
                
                # Save new board state
                self.board_history = self.board_history[:self.history_index+1]
                self.board_history.append(self.copy_board())
                
                # Switch player
                self.current_player = 'black' if self.current_player == 'white' else 'white'
                self.selected_square = None
                self.valid_moves = []
            
            # Clicked on another piece of current player
            else:
                piece = self.board[row][col]
                if piece and piece[0] == self.current_player:
                    self.selected_square = (row, col)
                    self.valid_moves = self.get_valid_moves(row, col)
    
    def undo_move(self):
        """Undo the last move"""
        if self.history_index >= 0:
            self.history_index -= 1
            self.board = [row.copy() for row in self.board_history[self.history_index]]
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            self.selected_square = None
            self.valid_moves = []
    
    def redo_move(self):
        """Redo the last undone move"""
        if self.history_index < len(self.board_history) - 1:
            self.history_index += 1
            self.board = [row.copy() for row in self.board_history[self.history_index]]
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            self.selected_square = None
            self.valid_moves = []
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if self.state == "main_menu":
                        # Check menu options
                        if 250 <= pos[1] <= 300:  # New Game
                            if WIDTH//2 - 100 <= pos[0] <= WIDTH//2 + 100:
                                self.__init__()  # Reset game
                                self.state = "game"
                        elif 330 <= pos[1] <= 380:  # Quit
                            if WIDTH//2 - 100 <= pos[0] <= WIDTH//2 + 100:
                                pygame.quit()
                                sys.exit()
                    
                    elif self.state == "theme_menu":
                        # Check theme selection
                        for i, theme in enumerate(THEMES.keys()):
                            col = 0 if i < len(THEMES)//2 else 1
                            row = i if i < len(THEMES)//2 else i - len(THEMES)//2
                            x = 20 + col * (WIDTH//2 - 10)
                            y = 80 + row * 40
                            
                            if (x <= pos[0] <= x + WIDTH//2 - 30 and 
                                y <= pos[1] <= y + 30):
                                self.current_theme = theme
                        
                        # Check back button
                        if (20 <= pos[0] <= 120 and 
                            HEIGHT - 60 <= pos[1] <= HEIGHT - 20):
                            self.state = "game"
                    
                    elif self.state == "game":
                        # Check if clicked on game board
                        if (MARGIN <= pos[0] < MARGIN + 8*SQUARE_SIZE and 
                            MARGIN <= pos[1] < MARGIN + 8*SQUARE_SIZE):
                            self.handle_click(pos)
                        
                        # Check undo button
                        elif (WIDTH - 220 <= pos[0] <= WIDTH - 140 and 
                              HEIGHT - 35 <= pos[1] <= HEIGHT - 5):
                            self.undo_move()
                        
                        # Check redo button
                        elif (WIDTH - 120 <= pos[0] <= WIDTH - 40 and 
                              HEIGHT - 35 <= pos[1] <= HEIGHT - 5):
                            self.redo_move()
                        
                        # Check theme button
                        elif (WIDTH - 350 <= pos[0] <= WIDTH - 240 and 
                              HEIGHT - 35 <= pos[1] <= HEIGHT - 5):
                            self.state = "theme_menu"
            
            # Draw current state
            if self.state == "main_menu":
                self.draw_main_menu()
            elif self.state == "theme_menu":
                self.draw_theme_menu()
            elif self.state == "game":
                self.draw_game()
            
            clock.tick(60)

if __name__ == "__main__":
    game = MiniChess()
    game.run()