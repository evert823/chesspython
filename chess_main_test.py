from chessgame import chessgame
from datetime import datetime

def Test(pchessgame, pgamefilename, ppositionfilename, n_plies):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions_verify\\" + ppositionfilename + ".json")
    
    pchessgame.display_when_n_plies_gt = n_plies - 2
    pchessgame.presort_when_n_plies_gt = 5

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

#SwapPosition(mychessgame, "maingame", "mate_in_5_for_white_morepieces")
#Json2FEN(mychessgame, "maingame", "mate_03_reversed")
#FEN2Json(mychessgame, "maingame", "mate_3_black_lichess_01", "Bn2r1k1/p4ppp/3Q4/2p3q1/8/2N4n/PPPP1P1P/R1B2R1K b")
#Json2FEN(mychessgame, "maingame", "loadedfromfen")

Test(mychessgame, "maingame", "mate_in_5_for_black_morepieces", 10)
