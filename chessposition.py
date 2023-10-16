import json

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
        self.IsAttacked = [] #To mark if a square is controlled by piece NOT from colourtomove - calculated
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
        self.IsAttacked.clear()
        for j in range(self.boardheight):
            myrank = []
            for i in range(self.boardwidth):
                myrank.append(False)
            self.IsAttacked.append(myrank)
#---------------------------------------------------------------------------------------------------------
    def InitIsAttacked(self):
        for i in range(self.boardwidth):
            for j in range(self.boardheight):
                self.IsAttacked[j][i] = False
#---------------------------------------------------------------------------------------------------------
    def LoadFromJsonFile(self, pfilename, pPieceTypeIndex):
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
                self.squares[j][i] = self.Str2PieceType(s, pPieceTypeIndex)
#---------------------------------------------------------------------------------------------------------
    def SaveAsJsonFile(self, pfilename, pPieceTypeIndex):
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
                mysymbol = self.PieceType2Str(self.squares[rj][i], pPieceTypeIndex)
                while len(mysymbol) < 2:
                    mysymbol = " " + mysymbol
                myvisualrank += mysymbol
                if i < self.boardwidth - 1:
                    myvisualrank += "|"
            positiondict["squares"].append(myvisualrank)

        json.dump(positiondict, positionfile, indent=4)
        positionfile.close()
#---------------------------------------------------------------------------------------------------------
    def Str2PieceType(self, psymbol, pPieceTypeIndex):
        for x in pPieceTypeIndex:
            if psymbol == x[1]:
                return x[0]
            if psymbol == "-" + x[1]:
                return x[0] * -1
        return 0
#---------------------------------------------------------------------------------------------------------
    def PieceType2Str(self, ptypenr, pPieceTypeIndex):
        for x in pPieceTypeIndex:
            if ptypenr == x[0]:
                return x[1]
            if ptypenr == x[0] * -1:
                return "-" + x[1]
        return "."
