def get_valid_moves(board, row, col):
    piece = board[row][col]
    if not piece:
        return []

    color, type = piece
    moves = []

    if type == 'pawn':
        direction = -1 if color == 'white' else 1
        if 0 <= row + direction < 6 and not board[row + direction][col]:
            moves.append((row + direction, col))
        for dc in [-1, 1]:
            if 0 <= col + dc < 5 and 0 <= row + direction < 6:
                target = board[row + direction][col + dc]
                if target and target[0] != color:
                    moves.append((row + direction, col + dc))

    elif type in ['rook', 'queen']:
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            for i in range(1, max(6, 5)):
                r, c = row + dr*i, col + dc*i
                if not (0 <= r < 6 and 0 <= c < 5):
                    break
                target = board[r][c]
                if not target:
                    moves.append((r, c))
                elif target[0] != color:
                    moves.append((r, c))
                    break
                else:
                    break
    
    return moves
