import chess.engine

def GetNextMove(FEN):
    rowLetters = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    rowNumbers = {8:0, 7:1, 6:2, 5:3, 4:4, 3:5, 2:6, 1:7}

    board = chess.Board(FEN)
    engine = chess.engine.SimpleEngine.popen_uci("Stockfish\stockfish_engine.exe")
    limit = chess.engine.Limit(time=0.)
    responce = engine.play(board, limit)

    movestring = str(responce.move)
    
    engine.quit()

    startRow = rowLetters[movestring[0]]
    StartCol = rowNumbers[int(movestring[1])]

    endRow = rowLetters[movestring[2]]
    endCol = rowNumbers[int(movestring[3])]

    #print(f"api{startRow, StartCol, endRow, endCol}")
    return [startRow, StartCol, endRow, endCol]
