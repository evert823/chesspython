#We convert each stepper or leaper to corresponding slider, and add maxrange1 in vectors
from os import listdir
from os.path import isfile, join
from chesspiecetype import chesspiecetype

def GetFiles(mypath):
    myfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return myfiles

def convert_chesspiecetype(pfilename):
    print(pfilename)
    pt.LoadFromJsonFile(infolder + "\\" + pfilename)
    convert_object()
    pt.SaveAsJsonFile(outfolder + "\\" + pfilename)

def convert_object():
    for v in pt.stepleapmovevectors:
        v = (v[0], v[1], 1)
        pt.slidemovevectors.append(v)
    pt.stepleapmovevectors.clear()

    for v in pt.stepleapcapturevectors:
        v = (v[0], v[1], 1)
        pt.slidecapturevectors.append(v)
    pt.stepleapcapturevectors.clear()


pt = chesspiecetype()

infolder = ".\\piecedefinitions"
outfolder = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub\\piecedefinitions_converted"

a = GetFiles(infolder)

for mypiece in a:
    convert_chesspiecetype(mypiece)
