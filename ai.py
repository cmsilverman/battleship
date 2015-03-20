# This file depends on the boards being 10x10
# Use nextMove('optimal')

from Board import Board
from random import random, shuffle
from subprocess import call

AIOPTIONS = ['optimal', 'random']
TIME_TOLERANCE = 3 # in seconds, how long the longest moves should take
                   # -1 if you never want brute-forcing to happen
TIME_TABLE = { 35: 12.14,
               36: 5.15,
               37: 5.43,
               38: 3.68,
               39: 3.29,
               40: 1.69,
               41: 2.17,
               42: 2.28,
               43: 1.94,
               44: 0.47,
               45: 0.37,
               46: 0.83,
               47: 0.69,
               48: 0.37,
               49: 0.13,
               50: 0.31,
               51: 0.14,
               52: 0.28,
               53: 0.08,
               54: 0.16,
               55: 0.06,
               56: 0.02,
               57: 0.01,
               58: 0.02,
               59: 0.0,
               60: 0.01,
               61: 0.01,
               62: 0.0,
               63: 0.0,
               64: 0.0,
               65: 0.0,
               66: 0.0,
               67: 0.0,
               68: 0.0,
               69: 0.0,
               70: 0.0,
               71: 0.0,
               72: 0.0,
               73: 0.0,
               74: 0.0,
               75: 0.0,
               76: 0.0,
               77: 0.0,
               78: 0.0,
               79: 0.0,
               80: 0.0,
               81: 0.0,
               82: 0.0
             } # Anything less than 35 takes...a while

def whenToBruteForce(tolerance):
    if tolerance < 0: return None
    keys = sorted(TIME_TABLE.keys(), reverse=True)
    for k in keys:
        if TIME_TABLE[k] > tolerance: return k+1
    return keys[-1] # Again, advisable tolerances will stop before this happens

MIN_INCORRECT = whenToBruteForce(TIME_TOLERANCE)

def validMoves(board):
    return [(x, y) for x in range(Board.rows) for y in range(Board.cols) if board.board[x][y] < 2]

def randomMove(board):
    options = validMoves(board)
    return options[int(random()*len(options))]

def heuristics(board, pos):
    h = [0, 0, 0, 0, 0, 0, 0, 0]
    successLines = [0, 0, 0, 0]
    failed = [0, 0, 0, 0]
    (y, x) = pos
    x0 = x1 = x2 = x3 = x
    y0 = y1 = y2 = y3 = y
    for i in range(1,11):
        x0 = x0 + 1
        if failed[0] <= 0:
            if x0 >= 10 or board.board[y0][x0] == 2:
                failed[0] = i
            elif board.board[y0][x0] < 2:
                failed[0] = -1
        y1 = y1 - 1
        if failed[1] <= 0:
            if y1 < 0 or board.board[y1][x1] == 2:
                failed[1] = i
            elif board.board[y1][x1] < 2:
                failed[1] = -1
        x2 = x2 - 1
        if failed[2] <= 0:
            if x2 < 0 or board.board[y2][x2] == 2:
                failed[2] = i
            elif board.board[y2][x2] < 2:
                failed[2] = -1
        y3 = y3 + 1
        if failed[3] <= 0:
            if y3 >= 10 or board.board[y3][x3] == 2:
                failed[3] = i
            elif board.board[y3][x3] < 2:
                failed[3] = -1
        timeToQuit = True
        for j in range(4):
            if failed[j] == 0:
                successLines[j] = i
                if i < 6:
                    h[i + 2] = h[i + 2] + 1
            if failed[j] <= 0:
                timeToQuit = False
        if timeToQuit:
            break
    h[0] = min(failed)
    h[1] = sum(failed)
    if successLines[0] > 0 and successLines[2] > 0: h[2] = h[2] + 1
    if successLines[1] > 0 and successLines[3] > 0: h[2] = h[2] + 1
    return h

def generateMeasurement(heuristicArray):
    arr = [-0.39327799534937513, -1.792984886190242, 4.281445223542508, 2.3469759133214754, 0.8354731660471665, 1.0309537235621375, 0.27132739366156355, 0.599564678651541, 1.005266318578071, 1.8149385722169682, 0.051623286487621434, -0.6839073184706217, -0.4532432309529142, 4.185120914145534, 3.404118872938517, 0.576674946189906, 0.3696021718811566, -2.8122045667486666, -2.49781340218178, 2.3782496065305367, 1.6435499772446476, 0.0424348591078799, 1.67976653945592, 0.8616288696969998, 2.4061906518590632, -0.07568747430973366, -0.7858308793999341, -0.3625244144075441]
    heuristicNet = [heuristicArray[x1] + heuristicArray[x2] for x1 in range(8) for x2 in range(x1+1,8)]
    return sum([heuristicNet[i] * arr[i] for i in range(len(arr))])

def bestMove(board):
    options = validMoves(board)
    shuffle(options)
    incorrectGuesses = [(x, y) for x in range(Board.rows) for y in range(Board.cols) if board.board[x][y] == 2]
    if len(incorrectGuesses) >= MIN_INCORRECT:
        goodGuesses = [x*Board.cols + y for x in range(Board.rows) for y in range(Board.cols) if board.board[x][y] == 3]
        badGuesses = [x*Board.cols + y for (x,y) in incorrectGuesses]
        args = [str(len(goodGuesses))]
        for x in goodGuesses:
            args.append(str(x))
        args.append(str(len(badGuesses)))
        for x in badGuesses:
            args.append(str(x))
        move =  call(['./nextMove'] + args)
        return (move//Board.cols, move%Board.cols)
    heurs = sorted([(generateMeasurement(heuristics(board, option)), option) for option in options], reverse=True)
    return heurs[0][1]

def nextMove(board, strategy):
    if not strategy in AIOPTIONS:
        return None
    if board.gameOver():
        return None
    if strategy == 'random':
        return randomMove(board)
    if strategy == 'optimal':
        return bestMove(board)
