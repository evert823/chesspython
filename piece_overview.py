from chessgame import chessgame
from os import listdir
from os.path import isfile, join

def GetFiles(mypath):
    myfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return myfiles

def GetAllPieceDefinitions(pchessgame, piecefilelist):
    for f in piecefilelist:
        p = f.replace(".json", "")
        pchessgame.LoadPiece(p, mylocalpath)
    print(len(pchessgame.piecetypes))
    for p in pchessgame.piecetypes:
        print(f"piecename {p.name} symbol {p.symbol}")

mylocalpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
mychessgame = chessgame(mylocalpath)

a = GetFiles(".\\piecedefinitions")
GetAllPieceDefinitions(mychessgame, a)
