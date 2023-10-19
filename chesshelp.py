class chesshelp:
    @staticmethod
    def Str2PieceType(psymbol, ppiecetypes):
        for i in range(len(ppiecetypes)):
            if psymbol == ppiecetypes[i].symbol:
                return i + 1
            if psymbol == "-" + ppiecetypes[i].symbol:
                return (i + 1) * -1
        return 0
#---------------------------------------------------------------------------------------------------------
    @staticmethod
    def PieceType2Str(ptypenr, ppiecetypes):
        if ptypenr > 0:
            i = ptypenr - 1
            return ppiecetypes[i].symbol
        if ptypenr < 0:
            i = (ptypenr * -1) - 1
            return "-" + ppiecetypes[i].symbol
        return "."
#---------------------------------------------------------------------------------------------------------
