import json
import chesshelp
from chessmove import chessmove
import copy

class chessposition:
    def __init__(self):
        self.boardwidth = -1
        self.boardheight = -1
        self.colourtomove = 1 # 1 for white; -1 for black
        #only purpose of storing preceding move here, is to determine legality of en passant
        self.precedingmove = (-1, -1, -1, -1)
        self.whitekinghasmoved = True
        self.whitekingsiderookhasmoved = True
        self.whitequeensiderookhasmoved = True
        self.blackkinghasmoved = True
        self.blackkingsiderookhasmoved = True
        self.blackqueensiderookhasmoved = True
        self.squares = []
        self.SquaresAttackedByPM = [] #list of squares as tuples (i,j) that the player to move is attacking
        self.SquaresAttackedByPO = [] #list of squares as tuples (i,j) that the opponent is attacking
        self.whitekingcoord = (-1, -1)
        self.blackkingcoord = (-1, -1)
#---------------------------------------------------------------------------------------------------------
    def ClearNonPersistent(self):
        self.SquaresAttackedByPM.clear()
        self.SquaresAttackedByPO.clear()
        self.whitekingcoord = (-1, -1)
        self.blackkingcoord = (-1, -1)
#---------------------------------------------------------------------------------------------------------
    def ResetBoardsize(self, pboardwidth, pboardheight):
        self.boardwidth = pboardwidth
        self.boardheight = pboardheight
        self.squares.clear()
        for j in range(self.boardheight):
            myrank = []
            for i in range(self.boardwidth):
                myrank.append(0)
            self.squares.append(myrank)
        self.ClearNonPersistent()
#---------------------------------------------------------------------------------------------------------
    def LoadFromJsonFile(self, pfilename, ppiecetypes):
        #Load from json file and convert to class structure
        positionfile = open(pfilename, 'r')
        positiondict = json.load(positionfile)
        positionfile.close()
        self.boardwidth = positiondict["boardwidth"]
        self.boardheight = positiondict["boardheight"]
        self.colourtomove = positiondict["colourtomove"]
        self.ResetBoardsize(self.boardwidth, self.boardheight)

        if "precedingmove" in positiondict:
            self.precedingmove = (positiondict["precedingmove"]["x_from"], positiondict["precedingmove"]["y_from"], 
                                  positiondict["precedingmove"]["x_to"], positiondict["precedingmove"]["y_to"])
        else:
            self.precedingmove = (-1, -1, -1, -1)

        if "castlinginfo" in positiondict:
            self.whitekinghasmoved = positiondict["castlinginfo"]["whitekinghasmoved"]
            self.whitekingsiderookhasmoved = positiondict["castlinginfo"]["whitekingsiderookhasmoved"]
            self.whitequeensiderookhasmoved = positiondict["castlinginfo"]["whitequeensiderookhasmoved"]
            self.blackkinghasmoved = positiondict["castlinginfo"]["blackkinghasmoved"]
            self.blackkingsiderookhasmoved = positiondict["castlinginfo"]["blackkingsiderookhasmoved"]
            self.blackqueensiderookhasmoved = positiondict["castlinginfo"]["blackqueensiderookhasmoved"]
        else:
            self.whitekinghasmoved = True
            self.whitekingsiderookhasmoved = True
            self.whitequeensiderookhasmoved = True
            self.blackkinghasmoved = True
            self.blackkingsiderookhasmoved = True
            self.blackqueensiderookhasmoved = True

        for j in range(self.boardheight):
            rj = (self.boardheight - 1) - j
            mysymbol = positiondict["squares"][rj].split("|")
            for i in range(self.boardwidth):
                s = mysymbol[i].lstrip()
                self.squares[j][i] = chesshelp.chesshelp.Str2PieceType(s, ppiecetypes)
#---------------------------------------------------------------------------------------------------------
    def SaveAsJsonFile(self, pfilename, ppiecetypes):
        #Convert class structure to json and save as json file
        positionfile = open(pfilename, 'w')
        positiondict = {}
        positiondict["boardwidth"] = self.boardwidth
        positiondict["boardheight"] = self.boardheight
        positiondict["colourtomove"] = self.colourtomove

        if self.precedingmove == (-1, -1, -1, -1):
            pass
        else:
            positiondict["precedingmove"] = {"x_from": self.precedingmove[0], "y_from": self.precedingmove[1],
                                             "x_to": self.precedingmove[2], "y_to": self.precedingmove[3]}

        if (self.whitekinghasmoved == False or self.whitekingsiderookhasmoved == False or self.whitequeensiderookhasmoved == False or
            self.blackkinghasmoved == False or self.blackkingsiderookhasmoved == False or self.blackqueensiderookhasmoved == False):
            positiondict["castlinginfo"] = {"whitekinghasmoved": self.whitekinghasmoved, 
                                            "whitekingsiderookhasmoved": self.whitekingsiderookhasmoved,
                                            "whitequeensiderookhasmoved": self.whitequeensiderookhasmoved,
                                            "blackkinghasmoved": self.blackkinghasmoved,
                                            "blackkingsiderookhasmoved": self.blackkingsiderookhasmoved,
                                            "blackqueensiderookhasmoved": self.blackqueensiderookhasmoved}

        positiondict["squares"] = []
        for j in range(self.boardheight):
            rj = (self.boardheight - 1) - j
            myvisualrank = ""
            for i in range(self.boardwidth):
                mysymbol = chesshelp.chesshelp.PieceType2Str(self.squares[rj][i], ppiecetypes)
                while len(mysymbol) < 2:
                    mysymbol = " " + mysymbol
                myvisualrank += mysymbol
                if i < self.boardwidth - 1:
                    myvisualrank += "|"
            positiondict["squares"].append(myvisualrank)

        json.dump(positiondict, positionfile, indent=4)
        positionfile.close()
#---------------------------------------------------------------------------------------------------------
    def PositionFromFEN(self, pfen, ppiecetypes):
        fenparts0 = pfen.split(" ")
        fenparts = fenparts0[0].split("/")
        
        self.boardwidth = 8
        self.boardheight = 8

        if fenparts0[1].lower() == "w":
            self.colourtomove = 1
        else:
            self.colourtomove = -1

        self.ResetBoardsize(self.boardwidth, self.boardheight)
        self.precedingmove = (-1, -1, -1, -1)
        self.whitekinghasmoved = True
        self.whitekingsiderookhasmoved = True
        self.whitequeensiderookhasmoved = True
        self.blackkinghasmoved = True
        self.blackkingsiderookhasmoved = True
        self.blackqueensiderookhasmoved = True

        for j in range(len(fenparts)):
            rj = (self.boardheight - 1) - j
            fp = fenparts[j]
            csqi = 0
            for ci in range(len(fp)):
                if fp[ci].isnumeric() == True:
                    csqi += int(fp[ci])
                else:
                    self.squares[rj][csqi] = chesshelp.chesshelp.Str2PieceType4FEN(fp[ci], ppiecetypes)
                    csqi += 1
#---------------------------------------------------------------------------------------------------------
    def PositionAsFEN(self, ppiecetypes):
        fenparts = []
        for j in range(self.boardheight):
            rj = (self.boardheight - 1) - j
            vacantcount = 0
            fenpart = ""
            for i in range(self.boardwidth):
                if self.squares[rj][i] != 0:
                    if vacantcount != 0:
                        fenpart += str(vacantcount)
                        vacantcount = 0
                    mysymbol = chesshelp.chesshelp.PieceType2Str4FEN(self.squares[rj][i], ppiecetypes)
                    fenpart += mysymbol
                if self.squares[rj][i] == 0:
                    vacantcount += 1
            if vacantcount != 0:
                fenpart += str(vacantcount)
            fenparts.append(fenpart)
        fen = "/".join(fenparts)
        if self.colourtomove == 1:
            fen += " w"
        else:
            fen += " b"
        return fen
#---------------------------------------------------------------------------------------------------------
    def WhiteKingIsInCheck(self):
        if self.colourtomove == 1:
            if self.whitekingcoord in self.SquaresAttackedByPO:
                return True
        else:
            if self.whitekingcoord in self.SquaresAttackedByPM:
                return True
        return False
#---------------------------------------------------------------------------------------------------------
    def BlackKingIsInCheck(self):
        if self.colourtomove == 1:
            if self.blackkingcoord in self.SquaresAttackedByPM:
                return True
        else:
            if self.blackkingcoord in self.SquaresAttackedByPO:
                return True
        return False
#---------------------------------------------------------------------------------------------------------
    def PMKingIsInCheck(self):
        if self.colourtomove == 1:
            if self.whitekingcoord in self.SquaresAttackedByPO:
                return True
        else:
            if self.blackkingcoord in self.SquaresAttackedByPO:
                return True
        return False
#---------------------------------------------------------------------------------------------------------
    def POKingIsInCheck(self):
        if self.colourtomove == 1:
            if self.blackkingcoord in self.SquaresAttackedByPM:
                return True
        else:
            if self.whitekingcoord in self.SquaresAttackedByPM:
                return True
        return False
#---------------------------------------------------------------------------------------------------------
    def ScanAttacked(self, ppiecetypes):
        SquaresAttackedByPMdup = []
        SquaresAttackedByPOdup = []
        for i in range(self.boardwidth):
            for j in range(self.boardheight):

                if self.squares[j][i] != 0:
                    pt = ppiecetypes[abs(self.squares[j][i]) - 1]
                    if pt.name == "King" and pt.IsRoyal == True:
                        if self.squares[j][i] > 0:
                            self.whitekingcoord = (i, j)
                        else:
                            self.blackkingcoord = (i, j)

                if ((self.squares[j][i] > 0 and self.colourtomove > 0) or
                    (self.squares[j][i] < 0 and self.colourtomove < 0)):
                    SquaresAttackedByPMdup.extend(self.GetStepLeapAttacks(i, j, ppiecetypes))
                    SquaresAttackedByPMdup.extend(self.GetSlideAttacks(i, j, ppiecetypes))
                if ((self.squares[j][i] > 0 and self.colourtomove < 0) or
                    (self.squares[j][i] < 0 and self.colourtomove > 0)):
                    SquaresAttackedByPOdup.extend(self.GetStepLeapAttacks(i, j, ppiecetypes))
                    SquaresAttackedByPOdup.extend(self.GetSlideAttacks(i, j, ppiecetypes))
        self.SquaresAttackedByPM = []
        for x in SquaresAttackedByPMdup:
            if x not in self.SquaresAttackedByPM:
                self.SquaresAttackedByPM.append(x)
        self.SquaresAttackedByPO = []
        for x in SquaresAttackedByPOdup:
            if x not in self.SquaresAttackedByPO:
                self.SquaresAttackedByPO.append(x)
#---------------------------------------------------------------------------------------------------------
    def GetStepLeapAttacks(self, i, j, ppiecetypes):
        SquaresAttacked = []
        pt = ppiecetypes[abs(self.squares[j][i]) - 1]
        if pt.IsDivergent == False:
            lookatvectors = pt.stepleapmovevectors
        else:
            lookatvectors = pt.stepleapcapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if self.squares[j][i] > 0:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            if i2 >= 0 and i2 < self.boardwidth:
                if j2 >= 0 and j2 < self.boardheight:
                    SquaresAttacked.append((i2, j2))
        return SquaresAttacked
#---------------------------------------------------------------------------------------------------------
    def GetSlideAttacks(self, i, j, ppiecetypes):
        SquaresAttacked = []
        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        if pt.IsDivergent == False:
            lookatvectors = pt.slidemovevectors
        else:
            lookatvectors = pt.slidecapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if self.squares[j][i] > 0:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False):
                
                SquaresAttacked.append((i2, j2))

                if self.squares[j2][i2] != 0:
                    blocked = True

                i2 = i2 + v[0]

                if self.squares[j][i] > 0:
                    j2 = j2 + v[1]
                else:
                    j2 = j2 - v[1]
        return SquaresAttacked
#---------------------------------------------------------------------------------------------------------
    def Position2MoveList(self, ppiecetypes):
        MoveList = []
        for i in range(self.boardwidth):
            for j in range(self.boardheight):
                if ((self.squares[j][i] > 0 and self.colourtomove > 0) or
                    (self.squares[j][i] < 0 and self.colourtomove < 0)):
                    MoveList.extend(self.GetStepLeapMoves(i, j, ppiecetypes))
                    MoveList.extend(self.GetSlideMoves(i, j, ppiecetypes))
                    MoveList.extend(self.GetStepLeapCaptures(i, j, ppiecetypes))
                    MoveList.extend(self.GetSlideCaptures(i, j, ppiecetypes))
                    MoveList.extend(self.GetPawn2StepMoves(ppiecetypes, i, j))
                    MoveList.extend(self.GetPawnEnPassantMoves(ppiecetypes, i, j))
        MoveList.extend(self.GetCastling(ppiecetypes))

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetStepLeapMoves(self, i, j, ppiecetypes):
        MoveList = []
        #print(f"GetStepLeaveMoves({i},{j})")

        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        for v in pt.stepleapmovevectors:
            i2 = i + v[0]

            if self.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            if i2 >= 0 and i2 < self.boardwidth:
                if j2 >= 0 and j2 < self.boardheight:
                    if self.squares[j2][i2] == 0:
                        mv = chessmove(i, j, i2, j2)
                        mv.MovingPiece = self.squares[j][i]
                        MoveList.extend(self.GetPromotion(mv, ppiecetypes))

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetSlideMoves(self, i, j, ppiecetypes):
        MoveList = []
        #print(f"GetSlideMoves({i},{j})")

        pt = ppiecetypes[abs(self.squares[j][i]) - 1]
        
        for v in pt.slidemovevectors:
            i2 = i + v[0]

            if self.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False):
                if self.squares[j2][i2] == 0:
                    mv = chessmove(i, j, i2, j2)
                    mv.MovingPiece = self.squares[j][i]
                    MoveList.extend(self.GetPromotion(mv, ppiecetypes))
                else:
                    blocked = True

                i2 = i2 + v[0]

                if self.colourtomove == 1:
                    j2 = j2 + v[1]
                else:
                    j2 = j2 - v[1]

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetStepLeapCaptures(self, i, j, ppiecetypes):
        MoveList = []
        #print(f"GetStepLeaveCaptures({i},{j})")

        pt = ppiecetypes[abs(self.squares[j][i]) - 1]
        if pt.IsDivergent == False:
            lookatvectors = pt.stepleapmovevectors
        else:
            lookatvectors = pt.stepleapcapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if self.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            if i2 >= 0 and i2 < self.boardwidth:
                if j2 >= 0 and j2 < self.boardheight:
                    if ((self.squares[j2][i2] > 0 and self.squares[j][i] < 0) or
                        (self.squares[j2][i2] < 0 and self.squares[j][i] > 0)):
                        mv = chessmove(i, j, i2, j2)
                        mv.MovingPiece = self.squares[j][i]
                        mv.IsCapture = True
                        MoveList.extend(self.GetPromotion(mv, ppiecetypes))

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetSlideCaptures(self, i, j, ppiecetypes):
        MoveList = []
        #print(f"GetSlideCaptures({i},{j})")

        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        if pt.IsDivergent == False:
            lookatvectors = pt.slidemovevectors
        else:
            lookatvectors = pt.slidecapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if self.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False):

                if ((self.squares[j2][i2] > 0 and self.squares[j][i] < 0) or
                    (self.squares[j2][i2] < 0 and self.squares[j][i] > 0)):
                    mv = chessmove(i, j, i2, j2)
                    mv.MovingPiece = self.squares[j][i]
                    mv.IsCapture = True
                    MoveList.extend(self.GetPromotion(mv, ppiecetypes))
                    blocked = True
                elif self.squares[j2][i2] != 0:
                    blocked = True

                i2 = i2 + v[0]

                if self.colourtomove == 1:
                    j2 = j2 + v[1]
                else:
                    j2 = j2 - v[1]

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetPromotion(self, mv, ppiecetypes):
        includepromote = False
        includenonpromote = False

        MoveList = []

        pt1 = ppiecetypes[abs(mv.MovingPiece) - 1]

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
            for pi in range(len(ppiecetypes)):
                if (ppiecetypes[pi].name not in ["Amazon", "King", pt1.name]) and ppiecetypes[pi].IsRoyal == False:
                    mv2 = copy.deepcopy(mv)
                    if mv.MovingPiece < 0:
                        mv2.PromoteToPiece = (pi + 1) * -1
                    else:
                        mv2.PromoteToPiece = pi + 1
                    MoveList.append(mv2)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetPawn2StepMoves(self, ppiecetypes, i, j):
        MoveList = []

        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        if pt.name != "Pawn":
            return MoveList
        if self.colourtomove > 0 and j != 1:
            return MoveList
        if self.colourtomove < 0 and j != self.boardheight - 2:
            return MoveList

        i2 = i
        i_skip = i
        if self.colourtomove > 0:
            j_skip = j + 1
            j2 = j + 2
        else:
            j_skip = j - 1
            j2 = j - 2
        if self.squares[j_skip][i_skip] == 0 and self.squares[j2][i2] == 0:
            mv = chessmove(i, j, i2, j2)
            mv.MovingPiece = self.squares[j][i]
            MoveList.append(mv)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def GetPawnEnPassantMoves(self, ppiecetypes, i, j):
        MoveList = []

        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        if pt.name != "Pawn":
            return MoveList
        if self.precedingmove[3] != j:
            return MoveList

        x_from = self.precedingmove[0]
        y_from = self.precedingmove[1]
        x_to = self.precedingmove[2]
        y_to = self.precedingmove[3]
        ptm = ppiecetypes[abs(self.squares[y_to][x_to]) - 1]
        if ptm.name != "Pawn":
            return MoveList
        if x_from - i == 1 or x_from - i == -1:
            pass
        else:
            return MoveList
        
        if self.colourtomove > 0:
            if self.squares[y_to][x_to] > 0:
                return MoveList
            if j != self.boardheight - 4:
                return MoveList
            if y_from != y_to + 2:
                return MoveList
            mv = chessmove(i, j, x_from, y_to + 1)
            mv.MovingPiece = self.squares[j][i]
            mv.IsEnPassant = True
            mv.othercoordinates = (x_to, y_to, -1, -1)
            mv.IsCapture = True
            MoveList.append(mv)

        if self.colourtomove < 0:
            if self.squares[y_to][x_to] < 0:
                return MoveList
            if j != 3:
                return MoveList
            if y_from != y_to - 2:
                return MoveList
            mv = chessmove(i, j, x_from, y_to - 1)
            mv.MovingPiece = self.squares[j][i]
            mv.IsEnPassant = True
            mv.othercoordinates = (x_to, y_to, -1, -1)
            mv.IsCapture = True
            MoveList.append(mv)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def LocateKingRooks4Castling(self, ppiecetypes):
        i_k = -1
        i_qr = -1
        i_kr = -1

        if self.colourtomove == 1:
            if self.whitekinghasmoved == True:
                return i_k, i_qr, i_kr
            j = 0
        if self.colourtomove == -1:
            if self.blackkinghasmoved == True:
                return i_k, i_qr, i_kr
            j = self.boardheight - 1

        for i in range(self.boardwidth):
            pt = ppiecetypes[abs(self.squares[j][i]) - 1]
            if (pt.name == "Rook" and self.squares[j][i] * self.colourtomove > 0):
                if i_k == -1:
                    i_qr = i
                else:
                    i_kr = i
            elif (pt.name == "King" and pt.IsRoyal == True and self.squares[j][i] * self.colourtomove > 0):
                i_k = i

        return i_k, i_qr, i_kr
#---------------------------------------------------------------------------------------------------------
    def GetCastling(self, ppiecetypes):
        MoveList = []
        if self.colourtomove == 1:
            if self.whitekinghasmoved == True:
                return MoveList
            j = 0
        if self.colourtomove == -1:
            if self.blackkinghasmoved == True:
                return MoveList
            j = self.boardheight - 1


        #Now locate King and Rooks
        i_k, i_qr, i_kr = self.LocateKingRooks4Castling(ppiecetypes)

        queensidepossible = True
        kingsidepossible = True

        if self.colourtomove == 1 and self.whitequeensiderookhasmoved == True:
            queensidepossible = False
        if self.colourtomove == -1 and self.blackqueensiderookhasmoved == True:
            queensidepossible = False
        if self.colourtomove == 1 and self.whitekingsiderookhasmoved == True:
            kingsidepossible = False
        if self.colourtomove == -1 and self.blackkingsiderookhasmoved == True:
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
                    if self.squares[j][i] != 0:
                        queensidepossible = False
                if ((i > i_k and i <= i_k_new) or (i < i_k and i >= i_k_new)) and i != i_qr:
                    if self.squares[j][i] != 0:
                        queensidepossible = False
                if ((i >= i_k and i <= i_k_new) or (i <= i_k and i >= i_k_new)) and (i,j) in self.SquaresAttackedByPO:
                    queensidepossible = False

        if queensidepossible:
            mv = chessmove(i_k, j, i_k_new, j)
            mv.MovingPiece = self.squares[j][i_k]
            mv.IsCastling = True
            mv.othercoordinates = (i_qr, j, i_qr_new, j)
            MoveList.append(mv)

        if kingsidepossible:
            i_k_new = self.boardwidth - 2
            i_kr_new = i_k_new - 1
            for i in range(self.boardwidth):
                if ((i > i_kr and i <= i_kr_new) or (i < i_kr and i >= i_kr_new)) and i != i_k:
                    if self.squares[j][i] != 0:
                        kingsidepossible = False
                if ((i > i_k and i <= i_k_new) or (i < i_k and i >= i_k_new)) and i != i_kr:
                    if self.squares[j][i] != 0:
                        kingsidepossible = False
                if ((i >= i_k and i <= i_k_new) or (i <= i_k and i >= i_k_new)) and (i,j) in self.SquaresAttackedByPO:
                    kingsidepossible = False

        if kingsidepossible:
            mv = chessmove(i_k, j, i_k_new, j)
            mv.MovingPiece = self.squares[j][i_k]
            mv.IsCastling = True
            mv.othercoordinates = (i_kr, j, i_kr_new, j)
            MoveList.append(mv)

        return MoveList
#---------------------------------------------------------------------------------------------------------
    def StaticEvaluation(self, ppiecetypes):
        materialbalance = 0.0
        myresult = 0.0
        #Locate white and black King:
        i_kw = -1
        j_kw = -1
        i_kb = -1
        j_kb = -1

        for j in range(self.boardheight -1,-1,-1):
            for i in range(self.boardheight):
                if self.squares[j][i] != 0:
                    pi = abs(self.squares[j][i]) - 1
                    pt = ppiecetypes[pi]

                    if self.squares[j][i] > 0:
                        if pt.name == "King" and pt.IsRoyal == True:
                            i_kw = i
                            j_kw = j
                        else:
                            materialbalance += chesshelp.chesshelp.PieceType2Value(pi, ppiecetypes)
                    else:
                        if pt.name == "King" and pt.IsRoyal == True:
                            i_kb = i
                            j_kb = j
                        else:
                            materialbalance -= chesshelp.chesshelp.PieceType2Value(pi, ppiecetypes)

        if i_kw == -1 and i_kb == -1:
            myresult = -100.0 * self.colourtomove
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
