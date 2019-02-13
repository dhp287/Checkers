''' Mini-Checkers'''
'''Implementation of a Mini-Checkers game for a human to play against a computer.
The game is played on a 6 x 6 squares board size.'''

import itertools
import pygame as pg
import numpy as np
import datetime
import time
from tkinter import *
import random

'''
Initial board containing 6 white pieces and 6 black pieces.
'1' - '6' :- are index values of the 6 x 6 board.
'.'(dot) :- signiies white space on the board where pieces are not allowed.
' ' (space) :- signifies empty space on the board where pieces are allowed.
'''
checkers_p = np.array([[' ','1 ','2 ','3 ','4 ','5 ','6 ','. '],
                    ['1','. ','W1','. ','W2','. ','W3','. '],
                    ['2','W4','. ','W5','. ','W6','. ','. '],
                    ['3','. ','  ','. ','  ','. ','  ','. '],
                    ['4','  ','. ','  ','. ','  ','. ','. '],
                    ['5','. ','B1','. ','B2','. ','B3','. '],
                    ['6','B4','. ','B5','. ','B6','. ','. ']])

t = datetime.datetime.now() #variable to restrict the execution of minimax for 15 seconds.
turn = 1 #determines who will play next, human or computer.
seconds = 8 #Default value of the time for which minimax algorithm will run to determine computer's next move.
secs = 8 #Default value of the time for which minimax algorithm will run to determine computer's next move.
node = 1 #Will Determine total number of nodes generated in the tree.
minprun = 0 #Will determine  number of times pruning occurred during MAX player's turn.
maxprun = 0 #Will determine  number of times pruning occurred during MIN player's turn.
maxdepth = 0 #Will determine maximum depth of tree.

'''
print_state(checkers) will print the current state of the game.
'''
def print_state(checkers):
    for i in range(7):
        for j in range(7):
            if i == 0:
                print('%s   ' % checkers[i][j], end='')
            else:
                print('%s | ' % checkers[i][j], end='')
        print()

'''
is_legal_white(checkers, x1, y1) will check if a white piece at position (x1, y1) has any legal moves,
if it has any legal moves it will return True else it will return False.
'''
def is_legal_white(checkers, x1, y1):
    if (x1 == 6):return False
    elif (y1 == 6 and x1 < 6 and checkers[x1 + 1][y1 - 1].startswith('W')):return False
    elif (y1 == 1 and x1 < 6 and checkers[x1 + 1][y1 + 1].startswith('W')):return False
    elif (x1 <= 4 and y1 == 1 and (checkers[x1 + 1][y1 + 1].startswith('B') and checkers[x1 + 2][y1 + 2] != '  ')):return False
    elif (x1 <= 4 and y1 == 6 and (checkers[x1 + 1][y1 - 1].startswith('B') and checkers[x1 + 2][y1 - 2] != '  ')):return False
    elif (x1 == 5 and y1 == 1 and checkers[x1 + 1][y1 + 1] != '  ') or (x1 == 5 and y1 == 6 and checkers[x1 + 1][y1 - 1] != '  '):return False
    elif (x1 == 5 and y1 >= 2 and y1 <= 5 and checkers[x1 + 1][y1 - 1] != '  ' and checkers[x1 + 1][y1 + 1] != '  '):return False
    elif (x1 <= 4 and y1 == 5 and (checkers[x1 + 1][y1 - 1].startswith('B') and checkers[x1 + 2][y1 - 2] != '  ') and checkers[x1 + 1][y1 + 1] != '  '):return False
    elif (x1 <=4 and y1 == 2 and checkers[x1 + 1][y1 - 1] != '  ' and (checkers[x1 + 1][y1 + 1].startswith('B') and checkers[x1 + 2][y1 + 2] != '  ')):return False
    elif (x1 <= 4 and y1 == 5 and (checkers[x1 + 1][y1 - 1].startswith('W')) and checkers[x1 + 1][y1 + 1] != '  '):return False
    elif (x1 <=4 and y1 == 2 and checkers[x1 + 1][y1 - 1] != '  ' and checkers[x1 + 1][y1 + 1].startswith('W')):return False
    elif (x1 <= 4 and y1 <= 4 and y1 >= 3 and (checkers[x1 + 1][y1 - 1].startswith('B') and checkers[x1 + 2][y1 - 2] != '  ') and (checkers[x1 + 1][y1 + 1].startswith('B') and checkers[x1 + 2][y1 + 2] != '  ')):return False
    elif (x1 <= 4 and y1 <= 4 and y1 >= 3 and (checkers[x1 + 1][y1 - 1].startswith('W')) and (checkers[x1 + 1][y1 + 1].startswith('B') and checkers[x1 + 2][y1 + 2] != '  ')):return False
    elif (x1 <= 4 and y1 <= 4 and y1 >= 3 and (checkers[x1 + 1][y1 - 1].startswith('B') and checkers[x1 + 2][y1 - 2] != '  ') and (checkers[x1 + 1][y1 + 1].startswith('W'))):return False
    elif (checkers[x1 + 1][y1 - 1].startswith('W') and checkers[x1 + 1][y1 + 1].startswith('W')):return False
    else:return True

'''
is_legal_black(checkers, x2, y2) will check if a black piece at position (x2, y2) has any legal moves,
if it has any legal moves it will return True else it will return False.
'''

def is_legal_black(checkers, x2, y2):
    if (x2 == 1):return False
    elif (y2 == 1 and x2 > 1 and checkers[x2 - 1][y2 + 1].startswith('B')):return False
    elif (y2 == 6 and x2 > 1 and checkers[x2 - 1][y2 - 1].startswith('B')):return False
    elif (x2 >= 3 and y2 == 6 and (checkers[x2 - 1][y2 - 1].startswith('W') and checkers[x2 - 2][y2 - 2] != '  ')):return False
    elif (x2 >= 3 and y2 == 1 and (checkers[x2 - 1][y2 + 1].startswith('W') and checkers[x2 - 2][y2 + 2] != '  ')):return False
    elif (x2 == 2 and y2 == 1 and checkers[x2 - 1][y2 + 1] != '  '):return False
    elif (x2 == 2 and y2 == 6 and checkers[x2 - 1][y2 - 1] != '  '):return False
    elif (x2 == 2 and y2 >= 2 and y2 <= 5 and checkers[x2 - 1][y2 - 1] != '  ' and checkers[x2 - 1][y2 + 1] != '  '):return False
    elif (x2 >= 3 and y2 == 2 and checkers[x2 - 1][y2 - 1] != '  ' and (checkers[x2 - 1][y2 + 1].startswith('W') and checkers[x2 - 2][y2 + 2] != '  ')):return False
    elif (x2 >= 3 and y2 == 5 and (checkers[x2 - 1][y2 - 1].startswith('W') and checkers[x2 - 2][y2 - 2] != '  ') and checkers[x2 - 1][y2 + 1] != '  '):return False
    elif (x2 >= 3 and y2 == 2 and checkers[x2 - 1][y2 - 1] != '  ' and checkers[x2 - 1][y2 + 1].startswith('B')):return False
    elif (x2 >= 3 and y2 == 5 and (checkers[x2 - 1][y2 - 1].startswith('B')) and checkers[x2 - 1][y2 + 1] != '  '):return False
    elif (x2 >= 3 and y2 >= 3 and y2 <= 4  and (checkers[x2 - 1][y2 - 1].startswith('W') and checkers[x2 - 2][y2 - 2] != '  ') and (checkers[x2 - 1][y2 + 1].startswith('W') and checkers[x2 - 2][y2 + 2] != '  ')):return False
    elif (x2 >= 3 and y2 >= 3 and y2 <= 4 and checkers[x2 - 1][y2 - 1].startswith('B') and checkers[x2 - 1][y2 + 1].startswith('W') and checkers[x2 - 2][y2 + 2] != '  '):return False
    elif (x2 >= 3 and y2 >= 3 and y2 <= 4 and checkers[x2 - 1][y2 - 1].startswith('W') and checkers[x2 - 2][y2 - 2] != '  ' and checkers[x2 - 1][y2 + 1].startswith('B')):return False
    elif (checkers[x2 - 1][y2 - 1].startswith('B') and checkers[x2 - 1][y2 + 1].startswith('B')):return False
    else:return True

'''
is_capture_move_white(checkers) finds the black pieces that can be captured with a jump move by the white pices and returns all such pieces in a list
'''

def is_capture_move_white(checkers):
    legal = []
    for i in range(1,7):
        for j in range(1,7):
            if checkers[i][j].startswith('W'):
                if i < 5:
                    if j == 1:
                        if checkers[i+1][j+1].startswith('B') and checkers[i+2][j+2] == '  ':
                            legal.append(checkers[i][j])
                    elif j == 6:
                        if checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ':
                            legal.append(checkers[i][j])
                    else:
                        if checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ':
                            legal.append(checkers[i][j])
                        elif checkers[i+1][j+1].startswith('B') and checkers[i+2][j+2] == '  ':
                            legal.append(checkers[i][j])
    return legal

'''
is_capture_move_black(checkers) finds the white pieces that can be captured with a jump move by the black pices and returns all such pieces in a list
'''

def is_capture_move_black(checkers):
    legal = []
    for i in range(1,7):
        for j in range(1,7):
            if checkers[i][j].startswith('B'):
                if i > 2:
                    if j == 1:
                        if checkers[i-1][j+1].startswith('W') and checkers[i-2][j+2] == '  ':
                            legal.append(checkers[i][j])
                    elif j == 6:
                        if checkers[i-1][j-1].startswith('W') and checkers[i-2][j-2] == '  ':
                            legal.append(checkers[i][j])
                    else:
                        if checkers[i-1][j-1].startswith('W') and checkers[i-2][j-2] == '  ':
                            legal.append(checkers[i][j])
                        elif checkers[i-1][j+1].startswith('W') and checkers[i-2][j+2] == '  ':
                            legal.append(checkers[i][j])
    return legal

'''
check_legal(checkers) counts the number of black and white pieces on the board as bpieces and wpieces respectively
and the number of black and white pieces which have legal moves left as bcount and wcount respectively
and will return all the values in a list
'''

def check_legal(checkers):
    wcount = 0
    bcount = 0
    wpieces = 0
    bpieces = 0
    ret = []
    for i in range(1,7):
        for j in range(1,7):
            if checkers[i][j].startswith('W'):
                wpieces += 1
                if not is_legal_white(checkers, i, j):
                    wcount += 1
            elif checkers[i][j].startswith('B'):
                bpieces += 1
                if not is_legal_black(checkers, i, j):
                    bcount += 1
    ret.append(wpieces)
    ret.append(wcount)
    ret.append(bpieces)
    ret.append(bcount)
    return ret

'''
evaluate function calculates the utility score of the current state of the board and returns the score.
It calculates the score of the white pieces and the score of the black pieces and returns the difference of both the scores.
If a piece cannot be captured i.e. no opposition piece is left in front of that piece then it gets 30 points.
If a piece can capture the opposition piece it gets 20 points.
And if a piece is not in the above two categories it gets 10 points.
'''

def evaluate(checkers):
    white_score = 0
    black_score = 0
    white = []
    black = []
    cw = is_capture_move_white(checkers)
    cb = is_capture_move_black(checkers)
    for i in range(1,7):
        for j in range(1,7):
            if checkers[i][j].startswith('W'):
                white.append(checkers[i][j])
            elif checkers[i][j].startswith('B'):
                black.append(checkers[i][j])
    for piece in white:
        i = np.argwhere(checkers == piece)[0][0]
        j = np.argwhere(checkers == piece)[0][1]
        count = 0
        for p in black:
            i1 = np.argwhere(checkers == p)[0][0]
            j1 = np.argwhere(checkers == p)[0][1]
            if i1 > i:
                count += 1
        if count == 0:
            white_score += 30   #30 for piece which cannot b captured by opposition
        elif checkers[i][j] in cw:
            white_score += 20   #20 for piece that can capture opposition piece
        else:
            white_score += 10 + i  #10 + i for all other pieces
    for piece in black:
        i = np.argwhere(checkers == piece)[0][0]
        j = np.argwhere(checkers == piece)[0][1]
        count = 0
        for p in white:
            i1 = np.argwhere(checkers == p)[0][0]
            j1 = np.argwhere(checkers == p)[0][1]
            if i1 < i:
                count += 1
        if count == 0:
            black_score += 30   #30 for piece which cannot b captured by opposition
        elif checkers[i][j] in cb:
            black_score += 20   #20 for piece that can capture opposition piece
        else:
            black_score += 10 + (6-i)   #10 + (6-i) for all other pieces
    return white_score - black_score

'''
maximum(checkers, depth, alpha, beta) is a maximizing function i.e. it tries to maximize the score in the alpha beta pruning algorithm,
'''

def maximum(checkers,depth, alpha, beta):
    global node
    global maxdepth
    global maxprun
    if depth > maxdepth:
        maxdepth = depth    #calculates the max depth reached at that iteration
    td = datetime.datetime.now() - t
    m = (td.days * 86400) + td.seconds
    if m < secs: #cutoff contition
        pg.event.pump()
        ret = check_legal(checkers)
        if ret[0] == ret[1] and ret[2] == ret[3]: #terminal state of the game, if reached score is returned
            return evaluate(checkers)
        elif ret[0] == ret[1]:
            return evaluate(checkers)
        else:
            best = -1000
            flag = False
            for i in range(1,7):
                if flag == True:
                    maxprun += 1    #calculates the maxprun value
                    break
                for j in range(1,7):    #checks all the moves possible for the white pieces
                    if checkers[i][j].startswith('W'):
                        if is_legal_white(checkers, i, j):
                            node += 1
                            if j == 1:
                                if checkers[i+1][j+1] == '  ':
                                    checkers[i+1][j+1] = checkers[i][j]
                                    checkers[i][j] = '  '
                                    best = max(best, minimum(checkers, depth+1, alpha, beta))
                                    alpha = max(best, alpha)
                                    checkers[i][j] = checkers[i+1][j+1]
                                    checkers[i+1][j+1] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                else: #checkers[i+1][j+1].startswith('B') and checkers[i+2][j+2] == '  ':
                                    temp = checkers[i+1][j+1]
                                    checkers[i+2][j+2] = checkers[i][j]
                                    checkers[i+1][j+1] = '  '
                                    checkers[i][j] = '  '
                                    best = max(best, minimum(checkers,depth+1, alpha, beta))
                                    alpha = max(best, alpha)
                                    checkers[i][j] = checkers[i+2][j+2]
                                    checkers[i+1][j+1] = temp
                                    checkers[i+2][j+2] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                            elif j == 6:
                                if checkers[i+1][j-1] == '  ':
                                    checkers[i+1][j-1] = checkers[i][j]
                                    checkers[i][j] = '  '
                                    best = max(best, minimum(checkers, depth+1,alpha, beta))
                                    alpha = max(best, alpha)
                                    checkers[i][j] = checkers[i+1][j-1]
                                    checkers[i+1][j-1] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                else: #checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ' and i < 5:
                                    temp = checkers[i+1][j-1]
                                    checkers[i+2][j-2] = checkers[i][j]
                                    checkers[i+1][j-1] = '  '
                                    checkers[i][j] = '  '
                                    best = max(best, minimum(checkers,depth+1, alpha, beta))
                                    alpha = max(best, alpha)
                                    checkers[i][j] = checkers[i+2][j-2]
                                    checkers[i+1][j-1] = temp
                                    checkers[i+2][j-2] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                            else:
                                if checkers[i+1][j-1] == '  ':
                                    checkers[i+1][j-1] = checkers[i][j]
                                    checkers[i][j] = '  '
                                    best = max(best, minimum(checkers,depth+1, alpha, beta))
                                    alpha = max(best, alpha)
                                    checkers[i][j] = checkers[i+1][j-1]
                                    checkers[i+1][j-1] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                elif checkers[i+1][j+1] == '  ':
                                    checkers[i+1][j+1] = checkers[i][j]
                                    checkers[i][j] = '  '
                                    best = max(best, minimum(checkers,depth+1, alpha, beta))
                                    alpha = max(best, alpha)
                                    checkers[i][j] = checkers[i+1][j+1]
                                    checkers[i+1][j+1] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                elif checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ' and i < 5:
                                    temp = checkers[i+1][j-1]
                                    checkers[i+2][j-2] = checkers[i][j]
                                    checkers[i+1][j-1] = '  '
                                    checkers[i][j] = '  '
                                    best = max(best, minimum(checkers, depth+1,alpha, beta))
                                    alpha = max(best, alpha)
                                    checkers[i][j] = checkers[i+2][j-2]
                                    checkers[i+1][j-1] = temp
                                    checkers[i+2][j-2] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                elif checkers[i+1][j+1].startswith('B') and checkers[i+2][j+2] == '  ' and i < 5:
                                    temp = checkers[i+1][j+1]
                                    checkers[i+2][j+2] = checkers[i][j]
                                    checkers[i+1][j+1] = '  '
                                    checkers[i][j] = '  '
                                    best = max(best, minimum(checkers, depth+1,alpha, beta))
                                    alpha = max(best, alpha)
                                    checkers[i][j] = checkers[i+2][j+2]
                                    checkers[i+1][j+1] = temp
                                    checkers[i+2][j+2] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                else:
                                    best = max(best, -1000)
                                    alpha = max(best, alpha)
                                    if beta <= alpha:
                                        flag = True
                                        break
            return best
    else:
        score = evaluate(checkers)  #when the search is cutoff, calculates the value of the current state of the board and returns the value.
        return score

'''
minimum(checkers, depth, alpha, beta) is a minimizing function i.e. it tries to minimize the score in the alpha beta pruning algorithm,
'''

def minimum(checkers,depth, alpha, beta):
    global node
    global maxdepth
    global minprun
    if depth > maxdepth:
        maxdepth = depth    #calculates the max depth reached at that iteration
    td = datetime.datetime.now() - t
    m = (td.days * 86400) + td.seconds
    if m < secs:    #cutoff contition
        pg.event.pump()
        ret = check_legal(checkers)
        if ret[0] == ret[1] and ret[2] == ret[3]:   #terminal state of the game, if reached score is returned
            return evaluate(checkers)
        elif ret[2] == ret[3]:
            return evaluate(checkers)
        else:
            best = 1000
            flag = False
            for i in range(1,7):
                if flag == True:
                    minprun += 1    #calculates the minprun value
                    break
                for j in range(1,7):    #checks all the moves possible for the black pieces
                    if checkers[i][j].startswith('B'):
                        if is_legal_black(checkers, i, j):
                            node += 1
                            if j == 1:
                                if checkers[i-1][j+1] == '  ':
                                    checkers[i-1][j+1] = checkers[i][j]
                                    checkers[i][j] = '  '
                                    best = min(best, maximum(checkers,depth+1, alpha, beta))
                                    beta = min(best, beta)
                                    checkers[i][j] = checkers[i-1][j+1]
                                    checkers[i-1][j+1] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                else: #checkers[i-1][j+1].startswith('W') and checkers[i-2][j+2] == '  ':
                                    temp = checkers[i-1][j+1]
                                    checkers[i-2][j+2] = checkers[i][j]
                                    checkers[i-1][j+1] = '  '
                                    checkers[i][j] = '  '
                                    best = min(best, maximum(checkers,depth+1, alpha, beta))
                                    beta = min(best, beta)
                                    checkers[i][j] = checkers[i-2][j+2]
                                    checkers[i-1][j+1] = temp
                                    checkers[i-2][j+2] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                            elif j == 6:
                                if checkers[i-1][j-1] == '  ':
                                    checkers[i-1][j-1] = checkers[i][j]
                                    checkers[i][j] = '  '
                                    best = min(best, maximum(checkers,depth+1, alpha, beta))
                                    beta = min(best, beta)
                                    checkers[i][j] = checkers[i-1][j-1]
                                    checkers[i-1][j-1] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                else: #checkers[i-1][j-1].startswith('W') and checkers[i-2][j-2] == '  ' and i > 2:
                                    temp = checkers[i-1][j-1]
                                    checkers[i-2][j-2] = checkers[i][j]
                                    checkers[i-1][j-1] = '  '
                                    checkers[i][j] = '  '
                                    best = min(best, maximum(checkers,depth+1, alpha, beta))
                                    beta = min(best, beta)
                                    checkers[i][j] = checkers[i-2][j-2]
                                    checkers[i-1][j-1] = temp
                                    checkers[i-2][j-2] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                            else:
                                if checkers[i-1][j-1] == '  ':
                                    checkers[i-1][j-1] = checkers[i][j]
                                    checkers[i][j] = '  '
                                    best = min(best, maximum(checkers,depth+1, alpha, beta))
                                    beta = min(best, beta)
                                    checkers[i][j] = checkers[i-1][j-1]
                                    checkers[i-1][j-1] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                elif checkers[i-1][j+1] == '  ':
                                    checkers[i-1][j+1] = checkers[i][j]
                                    checkers[i][j] = '  '
                                    best = min(best, maximum(checkers,depth+1, alpha, beta))
                                    beta = min(best, beta)
                                    checkers[i][j] = checkers[i-1][j+1]
                                    checkers[i-1][j+1] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                elif checkers[i-1][j-1].startswith('W') and checkers[i-2][j-2] == '  ' and i > 2:
                                    temp = checkers[i-1][j-1]
                                    checkers[i-2][j-2] = checkers[i][j]
                                    checkers[i-1][j-1] = '  '
                                    checkers[i][j] = '  '
                                    best = min(best, maximum(checkers,depth+1, alpha, beta))
                                    beta = min(best, beta)
                                    checkers[i][j] = checkers[i-2][j-2]
                                    checkers[i-1][j-1] = temp
                                    checkers[i-2][j-2] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                elif checkers[i-1][j+1].startswith('W') and checkers[i-2][j+2] == '  ' and i > 2:
                                    temp = checkers[i-1][j+1]
                                    checkers[i-2][j+2] = checkers[i][j]
                                    checkers[i-1][j+1] = '  '
                                    checkers[i][j] = '  '
                                    best = min(best, maximum(checkers,depth+1, alpha, beta))
                                    beta = min(best, beta)
                                    checkers[i][j] = checkers[i-2][j+2]
                                    checkers[i-1][j+1] = temp
                                    checkers[i-2][j+2] = '  '
                                    if beta <= alpha:
                                        flag = True
                                        break
                                else:
                                    best = min(best,1000)
                                    beta = min(best, beta)
                                    if beta <= alpha:
                                        flag = True
                                        break
            return best
    else:
        score = evaluate(checkers)  #when the search is cutoff, calculates the value of the current state of the board and returns the value.
        return score

'''
alpha_beta(checkers) is the function is initiates the alpha beta pruning algorithm, it checks for the legal moves the white pieces have and returns
the best possible move based on the utility score received from the maximum and minimum functions.
'''

def alpha_beta(checkers):
    global node
    global maxprun
    global minprun
    global maxdepth
    global t
    global secs
    node = 1
    maxprun = 0
    minprun = 0
    maxdepth = 0
    bestVal = -1000
    ibest = -1
    jbest = -1
    mi = -1
    mj = -1
    moveVal = -1000
    capture = is_capture_move_white(checkers)   #if there are capture moves then it will only check from among the capture moves and ignore all other moves.
    if len(capture) > 1:
        secs = seconds / len(capture)
        for piece in capture:
            t = datetime.datetime.now()
            i = np.argwhere(checkers == piece)[0][0]
            j = np.argwhere(checkers == piece)[0][1]
            if checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ':
                temp = checkers[i+1][j-1]
                checkers[i+2][j-2] = checkers[i][j]
                checkers[i+1][j-1] = '  '
                checkers[i][j] = '  '
                mi = i+2
                mj = j-2
                moveVal = minimum(checkers,0, -1000, 1000)
                if moveVal > bestVal: #if value of the current move is better than the best value replace the best value with move value
                    ibest = mi
                    icurr = i
                    jbest = mj
                    jcurr = j
                    bestVal = moveVal
                checkers[i][j] = checkers[i+2][j-2] #undo the current move so that other moves can be taken.
                checkers[i+1][j-1] = temp
                checkers[i+2][j-2] = '  '
            if checkers[i+1][j+1].startswith('B') and checkers[i+2][j+2] == '  ':
                temp = checkers[i+1][j+1]
                checkers[i+2][j+2] = checkers[i][j]
                checkers[i+1][j+1] = '  '
                checkers[i][j] = '  '
                mi = i+2
                mj = j+2
                moveVal = minimum(checkers,0, -1000, 1000)
                if moveVal > bestVal:
                    ibest = mi
                    icurr = i
                    jbest = mj
                    jcurr = j
                    bestVal = moveVal
                checkers[i][j] = checkers[i+2][j+2]
                checkers[i+1][j+1] = temp
                checkers[i+2][j+2] = '  '
    elif len(capture) == 1:
        i = np.argwhere(checkers == capture[0])[0][0]
        j = np.argwhere(checkers == capture[0])[0][1]
        if checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ' and checkers[i+1][j+1].startswith('B') and checkers[i+2][j+2] == '  ':
            temp = checkers[i+1][j-1]
            checkers[i+2][j-2] = checkers[i][j]
            checkers[i+1][j-1] = '  '
            checkers[i][j] = '  '
            mi = i+2
            mj = j-2
            moveVal = minimum(checkers,0, -1000, 1000)
            if moveVal > bestVal:
                ibest = mi
                icurr = i
                jbest = mj
                jcurr = j
                bestVal = moveVal
            checkers[i][j] = checkers[i+2][j-2]
            checkers[i+1][j-1] = temp
            checkers[i+2][j-2] = '  '
            temp = checkers[i+1][j+1]
            checkers[i+2][j+2] = checkers[i][j]
            checkers[i+1][j+1] = '  '
            checkers[i][j] = '  '
            mi = i+2
            mj = j+2
            moveVal = minimum(checkers,0, -1000, 1000)
            if moveVal > bestVal:
                ibest = mi
                icurr = i
                jbest = mj
                jcurr = j
                bestVal = moveVal
            checkers[i][j] = checkers[i+2][j+2]
            checkers[i+1][j+1] = temp
            checkers[i+2][j+2] = '  '
        elif checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ':
            #if there is only one capture move take that move immediately without calling the minimum and maximum functions.
            mi = i+2
            mj = j-2
            ibest = mi
            icurr = i
            jbest = mj
            jcurr = j
        else:
            mi = i+2
            mj = j+2
            ibest = mi
            icurr = i
            jbest = mj
            jcurr = j
    else:   # if no capture moves then it will check from among all the legal moves which are there to take.
        legal = []
        for i in range(1,7):
            for j in range(1,7):
                if checkers[i][j].startswith('W'):
                    if is_legal_white(checkers, i, j):
                        legal.append(checkers[i][j])
        secs = seconds / len(legal)
        for piece in legal:
            t = datetime.datetime.now()
            i = np.argwhere(checkers == piece)[0][0]
            j = np.argwhere(checkers == piece)[0][1]
            if j == 1:
                if checkers[i+1][j+1] == '  ':
                    checkers[i+1][j+1] = checkers[i][j]
                    checkers[i][j] = '  '
                    mi = i+1
                    mj = j+1
                    moveVal = minimum(checkers,0, -1000, 1000)
                    if moveVal > bestVal:    #if value of the current move is better than the best value replace the best value with move value
                        ibest = mi
                        icurr = i
                        jbest = mj
                        jcurr = j
                        bestVal = moveVal
                    checkers[i][j] = checkers[i+1][j+1] #undo the current move so that other moves can be taken.
                    checkers[i+1][j+1] = '  '
                else: #checkers[i+1][j+1].startswith('B') and checkers[i+2][j+2] == '  ':
                    temp = checkers[i+1][j+1]
                    checkers[i+2][j+2] = checkers[i][j]
                    checkers[i+1][j+1] = '  '
                    checkers[i][j] = '  '
                    mi = i+2
                    mj = j+2
                    moveVal = minimum(checkers,0, -1000, 1000)
                    if moveVal > bestVal:
                        ibest = mi
                        icurr = i
                        jbest = mj
                        jcurr = j
                        bestVal = moveVal
                    checkers[i][j] = checkers[i+2][j+2]
                    checkers[i+1][j+1] = temp
                    checkers[i+2][j+2] = '  '
            elif j == 6:
                if checkers[i+1][j-1] == '  ':
                    checkers[i+1][j-1] = checkers[i][j]
                    checkers[i][j] = '  '
                    mi = i+1
                    mj = j-1
                    moveVal = minimum(checkers,0, -1000, 1000)
                    if moveVal > bestVal:
                        ibest = mi
                        icurr = i
                        jbest = mj
                        jcurr = j
                        bestVal = moveVal
                    checkers[i][j] = checkers[i+1][j-1]
                    checkers[i+1][j-1] = '  '
                else: #checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ' and i < 5:
                    temp = checkers[i+1][j-1]
                    checkers[i+2][j-2] = checkers[i][j]
                    checkers[i+1][j-1] = '  '
                    checkers[i][j] = '  '
                    mi = i+2
                    mj = j-2
                    moveVal = minimum(checkers,0, -1000, 1000)
                    if moveVal > bestVal:
                        ibest = mi
                        icurr = i
                        jbest = mj
                        jcurr = j
                        bestVal = moveVal
                    checkers[i][j] = checkers[i+2][j-2]
                    checkers[i+1][j-1] = temp
                    checkers[i+2][j-2] = '  '
            else:
                if checkers[i+1][j-1] == '  ':
                    checkers[i+1][j-1] = checkers[i][j]
                    checkers[i][j] = '  '
                    mi = i+1
                    mj = j-1
                    moveVal = minimum(checkers,0, -1000, 1000)
                    if moveVal > bestVal:
                        ibest = mi
                        icurr = i
                        jbest = mj
                        jcurr = j
                        bestVal = moveVal
                    checkers[i][j] = checkers[i+1][j-1]
                    checkers[i+1][j-1] = '  '
                elif i < 5:
                    if checkers[i+1][j-1].startswith('B') and checkers[i+2][j-2] == '  ':
                        temp = checkers[i+1][j-1]
                        checkers[i+2][j-2] = checkers[i][j]
                        checkers[i+1][j-1] = '  '
                        checkers[i][j] = '  '
                        mi = i+2
                        mj = j-2
                        moveVal = minimum(checkers,0, -1000, 1000)
                        if moveVal > bestVal:
                            ibest = mi
                            icurr = i
                            jbest = mj
                            jcurr = j
                            bestVal = moveVal
                        checkers[i][j] = checkers[i+2][j-2]
                        checkers[i+1][j-1] = temp
                        checkers[i+2][j-2] = '  '
                if checkers[i+1][j+1] == '  ':
                    checkers[i+1][j+1] = checkers[i][j]
                    checkers[i][j] = '  '
                    mi = i+1
                    mj = j+1
                    moveVal = minimum(checkers,0, -1000, 1000)
                    if moveVal > bestVal:
                        ibest = mi
                        icurr = i
                        jbest = mj
                        jcurr = j
                        bestVal = moveVal
                    checkers[i][j] = checkers[i+1][j+1]
                    checkers[i+1][j+1] = '  '
                elif i < 5:
                    if checkers[i+1][j+1].startswith('B') and checkers[i+2][j+2] == '  ':
                        temp = checkers[i+1][j+1]
                        checkers[i+2][j+2] = checkers[i][j]
                        checkers[i+1][j+1] = '  '
                        checkers[i][j] = '  '
                        mi = i+2
                        mj = j+2
                        moveVal = minimum(checkers,0, -1000, 1000)
                        if moveVal > bestVal:
                            ibest = mi
                            icurr = i
                            jbest = mj
                            jcurr = j
                            bestVal = moveVal
                        checkers[i][j] = checkers[i+2][j+2]
                        checkers[i+1][j+1] = temp
                        checkers[i+2][j+2] = '  '
    #print the statistics of the current iteration.
    print('Number of Nodes :- ', node)
    print('Maximum Depth :- ', maxdepth)
    print('Min Pruning :- ', minprun)
    print('Max Pruning :- ', maxprun)
    bmv = []
    bmv.append(icurr)
    bmv.append(jcurr)
    bmv.append(ibest)
    bmv.append(jbest)
    return bmv  #return the best move that can be taken at this time.

'''
check_end_pos(checkers, x2, y2, b1, b2) checks if the end position selected by the human to move a piece is legal,
if its legal it returns False else returns True.
'''

def check_end_pos(checkers, x2, y2, b1, b2):
    if(checkers[b1][b2] == '. '):return True
    elif b1 > x2:return True
    elif len(capture) > 0 and abs(x2-b1) != 2 and abs(y2-b2) != 2:return True
    elif x2-b1 == 2 and y2-b2 == 2 and checkers[b1 + 1][b2 + 1] == '  ':return True
    elif x2-b1 == 2 and y2-b2 == -2 and checkers[b1 + 1][b2 - 1] == '  ':return True
    elif x2-b1 == 2 and y2-b2 == 2 and checkers[b1][b2] != '  ':return True
    elif x2-b1 == 2 and y2-b2 == -2 and checkers[b1][b2] != '  ':return True
    elif x2-b1 == 2 and y2-b2 == 2 and checkers[b1 + 1][b2 + 1].startswith('B'):return True
    elif x2-b1 == 2 and y2-b2 == -2 and checkers[b1 + 1][b2 - 1].startswith('B'):return True
    elif checkers[b1][b2] != '  ':return True
    elif abs(x2-b1) != abs(y2-b2):return True
    elif abs(x2-b1) > 2 or abs(y2-b2) > 2:return True
    else:return False

'''
levels of the game are managed by the cutoff of the alpha_beta pruning algorithm
'''

def first():    #when the level of play is selected as 1 the cutoff of the alpha_beta search is set to 0 seconds
    global seconds
    seconds = 0
    window.destroy()
def second():   #when the level of play is selected as 2 the cutoff of the alpha_beta search is set to 8 seconds
    global seconds
    seconds = 8
    window.destroy()
def third():    #when the level of play is selected as 3 the cutoff of the alpha_beta search is set to 15 seconds
    global seconds
    seconds = 15
    window.destroy()

def exit_function1():   #used to destroy the window when new game is continued
    exit_window.destroy()

def exit_function2():   #used to destroy the window when game is exited
    global exit
    exit = True
    exit_window.destroy()
'''
Following code is for the user interface of the game using pygame, it also contains logic for the human player.
'''
exit = False
while exit == False:
    turn = 1
    str = ''
    checkers = np.copy(checkers_p)
    print_state(checkers)
    window = Tk()
    #shows the window to select the level of the game.
    Label(window, text='Select Level').grid(row=1,column=2)
    Button(window, text = '    1    ', command=first).grid(row=2,column=2)
    Button(window, text = '    2    ', command=second).grid(row=3,column=2)
    Button(window, text = '    3    ', command=third).grid(row=4,column=2)
    window.mainloop()
    pg.init()
    #specifies the colors of the pieces and the board of the mini-checkers game
    RED = pg.Color(150,150,150,255)
    WHITE = pg.Color(200,200,200,255)
    GREEN = pg.Color(0,128,0,255)
    BLUE = pg.Color(50,50,50,255)
    BLACK = pg.Color('black')
    screen = pg.display.set_mode((420, 420)) #size of the window
    colors = itertools.cycle((WHITE, RED))
    tile_size = 70 #size of each tile on the checkers board
    width, height = 6*tile_size, 6*tile_size
    background = pg.Surface((width, height))
    #following for loop draws the checkers board
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            rect = (x, y, tile_size, tile_size)
            pg.draw.rect(background, next(colors), rect)
        next(colors)
    checkers_t = np.transpose(checkers[1:7,1:7])
    #following for loop draws the pieces on the board
    for i in range(6):
        for j in range(6):
            if checkers_t[i][j].startswith('W'):
                pg.draw.circle(background, WHITE, (i*70+35,j*70+35), 30)
            elif checkers_t[i][j].startswith('B'):
                pg.draw.circle(background, BLUE, (i*70+35,j*70+35), 30)
    game_exit = False
    #following while loop will run untill the game is running
    while not game_exit:
        screen.blit(background, (0, 0))
        pg.display.update()
        #the above two lines draws the new state of the board after the pieces are moved
        if turn == 2: #this is computers turn
            pg.display.set_caption('Computer\'s turn, please wait....')
            bmv = alpha_beta(checkers) #alpha_beta is callled on current state and best move is returned
            x1 = bmv[0]
            y1 = bmv[1]
            w1 = bmv[2]
            w2 = bmv[3]
            p = checkers[x1][y1]
            print(checkers[x1][y1])
            #following code makes the move that was returned by the the alpha_beta function
            if x1-w1 == -2 and y1-w2 == 2 and checkers[w1 - 1][w2 + 1].startswith('B'):
                checkers[x1][y1] = '  '
                checkers[w1 - 1][w2 + 1] = '  '
                checkers[w1][w2] = p
                pg.draw.circle(background, RED, ((y1-1)*70+35,(x1-1)*70+35), 30)
                pg.draw.circle(background, RED, (((w2-1)+1)*70+35,((w1-1)-1)*70+35), 30)
                pg.draw.circle(background, WHITE, ((w2-1)*70+35,(w1-1)*70+35), 30)
            elif x1-w1 == -2 and y1-w2 == -2 and checkers[w1 - 1][w2 - 1].startswith('B'):
                checkers[x1][y1] = '  '
                checkers[w1 - 1][w2 - 1] = '  '
                checkers[w1][w2] = p
                pg.draw.circle(background, RED, ((y1-1)*70+35,(x1-1)*70+35), 30)
                pg.draw.circle(background, RED, (((w2-1)-1)*70+35,((w1-1)-1)*70+35), 30)
                pg.draw.circle(background, WHITE, ((w2-1)*70+35,(w1-1)*70+35), 30)
            else:
                checkers[x1][y1] = '  '
                checkers[w1][w2] = p
                pg.draw.circle(background, RED, ((y1-1)*70+35,(x1-1)*70+35), 30)
                pg.draw.circle(background, WHITE, ((w2-1)*70+35,(w1-1)*70+35), 30)
            print_state(checkers)
            turn = 1;
            time.sleep(1)
        else: #this is humans turn
            capture = is_capture_move_black(checkers)
            pg.display.set_caption('Your turn')
            while turn == 1: #this loop will run untill human makes a valid move
                screen.blit(background, (0, 0))
                pg.display.update()
                #the above two lines draws the new state of the board after the pieces are moved
                for event in pg.event.get(): #pg.event.get gets the event that occured on the game window
                    if event.type == pg.QUIT:
                        pg.quit()
                    elif event.type == pg.MOUSEBUTTONDOWN:  #if mouse button is pressed control enters this if loop
                        px, py = event.pos  #position of the click is captured
                        i = int(px/70)
                        j = int(py/70)
                        #following code will check if the piece selected has any legal moves left.
                        if not checkers[j+1][i+1].startswith('B'):
                            pg.display.set_caption('Its not your piece, please select your piece.')
                        elif len(capture) > 0 and checkers[j+1][i+1] not in capture:
                            pg.display.set_caption('You cannot move this piece, select some other piece')
                        elif not is_legal_black(checkers, j+1, i+1):
                            pg.display.set_caption('You cannot move this piece, select some other piece')
                        else:
                            pg.draw.circle(background, GREEN, (i*70+35,j*70+35), 30)
                            for l in range(6):
                                for m in range(6):
                                    if l == i and m == j:continue
                                    else:
                                        if background.get_at((l*70+35,m*70+35))[1] == 128 and background.get_at((l*70+35,m*70+35))[0] == 0 and background.get_at((l*70+35,m*70+35))[2] == 0:
                                            pg.draw.circle(background, BLUE, (l*70+35,m*70+35), 30)
                            end_position = False
                            #if piece selected has legal moves control will enter the following if loop
                            while(end_position == False):
                                change = False
                                screen.blit(background, (0, 0))
                                pg.display.update()
                                pg.display.set_caption('Select end position.')  #asks for the end position of the piece selected.
                                for event in pg.event.get():
                                    if event.type == pg.QUIT:
                                        pg.quit()
                                    elif event.type == pg.MOUSEBUTTONDOWN:  #if mouse button is pressed control enters this if loop
                                        px, py = event.pos  #position of the click is captured
                                        b2 = int(px/70)+1
                                        b1 = int(py/70)+1
                                        x2 = j+1
                                        y2 = i+1
                                        if check_end_pos(checkers, x2, y2, b1, b2):
                                            pg.display.set_caption('Select a correct end position.')
                                            change = True
                                            break
                                        #if the end position is legal then following code will run and the piece will be moved to its new location
                                        if not check_end_pos(checkers, x2, y2, b1, b2):
                                            print(checkers[x2][y2])
                                            p = checkers[x2][y2]
                                            if x2-b1 == 2 and y2-b2 == 2 and checkers[b1 + 1][b2 + 1].startswith('W'):
                                                checkers[x2][y2] = '  '
                                                checkers[b1 + 1][b2 + 1] = '  '
                                                checkers[b1][b2] = p
                                                pg.draw.circle(background, RED, ((y2-1)*70+35,(x2-1)*70+35), 30)
                                                pg.draw.circle(background, RED, (((b2-1)+1)*70+35,((b1-1)+1)*70+35), 30)
                                                pg.draw.circle(background, BLUE, ((b2-1)*70+35,(b1-1)*70+35), 30)
                                            elif x2-b1 == 2 and y2-b2 == -2 and checkers[b1 + 1][b2 - 1].startswith('W'):
                                                checkers[x2][y2] = '  '
                                                checkers[b1 + 1][b2 - 1] = '  '
                                                checkers[b1][b2] = p
                                                pg.draw.circle(background, RED, ((y2-1)*70+35,(x2-1)*70+35), 30)
                                                pg.draw.circle(background, RED, (((b2-1)-1)*70+35,((b1-1)+1)*70+35), 30)
                                                pg.draw.circle(background, BLUE, ((b2-1)*70+35,(b1-1)*70+35), 30)
                                            else:
                                                checkers[x2][y2] = '  '
                                                checkers[b1][b2] = p
                                                pg.draw.circle(background, RED, ((y2-1)*70+35,(x2-1)*70+35), 30)
                                                pg.draw.circle(background, BLUE, ((b2-1)*70+35,(b1-1)*70+35), 30)
                                            print_state(checkers)
                                            end_position = True
                                            turn = 2
                                if change == True:
                                    for l in range(6):
                                        for m in range(6):
                                            if background.get_at((l*70+35,m*70+35))[1] == 128 and background.get_at((l*70+35,m*70+35))[0] == 0 and background.get_at((l*70+35,m*70+35))[2] == 0:
                                                pg.draw.circle(background, BLUE, (l*70+35,m*70+35), 30)
                                    break
        ret = check_legal(checkers)
        wpieces = ret[0]
        wcount = ret[1]
        bpieces = ret[2]
        bcount = ret[3]
        #If a player has no legal move to take, his/her turn will be forfeited and the other player will make the next move. Following code will do that.
        if turn == 2 and wcount == wpieces and bpieces != bcount and bpieces > 0 and wpieces > 0:
            turn = 1
        elif turn == 1 and bcount == bpieces and wcount != wpieces and bpieces > 0 and wpieces > 0:
            turn = 2
        elif wcount == wpieces and bcount == bpieces: #this is the terminating condition of the game
            game_exit = True
            if(wpieces == bpieces): #if pieces are equal game drawn
                str = 'Game Drawn'
                pg.display.set_caption('Game Drawn')
                print('Game Drawn')
            elif(wpieces > bpieces):    #if white pieces are more human looses the game
                str = 'You Lost'
                pg.display.set_caption('You Lost')
                print('You Lost')
            else:                       #if black pieces are more human wins the game
                str = 'You Won'
                pg.display.set_caption('You Won')
                print('You Won')
        elif wpieces == 0:              #if no white pieces left human wins the game
            str = 'You Won'
            game_exit = True
            pg.display.set_caption('You Won')
            print('You Won')
        elif bpieces == 0:          #if no black pieces left human looses the game
            str = 'You Lost'
            game_exit = True
            pg.display.set_caption('You Lost')
            print('You Lost')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True
                exit = True
    screen.blit(background, (0, 0))
    pg.display.update()
    exit_window = Tk()
    #following code asks through a window that if human player wants to play another game.
    Label(exit_window, text=str).grid(row=1,column=2)
    Label(exit_window, text='Do you want to play again?').grid(row=2,column=2)
    Button(exit_window, text = '     Yes    ', command=exit_function1).grid(row=3,column=2)
    Button(exit_window, text = '     No     ', command=exit_function2).grid(row=3,column=3)
    exit_window.mainloop()
    pg.quit()
pg.quit()
