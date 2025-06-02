def check_winner(board):
    """
    Check if there's a winner on the board.
    Returns 'X', 'O', or None
    """
    # Winning combinations (indices)
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for combo in winning_combinations:
        if (board[combo[0]] != "" and 
            board[combo[0]] == board[combo[1]] == board[combo[2]]):
            return board[combo[0]]
    
    return None

def is_draw(board):
    """
    Check if the game is a draw (board full, no winner).
    """
    return all(cell != "" for cell in board) and check_winner(board) is None

def is_valid_move(board, index):
    """
    Check if a move is valid.
    """
    if index < 0 or index > 8:
        return False
    return board[index] == ""

def get_available_moves(board):
    """
    Get list of available move indices.
    """
    return [i for i, cell in enumerate(board) if cell == ""]
