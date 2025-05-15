from copy import deepcopy
from constants import COLS, ROWS

class MiniChessAI:
    def __init__(self, depth=3):
        self.depth = depth
        self.piece_values = {
            'pawn': 100,
            'knight': 320,
            'bishop': 330,
            'rook': 500,
            'queen': 900,
            'king': 20000
        }

    def evaluate_board(self, board, color):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece:
                    value = self.piece_values.get(piece[1], 0)
                    if piece[0] == color:
                        score += value  
                    else:
                        score -= value  
        
        center = [(2, 2), (2, 3), (3, 2), (3, 3)]
        for (r, c) in center:
            piece = board[r][c]
            if piece and piece[0] == color:
                score += 50
            elif piece and piece[0] != color:
                score -= 50
        
        return score

    def minimax(self, board, depth, maximizing_player, current_color):
        if depth == 0 or board.is_checkmate(current_color) or board.is_stalemate(current_color):
            return self.evaluate_board(board.board, current_color)
            
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_all_moves(board, current_color):
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])
                eval = self.minimax(new_board, depth-1, False, current_color)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            opponent_color = 'black' if current_color == 'white' else 'white'
            for move in self.get_all_moves(board, opponent_color):
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])
                eval = self.minimax(new_board, depth-1, True, current_color)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_all_moves(self, board, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece and piece[0] == color:
                    valid_moves = board.get_valid_moves(row, col)
                    for move in valid_moves:
                        moves.append(((row, col), move))
        return moves

    def get_best_move(self, board, current_color):
        best_move = None
        best_eval = float('-inf')
        
        for move in self.get_all_moves(board, current_color):
            new_board = deepcopy(board)
            new_board.move_piece(move[0], move[1])
            current_eval = self.minimax(new_board, self.depth-1, False, current_color)
            
            if current_eval > best_eval:
                best_eval = current_eval
                best_move = move
                
        return best_move