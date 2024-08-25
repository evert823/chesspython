from chessgame import chessgame
from datetime import datetime

def Test(pchessgame, pgamefilename, ppositionfilename, n_plies):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions_verify\\" + ppositionfilename + ".json")
    
    pchessgame.display_when_n_plies_gt = n_plies - 2
    pchessgame.presort_when_n_plies_gt = 6

    print(datetime.now())
    print(f"Running evaluation {n_plies} plies {ppositionfilename} ...")
    myval, mymvidx, _ = pchessgame.Calculation_n_plies(n_plies)
    try:
        mymvstr = pchessgame.mainposition.movelist[mymvidx].ShortNotation(pchessgame.piecetypes)
    except:
        mymvstr = "No move"
    print(f"Result of evaluation {n_plies} plies {ppositionfilename}: {myval} {mymvstr}")
    print(datetime.now())

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

#SwapPosition(mychessgame, "maingame", "08A_stalemate_2_white")
#Json2FEN(mychessgame, "maingame", "mate_03_reversed")
#FEN2Json(mychessgame, "maingame", "mate_3_black_hard", "r1b2rk1/pppp1ppp/8/2b1p3/2B1P1nq/2N2N2/PPP2PPP/R1BQR1K1 b")
#Json2FEN(mychessgame, "maingame", "loadedfromfen")

Test(mychessgame, "maingame", "mate_3_black_hard", 6)
