from constants import COLS, ROWS

class ChessBoard:
    def __init__(self):
        self.board = self.setup_board()
    
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
        return self.board[row][col]
    
    def set_piece(self, row, col, piece):
        """Set a piece at the specified position"""
        self.board[row][col] = piece
    
    def move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None
    
    def get_valid_moves(self, row, col):
        """Get valid moves for the piece at (row, col)"""
        piece = self.board[row][col]
        if not piece:
            return []
        
        color, type = piece
        moves = []
        
        if type == 'pawn':
            direction = -1 if color == 'white' else 1
            # Forward move
            if 0 <= row + direction < ROWS and not self.board[row + direction][col]:
                moves.append((row + direction, col))
            # Captures
            for dc in [-1, 1]:
                if 0 <= col + dc < COLS and 0 <= row + direction < ROWS:
                    target = self.board[row + direction][col + dc]
                    if target and target[0] != color:
                        moves.append((row + direction, col + dc))
        
        elif type in ['rook', 'queen']:
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
        
        elif type in ['bishop', 'queen']:
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
        
        elif type == 'knight':
            # Knight moves
            for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), 
                          (1,-2), (1,2), (2,-1), (2,1)]:
                r, c = row + dr, col + dc
                if 0 <= r < ROWS and 0 <= c < COLS:
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
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        target = self.board[r][c]
                        if not target or target[0] != color:
                            moves.append((r, c))
        
        return moves