import pygame
import sys
import time
from pygame.locals import *
from constants import *
from board import ChessBoard
from ui import UI
from game_setup import GameSetupMenu

class MiniChess5x6:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ChessChamp")
        
        self.state = MAIN_MENU
        self.current_theme = "Classic Wood"
        self.selected_square = None
        self.valid_moves = []
        
        self.white_player = "human"
        self.black_player = "human"
        
        self.chess_board = ChessBoard()
        self.ui = UI(self.screen)
        self.setup_menu = GameSetupMenu(self.screen)
        
        self.board_history = [self.chess_board.copy_board()]
        self.history_index = 0
        
        self.clock = pygame.time.Clock()
        
        self.ai_think_time = 1.0  
        self.ai_last_move_time = 0
    
    def handle_click(self, pos):
        """Handle mouse clicks on the game board"""
        if self.chess_board.game_over:
            return
            
        x, y = pos
        if not (MARGIN_X <= x < MARGIN_X + COLS*SQUARE_SIZE and 
                MARGIN_Y <= y < MARGIN_Y + ROWS*SQUARE_SIZE):
            return
        
        col = (x - MARGIN_X) // SQUARE_SIZE
        row = (y - MARGIN_Y) // SQUARE_SIZE
        
        current_player_type = self.white_player if self.chess_board.current_turn == "white" else self.black_player
        if current_player_type == "ai":
            return
        
        if self.selected_square is None:
            piece = self.chess_board.get_piece(row, col)
            if piece and piece[0] == self.chess_board.current_turn:
                self.selected_square = (row, col)
                self.valid_moves = self.chess_board.get_valid_moves(row, col)
        
        else:
            selected_row, selected_col = self.selected_square
        
            if (row, col) == self.selected_square:
                self.selected_square = None
                self.valid_moves = []
            
            elif (row, col) in self.valid_moves:
                self.board_history = self.board_history[:self.history_index+1]
                
                self.chess_board.move_piece(self.selected_square, (row, col))
                
                self.board_history.append(self.chess_board.copy_board())
                self.history_index += 1
                
                self.selected_square = None
                self.valid_moves = []
                
                
                next_player_type = self.black_player if self.chess_board.current_turn == "black" else self.white_player
                if next_player_type == "ai" and not self.chess_board.game_over:
                    self.ai_last_move_time = time.time()
            
            
            else:
                piece = self.chess_board.get_piece(row, col)
                if piece and piece[0] == self.chess_board.current_turn:
                    self.selected_square = (row, col)
                    self.valid_moves = self.chess_board.get_valid_moves(row, col)
                else:
                    
                    self.selected_square = None
                    self.valid_moves = []
    
    def make_ai_move(self):
        """Make an AI move"""
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.chess_board.get_piece(row, col)
                if piece and piece[0] == self.chess_board.current_turn:
                    moves = self.chess_board.get_valid_moves(row, col)
                    if moves:
                        pieces.append((row, col, moves))
        
        if not pieces:
            return False  
            
        capture_moves = []
        check_moves = []
        safe_moves = []
        
        for row, col, moves in pieces:
            for move_row, move_col in moves:
                target = self.chess_board.get_piece(move_row, move_col)
                if target:
                    piece_value = self._get_piece_value(target[1])
                    capture_moves.append((piece_value, row, col, move_row, move_col))
                
                temp_board = [r.copy() for r in self.chess_board.board]
                temp_board[move_row][move_col] = temp_board[row][col]
                temp_board[row][col] = None
            
                opponent = 'white' if self.chess_board.current_turn == 'black' else 'black'
                king_pos = None
                for r in range(ROWS):
                    for c in range(COLS):
                        p = temp_board[r][c]
                        if p and p[0] == opponent and p[1] == 'king':
                            king_pos = (r, c)
                
                if king_pos:
                    is_check = False
                    for r in range(ROWS):
                        for c in range(COLS):
                            p = temp_board[r][c]
                            if p and p[0] == self.chess_board.current_turn:
                                if self._is_attacking(temp_board, r, c, p[1], king_pos[0], king_pos[1]):
                                    is_check = True
                    
                    if is_check:
                        check_moves.append((row, col, move_row, move_col))
                
                
                safe_moves.append((row, col, move_row, move_col))
        
        
        selected_move = None
        
        if check_moves:
            selected_move = check_moves[0]  
        elif capture_moves:
            
            capture_moves.sort(reverse=True)
            selected_move = capture_moves[0][1:]  
        elif safe_moves:
            selected_move = safe_moves[0]  
        
        if selected_move:
            from_row, from_col, to_row, to_col = selected_move
            
            self.board_history = self.board_history[:self.history_index+1]
            
            self.chess_board.move_piece((from_row, from_col), (to_row, to_col))
            
            self.board_history.append(self.chess_board.copy_board())
            self.history_index += 1
            
            return True
        
        return False
    
    def _get_piece_value(self, piece_type):
        """Get the value of a piece for AI evaluation"""
        values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 100  
        }
        return values.get(piece_type, 0)
    
    def _is_attacking(self, board, row, col, piece_type, target_row, target_col):
        """Check if a piece is attacking a target square"""
        if piece_type == 'pawn':
            direction = -1 if board[row][col][0] == 'white' else 1
            return (row + direction == target_row and 
                   (col - 1 == target_col or col + 1 == target_col))
        
        elif piece_type == 'knight':
            knight_moves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
            for dr, dc in knight_moves:
                if row + dr == target_row and col + dc == target_col:
                    return True
            return False
            
        elif piece_type in ['rook', 'queen']:
            if row == target_row:
                step = 1 if col < target_col else -1
                for c in range(col + step, target_col, step):
                    if board[row][c]:
                        return False
                return True
            if col == target_col:
                step = 1 if row < target_row else -1
                for r in range(row + step, target_row, step):
                    if board[r][col]:
                        return False
                return True
                
        if piece_type in ['bishop', 'queen']:
            if abs(row - target_row) == abs(col - target_col):
                step_row = 1 if row < target_row else -1
                step_col = 1 if col < target_col else -1
                r, c = row + step_row, col + step_col
                while r != target_row:
                    if board[r][c]:
                        return False
                    r += step_row
                    c += step_col
                return True
                
        if piece_type == 'king':
            return abs(row - target_row) <= 1 and abs(col - target_col) <= 1
            
        return False
    
    def undo_move(self):
        """Undo the last move"""
        if self.history_index > 0:
            self.history_index -= 1
            self.chess_board.board = [row.copy() for row in self.board_history[self.history_index]]
            self.chess_board.current_turn = 'black' if self.chess_board.current_turn == 'white' else 'white'
            self.chess_board.game_over = False
            self.chess_board.winner = None
            self.selected_square = None
            self.valid_moves = []
    
    def redo_move(self):
        """Redo the last undone move"""
        if self.history_index < len(self.board_history) - 1:
            self.history_index += 1
            self.chess_board.board = [row.copy() for row in self.board_history[self.history_index]]
            self.chess_board.current_turn = 'black' if self.chess_board.current_turn == 'white' else 'white'
            
            self.chess_board.check_game_end_conditions()
            
            self.selected_square = None
            self.valid_moves = []
    
    def reset_game(self):
        """Reset the game state but keep settings"""
        self.chess_board = ChessBoard()
        self.board_history = [self.chess_board.copy_board()]
        self.history_index = 0
        self.selected_square = None
        self.valid_moves = []
        
        
        if self.chess_board.current_turn == "black" and self.black_player == "ai":
            self.ai_last_move_time = time.time()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            current_time = time.time()
            
           
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    
                    if self.state == MAIN_MENU:
                        action = self.ui.check_main_menu_click(pos)
                        if action == "new_game":
                            self.state = SETUP_MENU
                        elif action == "quit":
                            running = False
                    
                    elif self.state == SETUP_MENU:
                        setup_result = self.setup_menu.handle_click(pos)
                        if setup_result:
                            self.white_player = setup_result["white_player"]
                            self.black_player = setup_result["black_player"]
                            self.reset_game()
                            self.state = GAME
                            if self.chess_board.current_turn == "white" and self.white_player == "ai":
                                self.ai_last_move_time = current_time
                    
                    elif self.state == THEME_MENU:
                        result = self.ui.check_theme_menu_click(pos)
                        if result == "back":
                            self.state = GAME
                        elif result:
                            self.current_theme = result
                    
                    elif self.state == GAME:
                        if self.chess_board.game_over:
                            game_over_action = self.ui.check_game_over_click(pos)
                            if game_over_action == "new_game":
                                self.state = SETUP_MENU
                            elif game_over_action == "quit":
                                running = False
                        else:
                            if (MARGIN_X <= pos[0] < MARGIN_X + COLS*SQUARE_SIZE and 
                                MARGIN_Y <= pos[1] < MARGIN_Y + ROWS*SQUARE_SIZE):
                                self.handle_click(pos)
                            
                            button_rects = self.ui.get_button_rects()
                            if "undo" in button_rects and button_rects["undo"].collidepoint(pos):
                                self.undo_move()
                            elif "redo" in button_rects and button_rects["redo"].collidepoint(pos):
                                self.redo_move()
                            elif "theme" in button_rects and button_rects["theme"].collidepoint(pos):
                                self.state = THEME_MENU
            
            
            if self.state == GAME and not self.chess_board.game_over:
                current_player_type = self.white_player if self.chess_board.current_turn == "white" else self.black_player
                if current_player_type == "ai" and current_time - self.ai_last_move_time >= self.ai_think_time:
                    self.make_ai_move()
                    self.ai_last_move_time = current_time
            
            
            if self.state == MAIN_MENU:
                self.ui.draw_main_menu()
            elif self.state == SETUP_MENU:
                self.setup_menu.draw()
            elif self.state == THEME_MENU:
                self.ui.draw_theme_menu(self.current_theme)
            elif self.state == GAME:
                self.ui.draw_game(
                    self.chess_board.board,
                    self.current_theme,
                    self.chess_board.current_turn,
                    self.selected_square,
                    self.valid_moves,
                    self.chess_board.game_over,
                    self.chess_board.winner
                )
            
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()