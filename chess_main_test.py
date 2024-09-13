from chessgame import chessgame
from datetime import datetime

def Test(pchessgame, pgamefilename, ppositionfilename, n_plies):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions_verify\\" + ppositionfilename + ".json")
    
    pchessgame.display_when_n_plies_gt = 6
    pchessgame.presort_when_n_plies_gt = 4

    print(datetime.now())
    print(f"Running evaluation {n_plies} plies {ppositionfilename} ...")
    myval, mymvidx, _ = pchessgame.Calculation_n_plies(n_plies)
    s = f"List : {pchessgame.mainposition.DisplayMovelist(pchessgame.piecetypes)}"
    print(s)

    try:
        mymvstr = pchessgame.mainposition.movelist[mymvidx].ShortNotation(pchessgame.piecetypes)
    except:
        mymvstr = "No move"
    print(f"Result of evaluation {n_plies} plies {ppositionfilename}: {myval} {mymvstr}")
    print(datetime.now())

def SwapPosition(pchessgame, pgamefilename, ppositionfilename):
    newname = ppositionfilename + "_reversed"
    if ppositionfilename.find("white") > -1:
        newname = ppositionfilename.replace("white", "black")
    elif ppositionfilename.find("black") > -1:
        newname = ppositionfilename.replace("black", "white")

    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.mainposition = pchessgame.SwapBlackWhite(pchessgame.mainposition)
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + newname + ".json")

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

SwapPosition(mychessgame, "maingame", "mate_5_white_talkchesscom")
SwapPosition(mychessgame, "maingame", "mate_7_white_talkchesscom")
#Json2FEN(mychessgame, "maingame", "08A_stalemate_2_white")
#Json2FEN(mychessgame, "maingame", "pf_comparison_black")
#FEN2Json(mychessgame, "maingame", "testposition", "2k5/3p4/2p1pB2/N7/2K3B1/4N3/3R4/8 w - - 0 3")

#Test(mychessgame, "maingame", "pf_comparison_white", 10)
#Test(mychessgame, "maingame", "pf_comparison_black", 10)
