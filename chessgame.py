import json
from chesspiecetype import chesspiecetype
from chessposition import chessposition
from chessmove import chessmove
import copy

class chessgame:
    def __init__(self):
        self.boardwidth = -1
        self.boardheight = -1
        self.piecetypes = []

        self.mainposition = chessposition()
#---------------------------------------------------------------------------------------------------------
    def LoadFromJsonFile(self, pfilename, ppositionfilename):
        #Load from json file and convert to class structure
        gamefile = open(pfilename, 'r')
        gamedict = json.load(gamefile)
        gamefile.close()
        self.boardwidth = gamedict["boardwidth"]
        self.boardheight = gamedict["boardheight"]

        self.piecetypes.clear()
        for p in gamedict["piecetypes"]:
            self.LoadPiece(p)

        self.mainposition.LoadFromJsonFile(ppositionfilename, self.piecetypes)
        self.boardwidth = self.mainposition.boardwidth
        self.boardheight = self.mainposition.boardheight
#---------------------------------------------------------------------------------------------------------
    def SaveAsJsonFile(self, pfilename, ppositionfilename):
        #Convert class structure to json and save as json file
        gamefile = open(pfilename, 'w')
        gamedict = {}
        gamedict["boardwidth"] = self.boardwidth
        gamedict["boardheight"] = self.boardheight

        gamedict["piecetypes"] = []
        for p in self.piecetypes:
            gamedict["piecetypes"].append(p.name)

        json.dump(gamedict, gamefile, indent=4)
        gamefile.close()

        self.mainposition.SaveAsJsonFile(ppositionfilename, self.piecetypes)
#---------------------------------------------------------------------------------------------------------
    def LoadPiece(self, ppiecename):
        mytype = chesspiecetype()
        mytype.LoadFromJsonFile(".\\piecedefinitions\\" + ppiecename + ".json")
        mylocalpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
        mytype.SaveAsJsonFile(f"{mylocalpath}\\piecedefinitions_verify\\" + ppiecename + ".json")
        self.piecetypes.append(mytype)
#---------------------------------------------------------------------------------------------------------
    def ExecuteMove(self, pposition, pmove):
        myresultpos = copy.deepcopy(pposition)
        myresultpos.ClearNonPersistent()

        i1 = pmove.coordinates[0]
        j1 = pmove.coordinates[1]
        i2 = pmove.coordinates[2]
        j2 = pmove.coordinates[3]

        myresultpos.precedingmove = (i1, j1, i2, j2)

        if pmove.PromoteToPiece != 0:
            myresultpos.squares[j2][i2] = pmove.PromoteToPiece
        else:
            myresultpos.squares[j2][i2] = pmove.MovingPiece
        myresultpos.squares[j1][i1] = 0

        #Set castling info for new position BEGIN
        pt = self.piecetypes[abs(pmove.MovingPiece) - 1]
        i_k, i_qr, i_kr = pposition.LocateKingRooks4Castling(self.piecetypes)

        if pt.name == "King" and pt.IsRoyal == True:
            if pposition.colourtomove == 1:
                myresultpos.whitekinghasmoved = True
            else:
                myresultpos.blackkinghasmoved = True
        elif pt.name == "Rook":
            if pposition.colourtomove == 1:
                if i1 == i_qr:
                    myresultpos.whitequeensiderookhasmoved = True
                elif i1 == i_kr:
                    myresultpos.whitekingsiderookhasmoved = True
            else:
                if i1 == i_qr:
                    myresultpos.blackqueensiderookhasmoved = True
                elif i1 == i_kr:
                    myresultpos.blackkingsiderookhasmoved = True
        #Set castling info for new position END

        if pmove.IsEnPassant == True:
            io1 = pmove.othercoordinates[0]
            jo1 = pmove.othercoordinates[1]
            myresultpos.squares[jo1][io1] = 0

        if pmove.IsCastling == True:
            io1 = pmove.othercoordinates[0]
            jo1 = pmove.othercoordinates[1]
            io2 = pmove.othercoordinates[2]
            jo2 = pmove.othercoordinates[3]
            otherpiece = myresultpos.squares[jo1][io1]
            myresultpos.squares[jo1][io1] = 0
            myresultpos.squares[jo2][io2] = otherpiece

        if pposition.colourtomove == 1:
            myresultpos.colourtomove = -1
        else:
            myresultpos.colourtomove = 1

        return myresultpos
#---------------------------------------------------------------------------------------------------------
    def Calculation_n_plies(self, pposition, n_plies):
        #response must be tuple len 3 (x, y, z)
        #x = evaluation float
        #y = chessmove object instance
        #z = boolean Yes if opponent's King in check else No

        evalresult = pposition.StaticEvaluation(self.piecetypes)

        if evalresult in (-100.0, 100.0):
            return (evalresult, None, False)

        pposition.ScanAttacked(self.piecetypes)

        if pposition.POKingIsInCheck() == True:
            if pposition.colourtomove == 1:
                evalresult = 100.0
            else:
                evalresult = -100.0
            return (evalresult, None, True)

        if n_plies == 0:
            return (evalresult, None, False)

        movelist = pposition.Position2MoveList(self.piecetypes)
        subresults = []

        if pposition.colourtomove == 1:
            goodenoughstopvalue = 100.0
        else:
            goodenoughstopvalue = -100.0

        noescapecheck = True
        for i in range(len(movelist)):
            #print(movelist[i].ShortNotation(self.piecetypes))
            newpos = self.ExecuteMove(pposition, movelist[i])
            newvalue, _, me_in_check = self.Calculation_n_plies(newpos, n_plies - 1)
            if me_in_check == False:
                noescapecheck = False
            subresults.append((i, newvalue))

            if pposition.colourtomove == 1:
                if newvalue >= goodenoughstopvalue:
                    break
            else:
                if newvalue <= goodenoughstopvalue:
                    break

        #Mate
        if pposition.PMKingIsInCheck() == True and noescapecheck == True:
            if pposition.colourtomove == 1:
                evalresult = -100.0
            else:
                evalresult = 100.0
            return (evalresult, None, False)
        #Stalemate
        if pposition.PMKingIsInCheck() == False and noescapecheck == True:
            evalresult = 0.0
            return (evalresult, None, False)

        if pposition.colourtomove == 1:
            res_sorted = sorted(subresults, key=lambda tup: tup[1], reverse=True)
        else:
            res_sorted = sorted(subresults, key=lambda tup: tup[1], reverse=False)

        evalresult = res_sorted[0][1]
        bestmove = copy.deepcopy(movelist[res_sorted[0][0]])

        return (evalresult, bestmove, False)
#---------------------------------------------------------------------------------------------------------
    def SwapBlackWhite(self, pposition):
        #For testing purposes - create same position with reversed colours and mirrored
        myresultpos = chessposition()

        myresultpos.ResetBoardsize(pposition.boardwidth, pposition.boardheight)

        myresultpos.colourtomove = pposition.colourtomove * -1

        if pposition.precedingmove[0] > -1:
            a = (pposition.precedingmove[0], 
                (pposition.boardheight - 1) - pposition.precedingmove[1],
                pposition.precedingmove[2],
                (pposition.boardheight - 1) - pposition.precedingmove[3])
            myresultpos.precedingmove = a

        myresultpos.whitekinghasmoved = pposition.blackkinghasmoved
        myresultpos.whitekingsiderookhasmoved = pposition.blackkingsiderookhasmoved
        myresultpos.whitequeensiderookhasmoved = pposition.blackqueensiderookhasmoved
        myresultpos.blackkinghasmoved = pposition.whitekinghasmoved
        myresultpos.blackkingsiderookhasmoved = pposition.whitekingsiderookhasmoved
        myresultpos.blackqueensiderookhasmoved = pposition.whitequeensiderookhasmoved

        for i in range(myresultpos.boardwidth):
            for j in range(myresultpos.boardheight):
                i2 = i
                j2 = (myresultpos.boardheight - 1) - j
                myresultpos.squares[j][i] = pposition.squares[j2][i2] * -1

        myresultpos.ClearNonPersistent()

        return myresultpos
