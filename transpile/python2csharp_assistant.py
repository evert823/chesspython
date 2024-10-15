import re

def FixCoordinates(myline):
    mycoordpattern = "\([0-9], [0-9], [0-9], [0-9]\)"
    myspan, mymatch = FindRegex(mycoordpattern, myline)
    if myspan[0] > -1:
        myresult = myline[:myspan[0]] + myline[myspan[0] + 1:myspan[1] - 1] + myline[myspan[1]:]
    else:
        myresult = myline
    return myresult

def Fixboardwidth(myline):
    if myline.find("<NumberOfFiles>") > -1:
        i1 = myline.find("<NumberOfFiles>")
        i2 = myline.find("</NumberOfFiles>")
        s12 = myline[i1 + 15:i2]
        return "    \"boardwidth\": " + s12 + ",\n"
    else:
        return myline

def Fixboardheight(myline):
    if myline.find("<NumberOfRanks>") > -1:
        i1 = myline.find("<NumberOfRanks>")
        i2 = myline.find("</NumberOfRanks>")
        s12 = myline[i1 + 15:i2]
        return "    \"boardheight\": " + s12 + ",\n"
    else:
        return myline

def FindRegex(ppattern, ptargetstring):
    a = re.search(ppattern, ptargetstring)
    try:
        b = a.span()
    except:
        b = (-1, -1)
    return b, ptargetstring[b[0]:b[1]]

def ReplaceRegex(ppattern, pnew, ptargetstring):
    a = re.sub(ppattern, pnew, ptargetstring)
    return a

def Transpile_assistant(infolder, infile, outfolder, outfile):
    file1 = open(infolder + infile, 'r')
    Lines = file1.readlines()
    file1.close()

    file2 = open(outfolder + outfile, 'w')

    foundranks = 0

    for line in Lines:
        if line.find("<Rank>") > -1:
            foundranks += 1
        line1 = line.replace("      <Rank>","         \"")

        if foundranks == 8:
            line1 = line1.replace("</Rank>","\"\n   ],")
        else:
            line1 = line1.replace("</Rank>","\",")


        line1 = line1.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>","{")
        line1 = line1.replace("<Game>","")
        line1 = line1.replace("</Game>","}")
        line1 = line1.replace("<NumberOfPositionsInGame>1</NumberOfPositionsInGame>","")
        line1 = line1.replace("<CastleDistance>3</CastleDistance>","")
        line1 = line1.replace("<Position>","")
        line1 = line1.replace("    <Squares>","    \"squares\": [")
        line1 = line1.replace("</Squares>","")
        line1 = line1.replace("<CastleWhiteRightBlockedPerm>true</CastleWhiteRightBlockedPerm>","")
        line1 = line1.replace("<CastleWhiteLeftBlockedPerm>true</CastleWhiteLeftBlockedPerm>","")
        line1 = line1.replace("<CastleBlackRightBlockedPerm>true</CastleBlackRightBlockedPerm>","")
        line1 = line1.replace("<CastleBlackLeftBlockedPerm>true</CastleBlackLeftBlockedPerm>","")
        line1 = line1.replace("<FiftyMovesRulePlyCount>0</FiftyMovesRulePlyCount>","")
        line1 = line1.replace("<RepetitionCount>0</RepetitionCount>","")
        line1 = line1.replace("</Position>","")
        line1 = line1.replace("aaa","")
        line1 = line1.replace("aaa","")
        line1 = line1.replace("aaa","")
        line1 = line1.replace("aaa","")
        line1 = line1.replace("aaa","")
        line1 = line1.replace("aaa","")
        line1 = line1.replace("aaa","")
        line1 = line1.replace("    <ColourToMove>b</ColourToMove>","    \"colourtomove\": -1")
        line1 = line1.replace("    <ColourToMove>w</ColourToMove>","    \"colourtomove\": 1")
        line1 = Fixboardwidth(line1)
        line1 = Fixboardheight(line1)

        if line1.replace("\n", "").strip() != "":
            if line1.find("Enrich") == -1 and line1.find("AllMov") == -1 and line1.find("<Move>") == -1:
                file2.write(line1)

    file2.close()


infolder = "Q:\\Persoonlijk\\Wiskunde en programmeren\\C#\\WeirdEngine\\import_export_examples\\"
outfolder = ".\\"

Transpile_assistant(infolder, "bulldog_mate_5_plies" + ".xml", outfolder, "bulldog_mate_5_plies" + ".json")
Transpile_assistant(infolder, "bulldog_mate_6" + ".xml", outfolder, "bulldog_mate_6" + ".json")
Transpile_assistant(infolder, "mate_5_from_mate_6_tug" + ".xml", outfolder, "mate_5_from_mate_6_tug" + ".json")
