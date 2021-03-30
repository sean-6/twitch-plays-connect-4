from time import sleep
from typing import ValuesView

from pygame.event import get
import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 1
AI_PIECE = 2

EMPTY = 0
WINDOW_LENGTH = 4


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

def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    if window.couint(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 5

    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 8

    return score

def score_position(board, piece):
    # Horizontal scores
    score = 0

    # Score centre column
    centre_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    centre_count = centre_array.count(piece)
    score += centre_count * 6

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

    # Vertical score
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positive sloped diagonal score
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range[WINDOW_LENGTH]]
            score += evaluate_window(window, piece)

    # Negative sloped
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximisingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else: # Game over
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))

    if maximisingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, AI_PIECE)
            new_score = minimax(board_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
            return column, value
    
    else: # Minimising player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, PLAYER_PIECE)
            new_score = minimax(board_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
            return column, value
    


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    best_score = 0
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)

        if score > best_score:
            best_score = score
            best_col = col

    return best_col



def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE/2, (r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE+SQUARESIZE/2, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
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


def chooseLocation(col):
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, PLAYER_PIECE)
                
        if winning_move(board, PLAYER_PIECE):
            label = myfont.render("Player 1 wins!", 1, RED)
            screen.blit(label, (40,10))
            return True
                
    print_board()
    draw_board(board)

    if ai_drop():
        return True
    
def ai_drop():
    sleep(5)
    col = minimax(board, 2, True)

    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)
                
        if winning_move(board, AI_PIECE):
            label = myfont.render("Player 2 wins!", 1, RED)
            screen.blit(label, (40,10))
            return True

    print_board()
    draw_board(board)






def play_round():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()




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
