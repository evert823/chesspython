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

def TuneCastlingInfo(pposition, ppiecetypes):
    pposition.whitekinghasmoved = True
    pposition.whitekingsiderookhasmoved = True
    pposition.whitequeensiderookhasmoved = True
    pposition.blackkinghasmoved = True
    pposition.blackkingsiderookhasmoved = True
    pposition.blackqueensiderookhasmoved = True

def CreateOneRandomPosition(pposition, ppiecetypes, pboardwidth, pboardheight):
    minpawns = 4
    maxpawns = 8
    random.seed()
    ptcountwhite = []
    ptcountblack = []

    mycolourtomove = random.randint(-1, 1)
    while mycolourtomove == 0:
        mycolourtomove = random.randint(-1, 1)
    pposition.colourtomove = mycolourtomove

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

def CreateHunterEndgame(pposition, ppiecetypes, pboardwidth, pboardheight):
    for i in range(len(ppiecetypes)):
        pt = ppiecetypes[i]
        if pt.name == "King":
            PutPiece(pposition, 0, 3, 0, 3, i, -1)
            PutPiece(pposition, 0, 4, 0, 5, i, 1)
        elif pt.name == "Hunter":
            PutPiece(pposition, 0, 5, 0, 4, i, 1)
        elif pt.name == "Bishop":
            PutPiece(pposition, 0, 7, 0, 7, i, 1)
        elif pt.name == "Knight":
            PutPiece(pposition, 0, 6, 0, 6, i, 1)

def CreateRandom_main():
    myval = 100.0
    while myval >= 100.0 or myval <= -100.0:
        ClearBoard(mychessgame.mainposition, mychessgame.mainposition.boardwidth, mychessgame.mainposition.boardheight)
        CreateOneRandomPosition(mychessgame.mainposition, mychessgame.piecetypes, mychessgame.mainposition.boardwidth, mychessgame.mainposition.boardheight)
        TuneCastlingInfo(mychessgame.mainposition, mychessgame.piecetypes)
        myval, movei, _ = mychessgame.Calculation_n_plies(1)

    try:
        mymvstr = mychessgame.mainposition.movelist[movei].ShortNotation(mychessgame.piecetypes)
    except:
        mymvstr = "No move"
    print(f"Result of evaluation : {myval} {mymvstr}")

    mychessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\setup01.json", f"{mylocalpath}\\positions_verify\\random_01.json")

    myval, movei, _ = mychessgame.Calculation_n_plies(4)
    try:
        mymvstr = mychessgame.mainposition.movelist[movei].ShortNotation(mychessgame.piecetypes)
    except:
        mymvstr = "No move"
    print(f"Result of evaluation : {myval} {mymvstr}")

def CreateHunter_main():
    random.seed()
    myval = 100.0
    myval2 = 50.0

    myseq = 0

    while myval2 != 100.0:
        myval = 100.0
        while myval >= 100.0 or myval <= -100.0:
            ClearBoard(mychessgame.mainposition, mychessgame.mainposition.boardwidth, mychessgame.mainposition.boardheight)
            CreateHunterEndgame(mychessgame.mainposition, mychessgame.piecetypes, mychessgame.mainposition.boardwidth, mychessgame.mainposition.boardheight)
            TuneCastlingInfo(mychessgame.mainposition, mychessgame.piecetypes)
            myval, movei, _ = mychessgame.Calculation_n_plies(3)

        try:
            mymvstr = mychessgame.mainposition.movelist[movei].ShortNotation(mychessgame.piecetypes)
        except:
            mymvstr = "No move"
        print(f"Result of evaluation : {myval} {mymvstr}")

        myseq += 1
        mychessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\setup01.json", f"{mylocalpath}\\positions_verify\\huntermate_{myseq}.json")

        print(f"Starting deeper calculation on this one {datetime.now()}")
        myval2, movei, _ = mychessgame.Calculation_n_plies(8)
        try:
            mymvstr = mychessgame.mainposition.movelist[movei].ShortNotation(mychessgame.piecetypes)
        except:
            mymvstr = "No move"
        print(f"Result of evaluation : {myval2} {mymvstr}")
        print(f"Ended the deeper calculation {datetime.now()}")

mylocalpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
mychessgame = chessgame(mylocalpath)

mychessgame.LoadFromJsonFile(".\\games\\setup01.json", f"{mylocalpath}\\positions\\empty8x8.json")
mychessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\setup01.json", f"{mylocalpath}\\positions_verify\\empty8x8.json")

CreateHunter_main()
