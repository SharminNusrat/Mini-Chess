from copy import deepcopy
from constants import COLS, ROWS
from board import ChessBoard
import time

CENTER_SQUARES = {(2, 2), (2, 3), (3, 2), (3, 3)}

class MiniChessAI:
    def __init__(self, depth=3):
        self.max_depth = depth  
        self.piece_values = {
            'pawn': 100,
            'knight': 320,
            'bishop': 330,
            'rook': 500,
            'queen': 900,
            'king': 20000
        }
        self.time_limit = 1.0 
        self.nodes_evaluated = 0

    def evaluate_board(self, board, current_turn, move_made=None):
        if isinstance(board, list):
            temp_board = ChessBoard()
            temp_board.board = board  
            board = temp_board

        score = 0
        opponent = 'black' if current_turn == 'white' else 'white'

       
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece:
                    value = self.piece_values.get(piece[1], 0)
                    if piece[0] == current_turn:
                        score += value
                    else:
                        score -= value

        
        for (r, c) in CENTER_SQUARES:
            piece = board.get_piece(r, c)
            if piece and piece[0] == current_turn:
                score += 50
            elif piece and piece[0] != current_turn:
                score -= 50

       
        my_moves = len(self.get_all_moves(board, current_turn))
        opponent_moves = len(self.get_all_moves(board, opponent))
        score += 0.1 * (my_moves - opponent_moves)

        
        king_pos = self._find_king(board, current_turn)
        if king_pos:
            if current_turn == 'white' and king_pos[0] == 5:  # White king in back rank
                score += 20
            elif current_turn == 'black' and king_pos[0] == 0:  # Black king in back rank
                score += 20

       
        if move_made:
            from_sq, to_sq = move_made
            piece = board[to_sq[0]][to_sq[1]]
            if piece and piece[0] == current_turn:
                vulnerability = self._get_post_move_vulnerability(board, to_sq, current_turn)
                aggression = self._get_proximity_to_threats(board, to_sq, opponent)
                score += aggression * 0.5  
                score -= vulnerability * 1.0  

        return score

    def _find_king(self, board, color):
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece and piece[0] == color and piece[1] == 'king':
                    return (row, col)
        return None

    def _get_post_move_vulnerability(self, board, pos, color):
        opponent = 'black' if color == 'white' else 'white'
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece and piece[0] == opponent:
                    moves = self._get_possible_moves(board, row, col, opponent, piece[1])
                    if pos in moves:
                        return 1  
        return 0

    def _get_proximity_to_threats(self, board, pos, opponent_color):
        r0, c0 = pos
        proximity_score = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if piece and piece[0] == opponent_color:
                    distance = abs(row - r0) + abs(col - c0)
                    if distance <= 2:  
                        proximity_score += self.piece_values.get(piece[1], 0) / (distance + 1)
        return proximity_score

    def minimax(self, board, depth, maximizing_player, current_color, alpha=float('-inf'), beta=float('inf')):
        self.nodes_evaluated += 1
        
        if depth == 0 or board.is_checkmate(current_color) or board.is_stalemate(current_color):
            return self.evaluate_board(board.board, current_color)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_all_moves(board, current_color):
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])
                eval = self.minimax(new_board, depth-1, False, current_color, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent_color = 'black' if current_color == 'white' else 'white'
            for move in self.get_all_moves(board, opponent_color):
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])
                eval = self.minimax(new_board, depth-1, True, current_color, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_all_moves(self, board, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = board.get_piece(row, col)
                if piece and piece[0] == color:
                    possible_moves = board._get_possible_moves(row, col, piece[0], piece[1])
                    for move in possible_moves:
                        if not board._would_be_in_check(piece[0], (row, col), move):
                            moves.append(((row, col), move))
        return moves

    def get_best_move(self, board, current_color):
        """Use IDDFS with minimax and alpha-beta pruning to find the best move"""
        best_move = None
        best_eval = float('-inf')
        start_time = time.time()
        
        
        for depth in range(1, self.max_depth + 1):
            if time.time() - start_time > self.time_limit:
                break  
                
            current_best_move = None
            current_best_eval = float('-inf')
            alpha = float('-inf')
            beta = float('inf')
            
          
            for move in self.get_all_moves(board, current_color):
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1])
                
               
                eval = self.minimax(
                    new_board, 
                    depth - 1, 
                    False,
                    current_color,
                    alpha,
                    beta
                )
                
                if eval > current_best_eval:
                    current_best_eval = eval
                    current_best_move = move
                    alpha = max(alpha, eval)
            
           
            if time.time() - start_time <= self.time_limit:
                best_move = current_best_move
                best_eval = current_best_eval
            else:
                break
        
        return best_move