import pygame
import sys
from pygame.locals import *
from constants import *
from board import ChessBoard
from ui import UI

class MiniChess5x6:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ChessChamp")
        
        # Game state
        self.state = MAIN_MENU
        self.current_theme = "Classic Wood"
        self.current_player = "white"
        self.selected_square = None
        self.valid_moves = []
        
        # History for undo/redo
        self.move_history = []
        self.history_index = -1
        
        # Create board and UI
        self.chess_board = ChessBoard()
        self.ui = UI(self.screen)
        
        # Board history for undo/redo
        self.board_history = [self.chess_board.copy_board()]
    
    def handle_click(self, pos):
        """Handle mouse clicks on the game board"""
        x, y = pos
        if not (MARGIN_X <= x < MARGIN_X + COLS*SQUARE_SIZE and 
                MARGIN_Y <= y < MARGIN_Y + ROWS*SQUARE_SIZE):
            return
        
        col = (x - MARGIN_X) // SQUARE_SIZE
        row = (y - MARGIN_Y) // SQUARE_SIZE
        
        # If no square is selected
        if self.selected_square is None:
            piece = self.chess_board.get_piece(row, col)
            if piece and piece[0] == self.current_player:
                self.selected_square = (row, col)
                self.valid_moves = self.chess_board.get_valid_moves(row, col)
        
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
                self.chess_board.move_piece(self.selected_square, (row, col))
                
                # Save new board state
                self.board_history = self.board_history[:self.history_index+1]
                self.board_history.append(self.chess_board.copy_board())
                
                # Switch player
                self.current_player = 'black' if self.current_player == 'white' else 'white'
                self.selected_square = None
                self.valid_moves = []
            
            # Clicked on another piece of current player
            else:
                piece = self.chess_board.get_piece(row, col)
                if piece and piece[0] == self.current_player:
                    self.selected_square = (row, col)
                    self.valid_moves = self.chess_board.get_valid_moves(row, col)
    
    def undo_move(self):
        """Undo the last move"""
        if self.history_index >= 0:
            self.history_index -= 1
            self.chess_board.board = [row.copy() for row in self.board_history[self.history_index]]
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            self.selected_square = None
            self.valid_moves = []
    
    def redo_move(self):
        """Redo the last undone move"""
        if self.history_index < len(self.board_history) - 1:
            self.history_index += 1
            self.chess_board.board = [row.copy() for row in self.board_history[self.history_index]]
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
                    
                    if self.state == MAIN_MENU:
                        action = self.ui.check_main_menu_click(pos)
                        if action == "new_game":
                            self.__init__()  # Reset game
                            self.state = GAME
                        elif action == "quit":
                            pygame.quit()
                            sys.exit()
                    
                    elif self.state == THEME_MENU:
                        result = self.ui.check_theme_menu_click(pos)
                        if result == "back":
                            self.state = GAME
                        elif result:  # A theme was selected
                            self.current_theme = result
                    
                    elif self.state == GAME:
                        # Check if clicked on game board
                        if (MARGIN_X <= pos[0] < MARGIN_X + COLS*SQUARE_SIZE and 
                            MARGIN_Y <= pos[1] < MARGIN_Y + ROWS*SQUARE_SIZE):
                            self.handle_click(pos)
                        
                        # Check undo/redo/theme buttons
                        undo_rect, redo_rect, theme_rect = self.ui.draw_game(
                            self.chess_board.board, 
                            self.current_theme, 
                            self.current_player, 
                            self.selected_square, 
                            self.valid_moves
                        )
                        
                        if undo_rect.collidepoint(pos):
                            self.undo_move()
                        elif redo_rect.collidepoint(pos):
                            self.redo_move()
                        elif theme_rect.collidepoint(pos):
                            self.state = THEME_MENU
            
            # Draw current state
            if self.state == MAIN_MENU:
                self.ui.draw_main_menu()
            elif self.state == THEME_MENU:
                self.ui.draw_theme_menu(self.current_theme)
            elif self.state == GAME:
                self.ui.draw_game(
                    self.chess_board.board, 
                    self.current_theme, 
                    self.current_player, 
                    self.selected_square, 
                    self.valid_moves
                )
            
            clock.tick(60)