# simple little hill-climbing program used to generate the mysterious array in ai.py

from Board import Board
from ai import *
from random import random

def randAdd(gen):
    return (2*random() - 1) * (100-gen)/100

for test in range(10):
    oldScore = 100
    oldH = [0 for x in range(8) for y in range(x + 1,8)]
    newH = None
    score = None
    for trial in range(100):
        newH = [oldH[x] + randAdd(trial) for x in range(len(oldH))]
        theSum = 0
        for x in range(100):
            b = Board.generateRandomBoard()
            moveCount = 0
            while not b.gameOver():
                moveCount = moveCount + 1
                moves = []
                for m in validMoves(b):
                    h = heuristics(b, m)
                    heuristicNet = [h[x1] + h[x2] for x1 in range(8) for x2 in range(x1+1,8)]
                    moves.append( (sum([newH[y] * heuristicNet[y] for y in range(len(newH))]), m) )
                sMoves = sorted(moves, reverse=True)
                b.takeHit(sMoves[0][1])
            theSum = theSum + moveCount
        score = theSum / 100
        if score < oldScore:
            oldH = newH
            oldScore = score
    print(oldH, oldScore)
