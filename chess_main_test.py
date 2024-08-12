from chessgame import chessgame


def TestExecuteMove(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(".\\games_verify\\" + pgamefilename + ".json", ".\\positions_verify\\" + ppositionfilename + ".json")
    a = pchessgame.Position2MoveList(pchessgame.mainposition)

    mycounter = 0
    for i in range(len(a)):
        pos1 = pchessgame.ExecuteMove(pchessgame.mainposition, a[i])
        a2 = pchessgame.Position2MoveList(pos1)
        for i2 in range(len(a2)):
            pos2 = pchessgame.ExecuteMove(pos1, a2[i2])
            mycounter += pos2.colourtomove
            if mycounter % 10000 == 0:
                print(f"mycounter : {mycounter}")


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

    for j in range(pchessgame.boardheight -1,-1,-1):
        s = ""
        for i in range(pchessgame.boardheight):
            if pchessgame.mainposition.IsAttacked[j][i] == True:
                s += 'X'
            else:
                s += '.'
        file2.write(s + "\n")

    file2.write("\n")
    file2.close()


mychessgame = chessgame()

#ProcessTestPosition(mychessgame, "maingame", "mainposition")
#ProcessTestPosition(mychessgame, "maingame", "whitecastle")
#ProcessTestPosition(mychessgame, "maingame", "blackcastle")
#ProcessTestPosition(mychessgame, "maingame", "whitepromote")
#ProcessTestPosition(mychessgame, "maingame", "blackpromote")

ProcessTestPosition(mychessgame, "maingame", "testposition")

TestExecuteMove(mychessgame, "maingame", "testposition")
