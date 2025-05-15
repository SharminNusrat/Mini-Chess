import copy
from board import ChessBoard

PIECE_VALUES = {
    'pawn': 10,
    'knight': 30,
    'bishop': 30,
    'rook': 50,
    'queen': 90,
    'king': 1000
}

PIECE_ORDER = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
OPTIMIZED_WEIGHTS = None

CENTER_SQUARES = {(2, 2), (2, 3), (3, 2), (3, 3)}

def evaluate_board(board, current_turn):
    """Calculates a score for the board and current player."""
    score = 0
    opponent = 'black' if current_turn == 'white' else 'white'

    for r in range(len(board)):
        for c in range(len(board[0])):
            piece = board[r][c]
            if not piece:
                continue
            color, ptype = piece
            value = PIECE_VALUES.get(ptype, 0)

            if color == current_turn:
                score += value
                if (r, c) in CENTER_SQUARES:
                    score += 3
            else:
                score -= value
                if (r, c) in CENTER_SQUARES:
                    score -= 3

    # Mobility
    my_moves = count_all_moves(board, current_turn)
    opponent_moves = count_all_moves(board, opponent)
    score += 0.1 * (my_moves - opponent_moves)

    # King safety: small bonus for having king on back
    for r in range(len(board)):
        for c in range(len(board[0])):
            piece = board[r][c]
            if piece and piece[0] == current_turn and piece[1] == 'king':
                if (current_turn == 'white' and r == 4) or (current_turn == 'black' and r == 0):
                    score += 5
                break

    return score

def count_all_moves(board, color):
    """Counts all possible moves for a specific player."""
    temp_cb = ChessBoard()
    temp_cb.board = copy.deepcopy(board)
    temp_cb.current_turn = color

    count = 0
    for r in range(5):
        for c in range(6):
            piece = temp_cb.get_piece(r, c)
            if piece and piece[0] == color:
                moves = temp_cb.get_valid_moves(r, c)
                count += len(moves)
    return count

def get_all_possible_moves(board, current_turn):
    """Returns all possible moves for the current player."""
    cb = ChessBoard()
    cb.board = copy.deepcopy(board)
    cb.current_turn = current_turn
    
    possible_moves = []
    for r in range(5):
        for c in range(6):
            piece = cb.get_piece(r, c)
            if piece and piece[0] == current_turn:
                moves = cb.get_valid_moves(r, c)
                for move in moves:
                    possible_moves.append(((r, c), move))
    
    return possible_moves

def make_move(board, current_turn, from_sq, to_sq):
    """Makes a move and returns the updated board."""
    cb = ChessBoard()
    cb.board = copy.deepcopy(board)
    cb.current_turn = current_turn
    cb.move_piece(from_sq, to_sq)
    return cb.board

def minimax(board, depth, maximizing, current_turn, weights=None):
    """Minimax algorithm - calculates the best move for the board."""
    if depth == 0:
        return evaluate_board(board, current_turn), None

    possible_moves = get_all_possible_moves(board, current_turn)
    
    if not possible_moves:
        return evaluate_board(board, current_turn), None

    next_turn = 'black' if current_turn == 'white' else 'white'
    best_move = None

    if maximizing:
        best_score = float('-inf')
        
        for (from_sq, to_sq) in possible_moves:
            new_board = make_move(board, current_turn, from_sq, to_sq)
            score, _ = minimax(new_board, depth - 1, False, next_turn)
            
            if score > best_score:
                best_score = score
                best_move = (from_sq, to_sq)
    else:
        best_score = float('inf')
        
        for (from_sq, to_sq) in possible_moves:
            new_board = make_move(board, current_turn, from_sq, to_sq)
            score, _ = minimax(new_board, depth - 1, True, next_turn)
            
            if score < best_score:
                best_score = score
                best_move = (from_sq, to_sq)

    return best_score, best_move

def get_ai_move(board, current_turn, depth=5, weights=None):
    """Returns the best move for the AI."""
    _, move = minimax(board, depth, True, current_turn, weights)
    return move
