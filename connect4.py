import numpy as np

ROW_COUNT = 5
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

board = create_board()
print(board)
game_over = False
turn = 0

while not game_over:
    #P1 Input
    if turn == 0:
        col = int(input("Player 1, make your move (0-6): "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)




    #P2 Input
    else:
        col = int((input("Player 2, make your move (0-6): ")))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

    print(board)
    turn += 1
    turn %= 2
