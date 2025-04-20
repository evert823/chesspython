from chessgame import chessgame
from os import listdir
from os.path import isfile, join

def GetFiles(mypath):
    myfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return myfiles

def ConvertAll(pchessgame, piecefilelist):
    for f in piecefilelist:
        if f.find("random_mate_") > -1:
            #print(f"{mylocalpath}\\randompositions\\{f}.json")
            pchessgame.LoadFromJsonFile(".\\games\\maingame.json", f"{mylocalpath}\\randompositions\\{f}")
            a = pchessgame.mainposition.PositionAsFEN(pchessgame.piecetypes)
            print(f"{f}|{a}")

mylocalpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
mychessgame = chessgame(mylocalpath)

a = GetFiles("C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub\\randompositions")
ConvertAll(mychessgame, a)
