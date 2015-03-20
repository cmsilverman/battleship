# This file does not depend on the boards being 10x10

from random import random

COLORS = {
    'black': 0,
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue': 4,
    'pink': 5,
    'cyan': 6,
    'white': 7
}

def coloredText(t, fg, bg):
    res = '\033[{}m'.format(40 + COLORS[bg])
    res += '\033[1;{}m'.format(30 + COLORS[fg])
    res += t
    res += '\033[0m'
    return res

class Board:

    # Static things
    rows = 10
    cols = 10
    columnNames = 'ABCDEFGHIL'
    ships = (5, 4, 3, 3, 2)
    def inputSpace():
        while True:
            try:
                line = input()
                if line == 'q': return None
                if len(line) < 2:
                    raise ValueError
                c = line[0].upper()
                if not c in Board.columnNames:
                    raise ValueError
                c = Board.columnNames.index(c)
                r = int(line[1:])
                if r < 1 or r > Board.rows:
                    raise ValueError
                return (r-1, c)
            except ValueError:
                print('Invalid input. Input should look like this: "A1" for the top-left corner. Or just "q" to quit.')
    def generateRandomBoard():
        b = Board()
        for x in Board.ships:
            while True:
                p = (int(random()*10), int(random()*10))
                d = int(random()*2)
                if b.shipLegal(p, x, d):
                    b.addShip(p, x, d)
                    break
        return b
    def formatMove(move):
        return '{}{}'.format(Board.columnNames[move[1]], move[0] + 1)

    # Initialization
    def __init__(self):
        # 0 for nothing, 1 for unhit ship, 2 for miss, 3 for hit ship
        self.board = [[0 for y in range(Board.cols)] for x in range(Board.rows)]

    def gameOver(self):
        for row in self.board:
            if 1 in row: return False
        return True

    # Placing ships
    def shipLegal(self, position, length, direction):
        if position is None or direction is None or length < 1:
            return False
        if direction == 0: # horizontal
            if position[1] + length > Board.cols:
                return False
            for x in range(length):
                if self.board[position[0]][position[1]+x] != 0:
                    return False
        else:
            if position[0] + length > Board.rows:
                return False
            for x in range(length):
                if self.board[position[0]+x][position[1]] != 0:
                    return False
        return True
    def addShip(self, position, length, direction):
        if direction == 0:
            for x in range(length):
                self.board[position[0]][position[1]+x] = 1
        else:
            for x in range(length):
                self.board[position[0]+x][position[1]] = 1
        return

    # Attacking squares
    def hit(self, position):
        return self.board[position[0]][position[1]] > 1
    def takeHit(self, position):
        self.board[position[0]][position[1]] += 2

    # Printing
    def printPartial(self): # for opponent's board
        res = '  ' + Board.columnNames + '\n'
        for row in range(Board.rows):
            res += '{:2}'.format(row+1)
            for col in range(Board.cols):
                if self.board[row][col] == 0:
                    res += coloredText('-', 'black', 'blue')
                if self.board[row][col] == 1:
                    res += coloredText('-', 'black', 'blue')
                if self.board[row][col] == 2:
                    res += coloredText('X', 'red', 'blue')
                if self.board[row][col] == 3:
                    res += coloredText('O', 'green', 'white')
            res += '\n'
        return res
    def printFull(self): # for player's own board
        res = '  ' + Board.columnNames + '\n'
        for row in range(Board.rows):
            res += '{:2}'.format(row+1)
            for col in range(Board.cols):
                if self.board[row][col] == 0:
                    res += coloredText('-', 'black', 'blue')
                if self.board[row][col] == 1:
                    res += coloredText('-', 'black', 'white')
                if self.board[row][col] == 2:
                    res += coloredText('X', 'green', 'blue')
                if self.board[row][col] == 3:
                    res += coloredText('O', 'red', 'white')
            res += '\n'
        return res
    def __str__(self):
        return self.printFull()
