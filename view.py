import pygame
import pygame
import numpy as np

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 1
AI_PIECE = 2

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT) * SQUARESIZE # Can take out +1 later
size = (width , height)
RADIUS = int(SQUARESIZE/2 -5)

pygame.init()
myfont = pygame.font.SysFont("arial", 75)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 Window")

pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
pygame.event.set_blocked(pygame.MOUSEBUTTONUP)


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE/2, (r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE+SQUARESIZE/2, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (c*SQUARESIZE+SQUARESIZE/2, height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


def loadGame(board):
    draw_board(board)
    pygame.display.update()

def print_board(board):
    print(np.flip(board, 0))

def showWinningText(player):
    text = ("Player {player} wins!").format(player=player)
    f = open("winner.txt", "w")
    f.write(text)
    f.close()
    label = myfont.render(text, 1, RED)
    screen.blit(label, (40,10))
    pygame.display.update()

def removeText():
    f = open("winner.txt", "w")
    f.write("")
    f.close()