from constants import COLS, ROWS, PIECES

class ChessBoard:
    def __init__(self):
        self.board = self.setup_board()
        self.move_history = []
        self.current_turn = 'white'
        self.last_moved_piece = None
        self.game_over = False
        self.winner = None
    
    def setup_board(self):
        """Initialize the 5x6 chess board with pieces"""
        board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        # Pawns
        for col in range(COLS):
            board[1][col] = ('black', 'pawn')
            board[4][col] = ('white', 'pawn')
        
        # Other pieces (simplified setup for 5x6)
        back_row = ['rook', 'knight', 'bishop', 'queen', 'king']
        for col, piece in enumerate(back_row[:COLS]):
            board[0][col] = ('black', piece)
            board[5][col] = ('white', piece)
            
        return board
    
    def copy_board(self):
        """Create a deep copy of the current board state"""
        return [row.copy() for row in self.board]
    
    def get_piece(self, row, col):
        """Get the piece at the specified position"""
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None
    
    def set_piece(self, row, col, piece):
        """Set a piece at the specified position"""
        self.board[row][col] = piece
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        moved_piece = self.board[from_row][from_col]
        captured_piece = self.board[to_row][to_col]
        
        # Check if the move would put own king in check
        color = moved_piece[0] if moved_piece else None
        if color and self._would_be_in_check(color, from_pos, to_pos):
            return False
            
        # Save move to history for undo/redo
        self.move_history.append({
            'from': from_pos,
            'to': to_pos,
            'piece': moved_piece,
            'captured': captured_piece
        })
        
        # Move piece
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
        
        # Store the last moved piece for highlighting
        self.last_moved_piece = to_pos
        
        # Switch turns
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        # Check for checkmate or stalemate after the move
        self.check_game_end_conditions()
        
        return True
    
    def undo_move(self):
        """Undo the last move if available"""
        if not self.move_history:
            return False
            
        move = self.move_history.pop()
        from_pos = move['from']
        to_pos = move['to']
        captured = move['captured']
        
        # Restore the pieces
        self.board[from_pos[0]][from_pos[1]] = self.board[to_pos[0]][to_pos[1]]
        self.board[to_pos[0]][to_pos[1]] = captured
        
        # Restore the turn
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        
        # Reset game over state if needed
        if self.game_over:
            self.game_over = False
            self.winner = None
            
        return True
    
    def get_valid_moves(self, row, col):
        """Get valid moves for the piece at (row, col)"""
        piece = self.board[row][col]
        if not piece:
            return []
        
        color, piece_type = piece
        possible_moves = self._get_possible_moves(row, col, color, piece_type)
        
        # Filter moves that would leave the king in check
        legal_moves = []
        for move in possible_moves:
            if not self._would_be_in_check(color, (row, col), move):
                legal_moves.append(move)
                
        return legal_moves
    
    def _get_possible_moves(self, row, col, color, piece_type):
        """Get all possible moves without considering check"""
        moves = []
        
        if piece_type == 'pawn':
            direction = -1 if color == 'white' else 1
            # Forward move
            new_row = row + direction
            if 0 <= new_row < ROWS and not self.board[new_row][col]:
                moves.append((new_row, col))
            
            # Captures
            for dc in [-1, 1]:
                new_col = col + dc
                if 0 <= new_col < COLS and 0 <= new_row < ROWS:
                    target = self.board[new_row][new_col]
                    if target and target[0] != color:
                        moves.append((new_row, new_col))
        
        elif piece_type == 'rook':
            # Horizontal and vertical moves
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                for i in range(1, max(ROWS, COLS)):
                    r, c = row + dr*i, col + dc*i
                    if not (0 <= r < ROWS and 0 <= c < COLS):
                        break
                    target = self.board[r][c]
                    if not target:
                        moves.append((r, c))
                    else:
                        if target[0] != color:
                            moves.append((r, c))
                        break
        
        elif piece_type == 'bishop':
            # Diagonal moves
            for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                for i in range(1, max(ROWS, COLS)):
                    r, c = row + dr*i, col + dc*i
                    if not (0 <= r < ROWS and 0 <= c < COLS):
                        break
                    target = self.board[r][c]
                    if not target:
                        moves.append((r, c))
                    else:
                        if target[0] != color:
                            moves.append((r, c))
                        break
                        
        elif piece_type == 'queen':
            # Combined rook and bishop moves
            # Horizontal and vertical moves (rook-like)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                for i in range(1, max(ROWS, COLS)):
                    r, c = row + dr*i, col + dc*i
                    if not (0 <= r < ROWS and 0 <= c < COLS):
                        break
                    target = self.board[r][c]
                    if not target:
                        moves.append((r, c))
                    else:
                        if target[0] != color:
                            moves.append((r, c))
                        break
            
            # Diagonal moves (bishop-like)
            for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                for i in range(1, max(ROWS, COLS)):
                    r, c = row + dr*i, col + dc*i
                    if not (0 <= r < ROWS and 0 <= c < COLS):
                        break
                    target = self.board[r][c]
                    if not target:
                        moves.append((r, c))
                    else:
                        if target[0] != color:
                            moves.append((r, c))
                        break
        
        elif piece_type == 'knight':
            # Knight moves
            for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), 
                          (1,-2), (1,2), (2,-1), (2,1)]:
                r, c = row + dr, col + dc
                if 0 <= r < ROWS and 0 <= c < COLS:
                    target = self.board[r][c]
                    if not target or target[0] != color:
                        moves.append((r, c))
        
        elif piece_type == 'king':
            # King moves
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        target = self.board[r][c]
                        if not target or target[0] != color:
                            moves.append((r, c))
        
        return moves
    
    def _find_king(self, color):
        """Find the position of the king of the specified color"""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece[0] == color and piece[1] == 'king':
                    return (row, col)
        return None
    
    def is_in_check(self, color):
        """Determine if the specified color's king is in check."""
        # Find king position
        king_pos = self._find_king(color)
        if not king_pos:
            return False  # Should not happen in a valid game

        # Check if any opponent piece can capture the king
        opponent_color = 'black' if color == 'white' else 'white'
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece[0] == opponent_color:
                    moves = self._get_possible_moves(row, col, opponent_color, piece[1])
                    if king_pos in moves:
                        return True
        return False
    
    def _would_be_in_check(self, color, from_pos, to_pos):
        """Check if making a move would result in check."""
        # Save current state
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        moved_piece = self.board[from_row][from_col]
        captured_piece = self.board[to_row][to_col]
        
        # Make temporary move
        self.board[to_row][to_col] = moved_piece
        self.board[from_row][from_col] = None
        
        # Check if king is in check
        in_check = self.is_in_check(color)
        
        # Restore board
        self.board[from_row][from_col] = moved_piece
        self.board[to_row][to_col] = captured_piece
        
        return in_check
    
    def has_legal_moves(self, color):
        """Check if the specified color has any legal moves"""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece[0] == color:
                    if self.get_valid_moves(row, col):
                        return True
        return False
    
    def is_checkmate(self, color):
        """Determine if the specified color is in checkmate."""
        if not self.is_in_check(color):
            return False
            
        # Check if any legal moves are available
        return not self.has_legal_moves(color)
    
    def is_stalemate(self, color):
        """Determine if the specified color is in stalemate."""
        if self.is_in_check(color):
            return False
            
        # Check if any legal moves are available
        return not self.has_legal_moves(color)
    
    def check_game_end_conditions(self):
        """Check if the game has ended (checkmate or stalemate)"""
        # Check for current player (not opponent) since we need to check if the player who's about to move is in checkmate
        current_player = self.current_turn
        
        if self.is_checkmate(current_player):
            self.game_over = True
            self.winner = 'black' if current_player == 'white' else 'white'
            return True
            
        if self.is_stalemate(current_player):
            self.game_over = True
            self.winner = 'draw'
            return True
            
        return False
    
    def get_game_status(self):
        """Get the current state of the game."""
        # Check for game over conditions first
        if self.is_checkmate(self.current_turn):
            opponent = 'black' if self.current_turn == 'white' else 'white'
            self.game_over = True
            self.winner = opponent
            return f"Game Over - {opponent.capitalize()} wins by checkmate"
            
        if self.is_stalemate(self.current_turn):
            self.game_over = True
            self.winner = 'draw'
            return "Game Over - Draw by stalemate"
            
        # If game is already marked as over
        if self.game_over:
            if self.winner == 'draw':
                return "Game Over - Draw by stalemate"
            else:
                return f"Game Over - {self.winner.capitalize()} wins by checkmate"
        
        # Normal gameplay status
        if self.is_in_check(self.current_turn):
            return f"{self.current_turn.capitalize()} is in check"
            
        return f"{self.current_turn.capitalize()}'s turn"
        
    def display(self):
        """Display the current state of the board."""
        piece_symbols = {
            'pawn': 'P', 'rook': 'R', 'knight': 'N',
            'bishop': 'B', 'queen': 'Q', 'king': 'K'
        }
        
        print('\n  a b c d e')
        print('  ---------')
        for row in range(ROWS-1, -1, -1):
            row_str = f"{row+1}|"
            for col in range(COLS):
                piece = self.board[row][col]
                if piece is None:
                    row_str += ' .'
                else:
                    color, piece_type = piece
                    symbol = piece_symbols[piece_type]
                    if color == 'black':
                        symbol = symbol.lower()
                    row_str += f' {symbol}'
            print(row_str)
        print(f"\n{self.get_game_status()}")