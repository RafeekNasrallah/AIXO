from copy import deepcopy
import pygame
import time

def thewinner(board): #checks if there is a winner, returns 1 if X is winner, 2 if O is winner and 0 if there is no winner
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


def isfull(board): # checks if the board is full, returns True, otherwise returns false
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return False
    return True


def allmoves(board,player):#generates all possible moves for a given board and player and returns a list of all the possible moves
    themoves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                new = deepcopy(board)
                new[i][j] = player
                themoves.append(new)
    return themoves


def whowins(board,fx): # evaluate function for minimax
        if thewinner(board) == 1:
            return 10
        if thewinner(board) == 2:
            return -10
        if isfull(board):
            return 0


def theMove(board,player,alpha,beta,fx): #picks a starting move, then calls minimax to compare which move is the best
    bestScore=-99999
    for i in range(3):
        for j in range(3):
            if board[i][j]==0:
                temp = deepcopy(board)
                temp[i][j] = player
                score = minimax(temp,2,alpha,beta,fx)
                if score > bestScore:
                    bestScore = score
                    move = (i,j)
    (i,j) = move
    return (i,j)





def minimax(board,player,alpha,beta,fx): #the minimax algorithm itslf
    if (isfull(board)) or (thewinner(board) != 0): #terminate condition
        return whowins(board,fx)
    list = allmoves(board,player) # generate all possible moves and puts them in a list
    if player == 1: # 1 is X and its the maximizer
        best = -99999
        for move in list: # iterate through all the possible moves and calling minimax on them
            score = minimax(move,2,alpha,beta,fx)
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                return
        return best
    else:
        best = 99999
        for move in list:
            score = minimax(move,1,alpha,beta,fx)
            best = min(best, score)
            alpha = min(alpha, best)
            if beta <= alpha:
                return
        return best

def findpos(i): # for GUI, checks for a given Pos, which block he pressed
    if i>10 and i<90:
        return 0
    if i>110 and i<190:
        return 1
    else:
        return 2



def draw_board(): # draws the board for the XO Board
    for col in range(3):
        for row in range(3):
            pygame.draw.rect(screen,(0,0,0),(col*100,row*100,100,100))
            pygame.draw.rect(screen,(255,255,255),((col*100)+10,(row*100)+10,80,80))


def draw_boardstart(): #draws the start board where he has to choose what to picj
    pygame.draw.rect(screen,(255,255,255),(75,100,150,80))
    pygame.draw.rect(screen,(0,0,0),(95,130,40,40))
    pygame.draw.rect(screen,(0,0,0),(160,130,40,40))
    font2 = pygame.font.Font('freesansbold.ttf', 25)
    text = font2.render('Play as:', True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (150, 115)
    screen.blit(text, textRect)
    text = font2.render('X', True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (115, 153)
    screen.blit(text, textRect)
    text = font2.render('O', True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (180, 153)
    screen.blit(text, textRect)




pygame.init()
screen = pygame.display.set_mode((300, 300))
font = pygame.font.Font('freesansbold.ttf', 100)
draw_boardstart()
pygame.display.update()
while True: # main loop, it only exists when the users quit the window, otherwise it keep going for new games
    originalBoard = [[0,0,0],
                 [0,0,0],
                 [0,0,0]]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse is pressed
            draw_board()
            pygame.display.update()
            if event.pos[1] >= 133 and event.pos[1] <179: #checks where he pressed in the start board, when he had to choose x or o
                if event.pos[0] > 97 and event.pos[0] <133:
                    x = 2 # this means he chose x
                    fx = True
                else:
                    if event.pos[0] >=163 and event.pos[0] <= 200:
                        x = 1
                        fx = False

            if x == 1: #so since the first steo, when the ai is playing with x, will always be 0,0, sparing the time im brute forcing this here
                first = True
            else:
                first = False
            while (not isfull(originalBoard)) and thewinner(originalBoard) == 0: # this loop keeps going till the game ends
                if (isfull(originalBoard)) or thewinner(originalBoard) != 0:
                    break
                for event3 in pygame.event.get():
                    if event3.type == pygame.QUIT:
                        exit()
                    if x == 2:
                        if event3.type == pygame.MOUSEBUTTONDOWN:
                            if fx:
                                texto = font.render('X', True, (0, 0, 0))
                            else:
                                texto = font.render('O', True, (0, 0, 0))
                            textRect = texto.get_rect()
                            i = event3.pos[0]
                            j = event3.pos[1]
                            while originalBoard[findpos(i)][findpos(j)] != 0: #and this loop checks if he pressed in an empty position,
                                for event2 in pygame.event.get():             #if not he can press again and again till eh find an empty position
                                    if event2.type == pygame.MOUSEBUTTONDOWN:
                                        i = event2.pos[0]
                                        j = event2.pos[1]
                                        if originalBoard[findpos(i)][findpos(j)] == 0:
                                            break
                            originalBoard[findpos(i)][findpos(j)] = x
                            textRect.center = (findpos(i) * 100 + 50, findpos(j) * 100 + 55)
                            screen.blit(texto, textRect)
                            pygame.display.update()
                            x = 1

                    else:
                        if x ==1:
                            if isfull(originalBoard):
                                break
                            if fx:
                                text = font.render('O', True, (0, 0, 0))
                            else:
                                text = font.render('X', True, (0, 0, 0))
                            textRect = text.get_rect()
                            if first:
                                textRect.center = (45, 55)
                                screen.blit(text, textRect)
                                pygame.display.update()
                                originalBoard[0][0] = 1
                                x = 2
                                first = False
                            else:
                                (i, j) = theMove(originalBoard, x, -99999, 99999,fx)
                                textRect.center = (i * 100 + 45, j * 100 + 55)
                                screen.blit(text, textRect)
                                pygame.display.update()
                                originalBoard[i][j] = 1
                                textRect.center = ((i * 100) + 10, (j * 100) + 10)
                                pygame.display.update()
                                x = 2
    if isfull(originalBoard) or thewinner(originalBoard) != 0: # writing who wins on teh screen in red when everything is done and restarting the game after 2 seconds
        font2 = pygame.font.Font('freesansbold.ttf', 50)
        winner = thewinner(originalBoard)
        if winner == 1:
            if fx:
                text = font2.render('O WINS', True, (255, 0, 0))
            else:
                text = font2.render('X WINS', True, (255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (150, 150)
            screen.blit(text, textRect)
            pygame.display.update()
            time.sleep(2)

        else:
            if winner == 2:
                text = font2.render('O WINS', True, (255, 0, 0))
                textRect = text.get_rect()
                textRect.center = (150, 150)
                screen.blit(text, textRect)
                pygame.display.update()
                time.sleep(2)
            else:
                text = font2.render('TIE', True, (255, 0, 0))
                textRect = text.get_rect()
                textRect.center = (150, 150)
                screen.blit(text, textRect)
                pygame.display.update()
                time.sleep(2)
        draw_boardstart()
        pygame.display.update()
