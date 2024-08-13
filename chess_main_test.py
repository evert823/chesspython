from chessgame import chessgame
from datetime import datetime

def Test(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(".\\games_verify\\" + pgamefilename + ".json", ".\\positions_verify\\" + ppositionfilename + ".json")
    
    print(datetime.now())
    myval, mymv = pchessgame.Calculation_n_plies(pchessgame.mainposition, 4)
    mymvstr = mymv.ShortNotation(pchessgame.piecetypes)
    print(f"PM in check True/False : {pchessgame.mainposition.PMKingIsInCheck()}")
    print(f"PO in check True/False : {pchessgame.mainposition.POKingIsInCheck()}")
    print(f"Result of evaluation : {myval} {mymvstr}")
    print(datetime.now())


def ProcessTestPosition(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(".\\games_verify\\" + pgamefilename + ".json", ".\\positions_verify\\" + ppositionfilename + ".json")
    a = pchessgame.Position2MoveList(pchessgame.mainposition)
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


mychessgame = chessgame()

#ProcessTestPosition(mychessgame, "maingame", "mainposition")
#ProcessTestPosition(mychessgame, "maingame", "whitecastle")
#ProcessTestPosition(mychessgame, "maingame", "blackcastle")
#ProcessTestPosition(mychessgame, "maingame", "whitepromote")
#ProcessTestPosition(mychessgame, "maingame", "blackpromote")
ProcessTestPosition(mychessgame, "maingame", "testposition")

Test(mychessgame, "maingame", "mate_in_2_for_black")
