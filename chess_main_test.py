from chessgame import chessgame
from datetime import datetime

def Test(pchessgame, pgamefilename, ppositionfilename, n_plies):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions_verify\\" + ppositionfilename + ".json")
    
    #pchessgame.display_when_n_plies_gt = n_plies - 2

    print(datetime.now())
    print(f"Running evaluation {n_plies} plies {ppositionfilename} ...")
    myval, mymv, _ = pchessgame.Calculation_n_plies(pchessgame.mainposition, -100.0, 100.0, n_plies)
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
#Test(mychessgame, "maingame", "mate_in_4_for_white_hard_chesscom", 8) #several days !!!

Test(mychessgame, "maingame", "08A_stalemate_2_white", 5)
Test(mychessgame, "maingame", "08A_stalemate_2_black", 5)
