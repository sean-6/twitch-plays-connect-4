import numpy as np


def create_board():
    board = np.zeros((6,7))
    return board

board = create_board()
game_over = False
turn = 0

while not game_over:
    #P1 Input
    if turn == 0:
        selection = int(input("Player 1, make your move (0-6): "))

    

    #P2 Input
    else:
        selection = int((input("Player 2, make your move (0-6): ")))
    
    turn += 1
    turn %= 2