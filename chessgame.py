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
        mytype.SaveAsJsonFile(".\\piecedefinitions_verify\\" + ppiecename + ".json")
        self.piecetypes.append(mytype)
#---------------------------------------------------------------------------------------------------------
    def Position2MoveList(self, pposition):
        pposition.InitIsAttacked()

        MoveList = []
        for i in range(self.boardwidth):
            for j in range(self.boardheight):
                if ((pposition.squares[j][i] > 0 and pposition.colourtomove > 0) or
                    (pposition.squares[j][i] < 0 and pposition.colourtomove < 0)):
                    MoveList.extend(self.GetStepLeapMoves(pposition, i, j))
                    MoveList.extend(self.GetSlideMoves(pposition, i, j))
                    MoveList.extend(self.GetStepLeapCaptures(pposition, i, j))
                    MoveList.extend(self.GetSlideCaptures(pposition, i, j))
                    MoveList.extend(self.GetPawn2StepMoves(pposition, i, j))
                    MoveList.extend(self.GetPawnEnPassantMoves(pposition, i, j))
        MoveList.extend(self.GetCastling(pposition))

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetStepLeapMoves(self, pposition, i, j):
        MoveList = []
        #print(f"GetStepLeaveMoves({i},{j})")

        pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]

        for v in pt.stepleapmovevectors:
            i2 = i + v[0]

            if pposition.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            if i2 >= 0 and i2 < self.boardwidth:
                if j2 >= 0 and j2 < self.boardheight:
                    if pposition.squares[j2][i2] == 0:
                        mv = chessmove(i, j, i2, j2)
                        mv.MovingPiece = pposition.squares[j][i]
                        MoveList.extend(self.GetPromotion(mv))

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetSlideMoves(self, pposition, i, j):
        MoveList = []
        #print(f"GetSlideMoves({i},{j})")

        pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]
        
        for v in pt.slidemovevectors:
            i2 = i + v[0]

            if pposition.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False):
                if pposition.squares[j2][i2] == 0:
                    mv = chessmove(i, j, i2, j2)
                    mv.MovingPiece = pposition.squares[j][i]
                    MoveList.extend(self.GetPromotion(mv))
                else:
                    blocked = True

                i2 = i2 + v[0]

                if pposition.colourtomove == 1:
                    j2 = j2 + v[1]
                else:
                    j2 = j2 - v[1]

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetStepLeapCaptures(self, pposition, i, j):
        MoveList = []
        #print(f"GetStepLeaveCaptures({i},{j})")

        pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]
        if pt.IsDivergent == False:
            lookatvectors = pt.stepleapmovevectors
        else:
            lookatvectors = pt.stepleapcapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if pposition.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            if i2 >= 0 and i2 < self.boardwidth:
                if j2 >= 0 and j2 < self.boardheight:
                    pposition.IsAttacked[j2][i2] = True
                    if ((pposition.squares[j2][i2] > 0 and pposition.squares[j][i] < 0) or
                        (pposition.squares[j2][i2] < 0 and pposition.squares[j][i] > 0)):
                        mv = chessmove(i, j, i2, j2)
                        mv.MovingPiece = pposition.squares[j][i]
                        mv.IsCapture = True
                        MoveList.extend(self.GetPromotion(mv))

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetSlideCaptures(self, pposition, i, j):
        MoveList = []
        #print(f"GetSlideCaptures({i},{j})")

        pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]

        if pt.IsDivergent == False:
            lookatvectors = pt.slidemovevectors
        else:
            lookatvectors = pt.slidecapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if pposition.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False):

                pposition.IsAttacked[j2][i2] = True
                if ((pposition.squares[j2][i2] > 0 and pposition.squares[j][i] < 0) or
                    (pposition.squares[j2][i2] < 0 and pposition.squares[j][i] > 0)):
                    mv = chessmove(i, j, i2, j2)
                    mv.MovingPiece = pposition.squares[j][i]
                    mv.IsCapture = True
                    MoveList.extend(self.GetPromotion(mv))
                    blocked = True
                elif pposition.squares[j2][i2] != 0:
                    blocked = True

                i2 = i2 + v[0]

                if pposition.colourtomove == 1:
                    j2 = j2 + v[1]
                else:
                    j2 = j2 - v[1]

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetPawn2StepMoves(self, pposition, i, j):
        MoveList = []

        pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]

        if pt.name != "Pawn":
            return MoveList
        if pposition.colourtomove > 0 and j != 1:
            return MoveList
        if pposition.colourtomove < 0 and j != pposition.boardheight - 2:
            return MoveList

        i2 = i
        i_skip = i
        if pposition.colourtomove > 0:
            j_skip = j + 1
            j2 = j + 2
        else:
            j_skip = j - 1
            j2 = j - 2
        if pposition.squares[j_skip][i_skip] == 0 and pposition.squares[j2][i2] == 0:
            mv = chessmove(i, j, i2, j2)
            mv.MovingPiece = pposition.squares[j][i]
            MoveList.append(mv)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetPawnEnPassantMoves(self, pposition, i, j):
        MoveList = []

        pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]

        if pt.name != "Pawn":
            return MoveList
        if pposition.precedingmove[3] != j:
            return MoveList

        x_from = pposition.precedingmove[0]
        y_from = pposition.precedingmove[1]
        x_to = pposition.precedingmove[2]
        y_to = pposition.precedingmove[3]
        ptm = self.piecetypes[abs(pposition.squares[y_to][x_to]) - 1]
        if ptm.name != "Pawn":
            return MoveList
        if x_from - i == 1 or x_from - i == -1:
            pass
        else:
            return MoveList
        
        if pposition.colourtomove > 0:
            if pposition.squares[y_to][x_to] > 0:
                return MoveList
            if j != pposition.boardheight - 4:
                return MoveList
            if y_from != y_to + 2:
                return MoveList
            mv = chessmove(i, j, x_from, y_to + 1)
            mv.MovingPiece = pposition.squares[j][i]
            mv.IsEnPassant = True
            mv.othercoordinates = (x_to, y_to, -1, -1)
            mv.IsCapture = True
            MoveList.append(mv)

        if pposition.colourtomove < 0:
            if pposition.squares[y_to][x_to] < 0:
                return MoveList
            if j != 3:
                return MoveList
            if y_from != y_to - 2:
                return MoveList
            mv = chessmove(i, j, x_from, y_to - 1)
            mv.MovingPiece = pposition.squares[j][i]
            mv.IsEnPassant = True
            mv.othercoordinates = (x_to, y_to, -1, -1)
            mv.IsCapture = True
            MoveList.append(mv)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetCastling(self, pposition):
        mykingsymbol = ""
        MoveList = []
        if pposition.colourtomove == 1:
            if pposition.whitekinghasmoved == True:
                return MoveList
            j = 0
        if pposition.colourtomove == -1:
            if pposition.blackkinghasmoved == True:
                return MoveList
            j = self.boardheight - 1


        #Now locate King and Rooks
        i_k = -1
        i_qr = -1
        i_kr = -1
        for i in range(self.boardwidth):
            pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]
            if (pt.name == "Rook" and pposition.squares[j][i] * pposition.colourtomove > 0):
                if i_k == -1:
                    i_qr = i
                else:
                    i_kr = i
            elif (pt.name == "King" and pt.IsRoyal == True and pposition.squares[j][i] * pposition.colourtomove > 0):
                mykingsymbol = pt.symbol
                i_k = i

        queensidepossible = True
        kingsidepossible = True

        if pposition.colourtomove == 1 and pposition.whitequeensiderookhasmoved == True:
            queensidepossible = False
        if pposition.colourtomove == -1 and pposition.blackqueensiderookhasmoved == True:
            queensidepossible = False
        if pposition.colourtomove == 1 and pposition.whitekingsiderookhasmoved == True:
            kingsidepossible = False
        if pposition.colourtomove == -1 and pposition.blackkingsiderookhasmoved == True:
            kingsidepossible = False

        if i_qr > -1 and i_k > i_qr:
            pass
        else:
            queensidepossible = False

        if i_k > -1 and i_kr > i_k:
            pass
        else:
            kingsidepossible = False


        if queensidepossible:
            i_k_new = 2
            i_qr_new = i_k_new + 1
            for i in range(self.boardwidth):
                if ((i > i_qr and i <= i_qr_new) or (i < i_qr and i >= i_qr_new)) and i != i_k:
                    if pposition.squares[j][i] != 0:
                        queensidepossible = False
                if ((i > i_k and i <= i_k_new) or (i < i_k and i >= i_k_new)) and i != i_qr:
                    if pposition.squares[j][i] != 0:
                        queensidepossible = False

        if queensidepossible:
            mv = chessmove(i_k, j, i_k_new, j)
            mv.MovingPiece = pposition.squares[j][i_k]
            mv.IsCastling = True
            mv.othercoordinates = (i_qr, j, i_qr_new, j)
            MoveList.append(mv)

        if kingsidepossible:
            i_k_new = self.boardwidth - 2
            i_kr_new = i_k_new - 1
            for i in range(self.boardwidth):
                if ((i > i_kr and i <= i_kr_new) or (i < i_kr and i >= i_kr_new)) and i != i_k:
                    if pposition.squares[j][i] != 0:
                        kingsidepossible = False
                if ((i > i_k and i <= i_k_new) or (i < i_k and i >= i_k_new)) and i != i_kr:
                    if pposition.squares[j][i] != 0:
                        kingsidepossible = False

        if kingsidepossible:
            mv = chessmove(i_k, j, i_k_new, j)
            mv.MovingPiece = pposition.squares[j][i_k]
            mv.IsCastling = True
            mv.othercoordinates = (i_kr, j, i_kr_new, j)
            MoveList.append(mv)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetPromotion(self, mv):
        includepromote = False
        includenonpromote = False

        MoveList = []

        pt1 = self.piecetypes[abs(mv.MovingPiece) - 1]

        if pt1.name in ["Pawn"]:
            if mv.MovingPiece > 0 and mv.coordinates[3] == self.boardheight - 1:
                includepromote = True
                includenonpromote = False
            elif mv.MovingPiece < 0 and mv.coordinates[3] == 0:
                includepromote = True
                includenonpromote = False
            else:
                includepromote = False
                includenonpromote = True
        else:
            includepromote = False
            includenonpromote = True

        if includenonpromote == True:
            mv2 = copy.deepcopy(mv)
            MoveList.append(mv2)            

        if includepromote == True:
            for pi in range(len(self.piecetypes)):
                if (self.piecetypes[pi].name not in ["Amazon", "King", pt1.name]) and self.piecetypes[pi].IsRoyal == False:
                    mv2 = copy.deepcopy(mv)
                    if mv.MovingPiece < 0:
                        mv2.PromoteToPiece = (pi + 1) * -1
                    else:
                        mv2.PromoteToPiece = pi + 1
                    MoveList.append(mv2)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def PrintIsAttacked(self, pposition):
        for j in range(self.boardheight -1,-1,-1):
            s = ""
            for i in range(self.boardheight):
                if pposition.IsAttacked[j][i] == True:
                    s += 'X'
                else:
                    s += '.'
            print(s)
#---------------------------------------------------------------------------------------------------------
    def ExecuteMove(self, pposition, pmove):
        myresultpos = copy.deepcopy(pposition)

        i1 = pmove.coordinates[0]
        j1 = pmove.coordinates[1]
        i2 = pmove.coordinates[2]
        j2 = pmove.coordinates[3]

        if pmove.PromoteToPiece != 0:
            myresultpos.squares[j2][i2] = pmove.PromoteToPiece
        else:
            myresultpos.squares[j2][i2] = pmove.MovingPiece
        myresultpos.squares[j1][i1] = 0

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
    def StaticEvaluation(self, pposition):
        piecevalues = [13.0, 3.1, 4.0, 3.8, 4.0, 3.0, 3.4, 1.0, 9.1, 5.0]
        materialbalance = 0.0
        myresult = 0.0
        #Locate white and black King:
        i_kw = -1
        j_kw = -1
        i_kb = -1
        j_kb = -1

        for j in range(self.boardheight -1,-1,-1):
            for i in range(self.boardheight):
                if pposition.squares[j][i] != 0:
                    pi = abs(pposition.squares[j][i]) - 1
                    pt = self.piecetypes[pi]

                    if pposition.squares[j][i] > 0:
                        if pt.name == "King" and pt.IsRoyal == True:
                            i_kw = i
                            j_kw = j
                        else:
                            materialbalance += piecevalues[pi]
                    else:
                        if pt.name == "King" and pt.IsRoyal == True:
                            i_kb = i
                            j_kb = j
                        else:
                            materialbalance -= piecevalues[pi]

        if i_kw == -1 and i_kb == -1:
            myresult = -100.0 * pposition.colourtomove
            return myresult
        if i_kw == -1:
            myresult = -100.0
            return myresult
        if i_kb == -1:
            myresult = 100.0
            return myresult
        if materialbalance > 8:
            myresult = 80.0
            return myresult
        if materialbalance < -8:
            myresult = -80.0
            return myresult
        return materialbalance * 10
#---------------------------------------------------------------------------------------------------------
    def Calculation_n_plies(self, pposition, n_plies):
        if n_plies > 3:
            print(f"Start calculation n_plies = {n_plies}")

        myresult = self.StaticEvaluation(pposition)

        if n_plies == 0:
            return myresult
        if myresult in (-100, 100):
            return myresult

        a = self.Position2MoveList(pposition)
        subresults = []
        for i in range(len(a)):
            newpos = self.ExecuteMove(pposition, a[i])
            newvalue = self.Calculation_n_plies(newpos, n_plies - 1)
            subresults.append((i, newvalue))

        if pposition.colourtomove == 1:
            res_sorted = sorted(subresults, key=lambda tup: tup[1], reverse=True)
        else:
            res_sorted = sorted(subresults, key=lambda tup: tup[1], reverse=False)
        myresult = res_sorted[0][1]

        return myresult
#---------------------------------------------------------------------------------------------------------
