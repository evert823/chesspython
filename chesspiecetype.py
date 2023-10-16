import json

class chesspiecetype:
    def __init__(self):
        self.symbol = ''
        self.name = ''
        self.IsRoyal = False
        self.IsDivergent = False
        #Rule: if IsDivergent is false then capturevectors will be ignored, only movevectors will be looked at
        self.stepleapmovevectors = []
        self.slidemovevectors = []
        self.stepleapcapturevectors = []
        self.slidecapturevectors = []
#---------------------------------------------------------------------------------------------------------
    def VectorSetFromjson(self, mydict):
        myresult = []
        for v in mydict:
            myresult.append((v["x"], v["y"]))
        return myresult
#---------------------------------------------------------------------------------------------------------
    def VectorSetTojson(self, myset):
        myresult = []
        for v in myset:
            vectordict = {}
            vectordict["x"] = v[0]
            vectordict["y"] = v[1]
            myresult.append(vectordict)
        return myresult
#---------------------------------------------------------------------------------------------------------
    def LoadFromJsonFile(self, pfilename):
        #Load from json file and convert to class structure
        piecefile = open(pfilename, 'r')
        piecedict = json.load(piecefile)
        piecefile.close()
        self.symbol = piecedict["symbol"]
        self.name = piecedict["name"]
        self.IsRoyal = piecedict["IsRoyal"]
        self.IsDivergent = piecedict["IsDivergent"]

        self.stepleapmovevectors = self.VectorSetFromjson(piecedict["stepleapmovevectors"]).copy()
        self.slidemovevectors = self.VectorSetFromjson(piecedict["slidemovevectors"]).copy()
        if self.IsDivergent == True:
            self.stepleapcapturevectors = self.VectorSetFromjson(piecedict["stepleapcapturevectors"]).copy()
            self.slidecapturevectors = self.VectorSetFromjson(piecedict["slidecapturevectors"]).copy()
#---------------------------------------------------------------------------------------------------------
    def SaveAsJsonFile(self, pfilename):
        #Convert class structure to json and save as json file
        piecefile = open(pfilename, 'w')
        piecedict = {}
        piecedict["symbol"] = self.symbol
        piecedict["name"] = self.name
        piecedict["IsRoyal"] = self.IsRoyal
        piecedict["IsDivergent"] = self.IsDivergent

        piecedict["stepleapmovevectors"] = self.VectorSetTojson(self.stepleapmovevectors).copy()
        piecedict["slidemovevectors"] = self.VectorSetTojson(self.slidemovevectors).copy()
        if self.IsDivergent == True:
            piecedict["stepleapcapturevectors"] = self.VectorSetTojson(self.stepleapcapturevectors).copy()
            piecedict["slidecapturevectors"] = self.VectorSetTojson(self.slidecapturevectors).copy()

        json.dump(piecedict, piecefile, indent=4)
        piecefile.close()
#---------------------------------------------------------------------------------------------------------
