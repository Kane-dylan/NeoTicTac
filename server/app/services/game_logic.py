def check_winner(board):
    win_patterns = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for pattern in win_patterns:
        a, b, c = pattern
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None

def is_draw(board):
    return all(cell != "" for cell in board)
