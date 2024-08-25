from chessgame import chessgame
from datetime import datetime

def TestCastle(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")
    

    queensidecastling_happened = False
    kingsidecastling_happened = False

    pchessgame.mainposition.ScanAttacked(pchessgame.piecetypes)
    pchessgame.mainposition.Position2MoveList(pchessgame.piecetypes)
    for movei in range(pchessgame.mainposition.movelist_totalfound):
        a = pchessgame.mainposition.movelist[movei].ShortNotation(pchessgame.piecetypes)
        if a == "0-0":
            kingsidecastling_happened = True
        if a == "0-0-0":
            queensidecastling_happened = True

    if queensidecastling_happened == False:
        raise Exception("Queenside castling expected but did not happen")
    if kingsidecastling_happened == False:
        raise Exception("Kingside castling expected but did not happen")

def TestNoCastle(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")
    
    castling_happened = False

    pchessgame.mainposition.ScanAttacked(pchessgame.piecetypes)
    pchessgame.mainposition.Position2MoveList(pchessgame.piecetypes)
    for movei in range(pchessgame.mainposition.movelist_totalfound):
        a = pchessgame.mainposition.movelist[movei].ShortNotation(pchessgame.piecetypes)
        if a == "0-0" or a == "0-0-0":
            castling_happened = True

    if castling_happened == True:
        raise Exception("Castling happened but not expected")

def TestPawn(pchessgame, pgamefilename, ppositionfilename, expectedcoord):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")
    
    pchessgame.mainposition.ScanAttacked(pchessgame.piecetypes)
    pchessgame.mainposition.Position2MoveList(pchessgame.piecetypes)

    mymovehappened = False
    for movei in range(pchessgame.mainposition.movelist_totalfound):
        pt = pchessgame.piecetypes[abs(pchessgame.mainposition.movelist[movei].MovingPiece) - 1]
        if pt.name == "Pawn":
            if pchessgame.mainposition.movelist[movei].coordinates == expectedcoord:
                mymovehappened = True

    if mymovehappened == False:
        raise Exception(f"Expected pawnmove {expectedcoord} did not happen")

def TestPawnPromote(pchessgame, pgamefilename, ppositionfilename, expectedcoord):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")
    
    pchessgame.mainposition.ScanAttacked(pchessgame.piecetypes)
    pchessgame.mainposition.Position2MoveList(pchessgame.piecetypes)

    mymovehappened = False
    for movei in range(pchessgame.mainposition.movelist_totalfound):
        pt = pchessgame.piecetypes[abs(pchessgame.mainposition.movelist[movei].MovingPiece) - 1]
        if pt.name == "Pawn":
            if pchessgame.mainposition.movelist[movei].coordinates == expectedcoord:
                if pchessgame.mainposition.movelist[movei].PromoteToPiece != 0:
                    ptp = pchessgame.piecetypes[abs(pchessgame.mainposition.movelist[movei].PromoteToPiece) - 1]
                    if ptp.name == "Hunter":
                        mymovehappened = True

    if mymovehappened == False:
        raise Exception(f"Expected pawnmove {expectedcoord} did not happen")


def TestMove(pchessgame, pgamefilename, ppositionfilename, expectedmovingpiecename, expectedcoord, IsExpected):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")
    
    pchessgame.mainposition.ScanAttacked(pchessgame.piecetypes)
    pchessgame.mainposition.Position2MoveList(pchessgame.piecetypes)

    mymovehappened = False
    for movei in range(pchessgame.mainposition.movelist_totalfound):
        pt = pchessgame.piecetypes[abs(pchessgame.mainposition.movelist[movei].MovingPiece) - 1]
        if pt.name == expectedmovingpiecename:
            if pchessgame.mainposition.movelist[movei].coordinates == expectedcoord:
                mymovehappened = True

    if mymovehappened == True and IsExpected == False:
        raise Exception(f"Move {expectedmovingpiecename} {expectedcoord} happened and not expected")
    if mymovehappened == False and IsExpected == True:
        raise Exception(f"Move {expectedmovingpiecename} {expectedcoord} expected and not happened")


def TestCheck(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")
    pchessgame.mainposition.ScanAttacked(pchessgame.piecetypes)
    if pchessgame.mainposition.PMKingIsInCheck() == True:
        pass
    else:
        raise Exception(f"Check expected but there was no check.")

def TestStalemate(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")
    myval, _, _ = pchessgame.Calculation_n_plies(1)

    if myval == 0.0:
        pass
    else:
        raise Exception(f"Stalemate expected but there was no stalemate.")

def TestMate(pchessgame, pgamefilename, ppositionfilename):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")
    myval, _, _ = pchessgame.Calculation_n_plies(1)

    if ((myval == 100.0 and pchessgame.mainposition.colourtomove == -1) or
        (myval == -100.0 and pchessgame.mainposition.colourtomove == 1)):
        pass
    else:
        raise Exception(f"Mate expected, but there was no mate.")

def TestMate_n(pchessgame, pgamefilename, ppositionfilename, mate_in_n=2, expectedcoordinates=(-1, -1, -1, -1)):
    if mate_in_n in (1, 2, 3, 4):
        pass
    else:
        n = 2
    n_plies = mate_in_n * 2

    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")

    startdatetime = datetime.now()
    myval, movei, _ = pchessgame.Calculation_n_plies(n_plies)
    enddatetime = datetime.now()

    d = enddatetime - startdatetime
    secondsneeded = d.total_seconds()

    if n_plies < 5 and secondsneeded > 15:
        raise Exception(f"Performance of calculation under acceptable levels")

    foundcoordinates = pchessgame.mainposition.movelist[movei].coordinates
    if expectedcoordinates != (-1, -1, -1, -1):
        if foundcoordinates != expectedcoordinates:
            raise Exception(f"Mate expected, but the identified move is not correct.")

    if ((myval == 100.0 and pchessgame.mainposition.colourtomove == 1) or
        (myval == -100.0 and pchessgame.mainposition.colourtomove == -1)):
        pass
    else:
        raise Exception(f"Mate expected, but there was no mate.")

def TestStalemate_n(pchessgame, pgamefilename, ppositionfilename, stalemate_in_n=2):
    if stalemate_in_n in (1, 2, 3, 4):
        pass
    else:
        n = 2
    n_plies = (stalemate_in_n * 2) + 1

    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")

    myval, _, _ = pchessgame.Calculation_n_plies(n_plies)

    if myval == 0.0:
        pass
    else:
        raise Exception(f"Stalemate expected, but there was no mate.")

def BaselinePerformance(pchessgame, pgamefilename, ppositionfilename, n_plies, baseline_seconds):

    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", ".\\unittests\\" + ppositionfilename + ".json")

    print(f"Executing performance test for {ppositionfilename} baseline {baseline_seconds}")

    startdatetime = datetime.now()
    myval, _, _ = pchessgame.Calculation_n_plies(n_plies)
    enddatetime = datetime.now()
    d = enddatetime - startdatetime
    secondsneeded = d.total_seconds()

    print(f"secondsneeded for {ppositionfilename}: {secondsneeded} baseline {baseline_seconds}")
    if secondsneeded > baseline_seconds:
        raise Exception(f"Performance of calculation under acceptable levels")


mylocalpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
mychessgame = chessgame(mylocalpath)

print(datetime.now())
TestCastle(mychessgame, "maingame", "01A_castle_white")
TestCastle(mychessgame, "maingame", "01B_castle_black")
TestNoCastle(mychessgame, "maingame", "01C_nocastle_white")
TestNoCastle(mychessgame, "maingame", "01D_nocastle_black")
TestNoCastle(mychessgame, "maingame", "01E_nocastle_white")
TestNoCastle(mychessgame, "maingame", "01F_nocastle_black")
TestNoCastle(mychessgame, "maingame", "01G_nocastle_white")
TestNoCastle(mychessgame, "maingame", "01H_nocastle_black")
TestPawn(mychessgame, "maingame", "02A_pawn_white", (3, 4, 3, 5))
TestPawn(mychessgame, "maingame", "02A_pawn_black", (4, 3, 4, 2))
TestPawn(mychessgame, "maingame", "02B_pawn_white", (2, 1, 2, 3))
TestPawn(mychessgame, "maingame", "02B_pawn_black", (1, 6, 1, 4))
TestPawn(mychessgame, "maingame", "02C_pawn_white", (5, 3, 4, 4))
TestPawn(mychessgame, "maingame", "02C_pawn_white", (5, 3, 6, 4))
TestPawn(mychessgame, "maingame", "02C_pawn_black", (2, 3, 3, 2))
TestPawn(mychessgame, "maingame", "02C_pawn_black", (2, 3, 1, 2))
TestPawn(mychessgame, "maingame", "02D_pawn_white", (1, 4, 2, 5))
TestPawn(mychessgame, "maingame", "02D_pawn_black", (2, 3, 1, 2))
TestPawnPromote(mychessgame, "maingame", "02E_pawn_white", (1, 6, 1, 7))
TestPawnPromote(mychessgame, "maingame", "02E_pawn_white", (1, 6, 0, 7))
TestPawnPromote(mychessgame, "maingame", "02E_pawn_black", (6, 1, 6, 0))
TestPawnPromote(mychessgame, "maingame", "02E_pawn_black", (6, 1, 7, 0))
TestMove(mychessgame, "maingame", "03A_divergent_white", "Hunter", (4, 5, 4, 6), True)
TestMove(mychessgame, "maingame", "03A_divergent_white", "Hunter", (4, 5, 2, 6), True)
TestMove(mychessgame, "maingame", "03A_divergent_black", "Hunter", (2, 3, 2, 2), True)
TestMove(mychessgame, "maingame", "03A_divergent_black", "Hunter", (2, 3, 4, 4), True)
TestMove(mychessgame, "maingame", "03A_divergent_white", "Hunter", (4, 5, 4, 4), False)
TestMove(mychessgame, "maingame", "03A_divergent_white", "Hunter", (4, 5, 2, 5), False)
TestMove(mychessgame, "maingame", "03A_divergent_black", "Hunter", (2, 3, 2, 4), False)
TestMove(mychessgame, "maingame", "03A_divergent_black", "Hunter", (2, 3, 4, 3), False)
TestCheck(mychessgame, "maingame", "04A_check_white")
TestCheck(mychessgame, "maingame", "04A_check_black")
TestStalemate(mychessgame, "maingame", "05A_stalemate_white")
TestStalemate(mychessgame, "maingame", "05A_stalemate_black")
TestMate(mychessgame, "maingame", "06A_mate_0_white")
TestMate(mychessgame, "maingame", "06A_mate_0_black")
TestMate_n(mychessgame, "maingame", "06B_mate_1_white", 1, (5, 1, 2, 4))
TestMate_n(mychessgame, "maingame", "06B_mate_1_black", 1, (5, 6, 2, 3))
TestMate_n(mychessgame, "maingame", "06C_mate_2_white_01", 2, (0, 1, 6, 7))
TestMate_n(mychessgame, "maingame", "06C_mate_2_white_02", 2, (7, 1, 1, 7))
TestMate_n(mychessgame, "maingame", "06C_mate_2_black_01", 2, (7, 6, 1, 0))
TestMate_n(mychessgame, "maingame", "06C_mate_2_black_02", 2, (0, 6, 6, 0))
TestMate_n(mychessgame, "maingame", "06D_huntermate_3_white", 3, (2, 4, 1, 4))
TestMate_n(mychessgame, "maingame", "06D_huntermate_3_black", 3, (2, 3, 1, 3))
TestStalemate_n(mychessgame, "maingame", "08A_stalemate_2_white", 2)
TestStalemate_n(mychessgame, "maingame", "08A_stalemate_2_black", 2)
BaselinePerformance(mychessgame, "maingame", "07A_mate_4_white_BN", 8, 6)
BaselinePerformance(mychessgame, "maingame", "07A_mate_4_black_BN", 8, 6)
print("ALL UNITTESTS PASSED")

print(datetime.now())
