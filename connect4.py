import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board():
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Verticals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Positive Diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Negative diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE/2, (r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE+SQUARESIZE/2, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (c*SQUARESIZE+SQUARESIZE/2, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
                
# Starting program
board = create_board()
print_board()
game_over = True
turn = 0

pygame.init()
myfont = pygame.font.SysFont("arial", 75)

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE # Can take out +1 later
size = (width , height)
RADIUS = int(SQUARESIZE/2 -5)

screen = pygame.display.set_mode(size)

# draw_board(board)
# pygame.display.update()

def loadGame():
    draw_board(board)
    pygame.display.update()

turn = 0

def chooseLocation(col):
    global turn
    if turn == 0:
        # GETTING MOUSE CLICK, NOT IMPORTANT FOR FINAL PROJ
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
                    
            if winning_move(board, 1):
                label = myfont.render("Player 1 wins!", 1, RED)
                screen.blit(label, (40,10))
                return True

            # #P2 Input
    else:
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                label = myfont.render("Player 1 wins!", 1, RED)
                screen.blit(label)
                return True
                
                
    print_board()
    draw_board(board)
    turn += 1
    turn %= 2
    







def play_round():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            #P1 Input




            if game_over:
                pygame.time.wait(3000)









































# while not game_over:

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             # print(event.pos)
#             #P1 Input
#             if turn == 0:
#                 # GETTING MOUSE CLICK, NOT IMPORTANT FOR FINAL PROJ
#                 posx = event.pos[0]
#                 col = int(math.floor(posx/SQUARESIZE))

#                 if is_valid_location(board, col):
#                     row = get_next_open_row(board, col)
#                     drop_piece(board, row, col, 1)
                    
#                     if winning_move(board, 1):
#                         label = myfont.render("Player 1 wins!", 1, RED)
#                         screen.blit(label, (40,10))
#                         game_over = True

#             # #P2 Input
#             else:
#                 posx = event.pos[0]
#                 col = int(math.floor(posx/SQUARESIZE))

#                 if is_valid_location(board, col):
#                     row = get_next_open_row(board, col)
#                     drop_piece(board, row, col, 2)

#                     if winning_move(board, 2):
#                         label = myfont.render("Player 1 wins!", 1, RED)
#                         screen.blit(label)
#                         game_over = True

#             print_board()
#             draw_board(board)
#             turn += 1
#             turn %= 2

#             if game_over:
#                 pygame.time.wait(3000)
