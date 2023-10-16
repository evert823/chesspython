import json
from chesspiecetype import chesspiecetype
from chessposition import chessposition
from chessmove import chessmove

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
        for i in range(self.boardwidth):
            for j in range(self.boardheight):
                if ((pposition.squares[j][i] > 0 and pposition.colourtomove < 0) or
                    (pposition.squares[j][i] < 0 and pposition.colourtomove > 0)):
                    self.GetStepLeapAttacks(pposition, i, j)
                    self.GetSlideAttacks(pposition, i, j)

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
                        mv.MovingPieceSymbol = pt.symbol
                        MoveList.append(mv)

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
            mv.MovingPieceSymbol = pt.symbol
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
            mv.MovingPieceSymbol = pt.symbol
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
            mv.MovingPieceSymbol = pt.symbol
            mv.IsEnPassant = True
            mv.othercoordinates = (x_to, y_to, -1, -1)
            mv.IsCapture = True
            MoveList.append(mv)

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
                    mv.MovingPieceSymbol = pt.symbol
                    MoveList.append(mv)
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
                    if ((pposition.squares[j2][i2] > 0 and pposition.squares[j][i] < 0) or
                        (pposition.squares[j2][i2] < 0 and pposition.squares[j][i] > 0)):
                        mv = chessmove(i, j, i2, j2)
                        mv.MovingPieceSymbol = pt.symbol
                        mv.IsCapture = True
                        MoveList.append(mv)

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

                if ((pposition.squares[j2][i2] > 0 and pposition.squares[j][i] < 0) or
                    (pposition.squares[j2][i2] < 0 and pposition.squares[j][i] > 0)):
                    mv = chessmove(i, j, i2, j2)
                    mv.MovingPieceSymbol = pt.symbol
                    mv.IsCapture = True
                    MoveList.append(mv)
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
                if ((i >= i_k and i <= i_k_new) or (i <= i_k and i >= i_k_new)) and pposition.IsAttacked[j][i] == True:
                    queensidepossible = False

        if queensidepossible:
            mv = chessmove(i_k, j, i_k_new, j)
            mv.MovingPieceSymbol = mykingsymbol
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
                if ((i >= i_k and i <= i_k_new) or (i <= i_k and i >= i_k_new)) and pposition.IsAttacked[j][i] == True:
                    kingsidepossible = False

        if kingsidepossible:
            mv = chessmove(i_k, j, i_k_new, j)
            mv.MovingPieceSymbol = mykingsymbol
            mv.IsCastling = True
            mv.othercoordinates = (i_kr, j, i_kr_new, j)
            MoveList.append(mv)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetStepLeapAttacks(self, pposition, i, j):
        pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]
        if pt.IsDivergent == False:
            lookatvectors = pt.stepleapmovevectors
        else:
            lookatvectors = pt.stepleapcapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if pposition.colourtomove == 1:
                j2 = j - v[1]
            else:
                j2 = j + v[1]

            if i2 >= 0 and i2 < self.boardwidth:
                if j2 >= 0 and j2 < self.boardheight:
                    pposition.IsAttacked[j2][i2] = True
#---------------------------------------------------------------------------------------------------------
    def GetSlideAttacks(self, pposition, i, j):
        pt = self.piecetypes[abs(pposition.squares[j][i]) - 1]

        if pt.IsDivergent == False:
            lookatvectors = pt.slidemovevectors
        else:
            lookatvectors = pt.slidecapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if pposition.colourtomove == 1:
                j2 = j - v[1]
            else:
                j2 = j + v[1]

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False):
                
                pposition.IsAttacked[j2][i2] = True

                if pposition.squares[j2][i2] != 0:
                    blocked = True

                i2 = i2 + v[0]

                if pposition.colourtomove == 1:
                    j2 = j2 - v[1]
                else:
                    j2 = j2 + v[1]
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
