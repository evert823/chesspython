from chessgame import chessgame
from datetime import datetime
import random
import numpy as np

def ClearBoard(pposition, pboardwidth, pboardheight):
    for i in range(pboardwidth):
        for j in range(pboardheight):
            pposition.squares[j][i] = 0

def PutPiece(pposition, min_i, max_i, min_j, max_j, piecetypeno, colour):
    i = random.randint(min_i, max_i)
    j = random.randint(min_j, max_j)
    while pposition.squares[j][i] != 0:
        i = random.randint(min_i, max_i)
        j = random.randint(min_j, max_j)

    if colour == 1:
        pno = piecetypeno + 1
    elif colour == -1:
        pno = (piecetypeno + 1) * -1

    pposition.squares[j][i] = pno

def CreateOneRandomPosition(pposition, ppiecetypes, pboardwidth, pboardheight):
    minpawns = 4
    maxpawns = 8
    random.seed()
    ptcountwhite = []
    ptcountblack = []
    for pt in ppiecetypes:
        if pt.name == "King":
            n = 1
        elif pt.name == "Pawn":
            n = random.randint(minpawns, maxpawns)
        else:
            n = random.randint(0, 3)
        ptcountwhite.append(n)
    print(ptcountwhite)
    ptcountblack = []
    for pt in ppiecetypes:
        if pt.name == "King":
            n = 1
        elif pt.name == "Pawn":
            n = random.randint(minpawns, maxpawns)
        else:
            n = random.randint(0, 3)
        ptcountblack.append(n)
    print(ptcountblack)

    for i in range(len(ppiecetypes)):
        pt = ppiecetypes[i]
        if pt.name == "Pawn":
            for x in range(ptcountwhite[i]):
                PutPiece(pposition, 0, pboardwidth - 1, 1, pboardheight - 2, i, 1)
            for x in range(ptcountblack[i]):
                PutPiece(pposition, 0, pboardwidth - 1, 1, pboardheight - 2, i, -1)
        else:
            for x in range(ptcountwhite[i]):
                PutPiece(pposition, 0, pboardwidth - 1, 0, pboardheight - 1, i, 1)
            for x in range(ptcountblack[i]):
                PutPiece(pposition, 0, pboardwidth - 1, 0, pboardheight - 1, i, -1)





mychessgame = chessgame()

mychessgame.LoadFromJsonFile(".\\games\\setup01.json", ".\\positions\\empty8x8.json")
mychessgame.SaveAsJsonFile(".\\games_verify\\setup01.json", ".\\positions_verify\\empty8x8.json")

myval = 100.0
while myval >= 100.0 or myval <= -100.0:
    ClearBoard(mychessgame.mainposition, mychessgame.boardwidth, mychessgame.boardheight)
    CreateOneRandomPosition(mychessgame.mainposition, mychessgame.piecetypes, mychessgame.boardwidth, mychessgame.boardheight)
    myval, mymv, _ = mychessgame.Calculation_n_plies(mychessgame.mainposition, 1)

try:
    mymvstr = mymv.ShortNotation(mychessgame.piecetypes)
except:
    mymvstr = "No move"
print(f"Result of evaluation : {myval} {mymvstr}")

mychessgame.SaveAsJsonFile(".\\games_verify\\setup01.json", ".\\positions_verify\\random_01.json")
