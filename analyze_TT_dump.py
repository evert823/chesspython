import json
from chessgame import chessgame

from os import listdir
from os.path import isfile, join

def GetFiles(ppath):
    onlyfiles = [f for f in listdir(ppath) if isfile(join(ppath, f))]
    a = []
    for x in onlyfiles:
        if x.endswith(".log.transpositiontable.json"):
            a.append(x)
    return a

def Read_one_TT_dump(ppath, pfilename):
    ttfile = open(ppath + "\\" + pfilename, 'r')
    ttdict = json.load(ttfile)
    ttfile.close()
    s = ttdict["TransTable_no_items_available"]
    lastitem = ttdict["TranspositionTable"][int(s) - 1]
    checkdepth = int(lastitem["used_depth"])
    checkscore = float(lastitem["calculated_value"])
    return checkdepth, checkscore


mylocalpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
mychessgame = chessgame(mylocalpath)

mylogfolder = f"{mylocalpath}\\log"
myfilelist = GetFiles(mylogfolder)

totalpositions = 0
totalscore = 0.0
totalpositions_nomate = 0
totalscore_nomate = 0.0

for mytt in myfilelist:
    mydepth, myscore = Read_one_TT_dump(mylogfolder, mytt)
    if mydepth == 7:
        totalpositions += 1
        totalscore += myscore
        if myscore < -95 or myscore > 95:
            print(f"mytt {mytt} mydepth {mydepth} myscore {myscore}")
        else:
            totalpositions_nomate += 1
            totalscore_nomate += myscore
    else:
        print(f"mytt {mytt} mydepth {mydepth}")

print(f"number of positions {totalpositions} score {totalscore} avg {totalscore / totalpositions}")
print(f"number of positions {totalpositions_nomate} score {totalscore_nomate} avg {totalscore_nomate / totalpositions_nomate}")

