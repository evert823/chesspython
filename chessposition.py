import json
import chesshelp

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
