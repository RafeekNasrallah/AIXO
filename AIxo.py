from copy import deepcopy
import pygame
from tkinter import messagebox


def thewinner(board):
    if board[0][0] == board[0][1] == board[0][2] != 0:
        return board[0][0]
    if board[1][0] == board[1][1] == board[1][2] != 0:
        return board[1][0]
    if board[2][0] == board[2][1] == board[2][2] != 0:
        return board[2][0]
    if board[0][0] == board[1][0] == board[2][0] != 0:
        return board[0][0]
    if board[0][1] == board[1][1] == board[2][1] != 0:
        return board[0][1]
    if board[0][2] == board[1][2] == board[2][2] != 0:
        return board[0][2]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return 0


def isfull(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return False
    return True


def allmoves(board,player):
    themoves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                new = deepcopy(board)
                new[i][j] = player
                themoves.append(new)
    return themoves


def whowins(board):
    if thewinner(board) == 1:
        return 10
    if thewinner(board) == 2:
        return -10
    if isfull(board):
        return 0


def theMove(board,player,alpha,beta):
    bestScore=-99999
    for i in range(3):
        for j in range(3):
            if board[i][j]==0:
                temp = deepcopy(board)
                temp[i][j] = player
                score = minimax(temp,2,alpha,beta)
                if score>bestScore:
                    bestScore = score
                    move = (i,j)
    (i,j) = move
    return (i,j)





def minimax(board,player,alpha,beta):
    if (isfull(board)) or (thewinner(board) != 0):
        return whowins(board)
    list = allmoves(board,player)
    if player == 1:
        best = -99999
        for move in list:
            score = minimax(move,2,alpha,beta)
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                return
        return best
    else:
        best = 99999
        for move in list:
            score = minimax(move,1,alpha,beta)
            best = min(best, score)
            alpha = min(alpha, best)
            if beta <= alpha:
                return
        return best


def draw_board():
    for col in range(3):
        for row in range(3):
            pygame.draw.rect(screen,(0,0,0),(col*100,row*100,100,100))
            pygame.draw.rect(screen,(255,255,255),((col*100)+10,(row*100)+10,80,80))


pygame.init()
screen = pygame.display.set_mode((300, 300))
font = pygame.font.Font('freesansbold.ttf', 100)
draw_board()
pygame.display.update()
originalBoard = [[0,0,0],
                 [0,0,0],
                 [0,0,0]]



def findpos(i):
    if i>10 and i<90:
        return 0
    if i>110 and i<190:
        return 1
    else:
        return 2



x = 1
if x == 1:
    first = True
else:
    first = False
while (not isfull(originalBoard)) and thewinner(originalBoard) == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if x==1:
            text = font.render('X', True, (0, 0, 0))
            textRect = text.get_rect()
            if first:
                textRect.center = (45, 55)
                screen.blit(text, textRect)
                pygame.display.update()
                originalBoard[0][0] = 1
                x = 2
                first = False
                print(originalBoard)
            else:
                (i, j) = theMove(originalBoard, x, -99999, 99999)
                textRect.center = (i*100+45,j*100 + 55)
                screen.blit(text, textRect)
                pygame.display.update()
                originalBoard[i][j] = 1
                textRect.center = ((i * 100) + 10, (j * 100) + 10)
                pygame.display.update()
                print(originalBoard)
                x = 2

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                texto = font.render('O', True, (0, 0, 0))
                textRect = texto.get_rect()
                i = event.pos[0]
                j = event.pos[1]
                while originalBoard[findpos(i)][findpos(j)] != 0:
                    print("this cell is full")
                    i = event.pos[0]
                    j = event.pos[1]
                originalBoard[findpos(i)][findpos(j)] = x
                textRect.center = (findpos(i)*100+50, findpos(j)*100+55)
                screen.blit(texto, textRect)
                pygame.display.update()
                print(originalBoard)
                x = 1

winner = thewinner(originalBoard)
if winner == 1:
    messagebox.showinfo('Continue','X Wins')
else:
    if winner == 2:
        messagebox.showinfo('Continue','O Wins')
    else:
        messagebox.showinfo('Continue','Tie')

