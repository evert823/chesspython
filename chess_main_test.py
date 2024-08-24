from chessgame import chessgame
from datetime import datetime

def Test(pchessgame, pgamefilename, ppositionfilename, n_plies):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions_verify\\" + ppositionfilename + ".json")
    
    pchessgame.display_when_n_plies_gt = n_plies - 2
    pchessgame.presort_when_n_plies_gt = 6

    print(datetime.now())
    print(f"Running evaluation {n_plies} plies {ppositionfilename} ...")
    myval, mymv, _ = pchessgame.Calculation_n_plies(0, -100.0, 100.0, n_plies)
    try:
        mymvstr = mymv.ShortNotation(pchessgame.piecetypes)
    except:
        mymvstr = "No move"
    print(f"Result of evaluation {n_plies} plies {ppositionfilename}: {myval} {mymvstr}")
    print(datetime.now())


def ProcessTestPosition(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions_verify\\" + ppositionfilename + ".json")
    a = pchessgame.mainposition.Position2MoveList(pchessgame.piecetypes)
    file2 = open(".\\movelists\\" + ppositionfilename + ".txt", "w")
    s = ""
    for i in range(len(a)):
        s += a[i].ShortNotation(pchessgame.piecetypes)
        if i < len(a) - 1:
            s += "|"
    file2.write(s + "\n")
    file2.write("\n")
    for mv in a:
        file2.write(mv.JsonString(pchessgame.piecetypes) + "\n")
    file2.write("\n")

    file2.write("\n")
    file2.close()


def SwapPosition(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.mainposition = pchessgame.SwapBlackWhite(pchessgame.mainposition)
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + "_reversed.json")

def Json2FEN(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    a = pchessgame.mainposition.PositionAsFEN(pchessgame.piecetypes)
    print(a)

def FEN2Json(pchessgame, pgamefilename, ppositionfilename, pfen):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f".\\positions\\mainposition.json")
    pchessgame.mainposition.PositionFromFEN(pfen, pchessgame.piecetypes)
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")

mylocalpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
mychessgame = chessgame(mylocalpath)

#ProcessTestPosition(mychessgame, "maingame", "mainposition")
#ProcessTestPosition(mychessgame, "maingame", "whitepawn")
#ProcessTestPosition(mychessgame, "maingame", "blackpawn")
#ProcessTestPosition(mychessgame, "maingame", "blackcastle")
#ProcessTestPosition(mychessgame, "maingame", "whitepromote")
#ProcessTestPosition(mychessgame, "maingame", "blackpromote")
#ProcessTestPosition(mychessgame, "maingame", "testposition")

#SwapPosition(mychessgame, "maingame", "08A_stalemate_2_white")
#Json2FEN(mychessgame, "maingame", "mate_03_reversed")
#FEN2Json(mychessgame, "maingame", "loadedfromfen", "3k4/2n3q1/2n5/2p5/2K5/8/8/8 b")
#Json2FEN(mychessgame, "maingame", "loadedfromfen")

Test(mychessgame, "maingame", "mate_in_5_for_white_BN", 10)
