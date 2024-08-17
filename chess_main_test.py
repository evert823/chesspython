from chessgame import chessgame
from datetime import datetime

def Test(pchessgame, pgamefilename, ppositionfilename, n_plies):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions_verify\\" + ppositionfilename + ".json")
    
    print(datetime.now())
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
mychessgame = chessgame()

#ProcessTestPosition(mychessgame, "maingame", "mainposition")
#ProcessTestPosition(mychessgame, "maingame", "whitepawn")
#ProcessTestPosition(mychessgame, "maingame", "blackpawn")
#ProcessTestPosition(mychessgame, "maingame", "blackcastle")
#ProcessTestPosition(mychessgame, "maingame", "whitepromote")
#ProcessTestPosition(mychessgame, "maingame", "blackpromote")
#ProcessTestPosition(mychessgame, "maingame", "testposition")

#SwapPosition(mychessgame, "maingame", "Archbishop_mate_04_black")
Test(mychessgame, "maingame", "mate_in_4_for_black_BN", 8)
Test(mychessgame, "maingame", "mate_in_4_for_white_BN", 8)
