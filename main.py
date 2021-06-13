import pygame
import matplotlib.pyplot as plt

from draw import *
from computer import *

BOARDWIDTH = 400
BOARDHEIGHT = 400

SCREENWIDTH = 420
SCREENHEIGHT = 400

BOXSIZE = BOARDWIDTH//8

############################## Colours ##############################

# green shades
# colour1 = (118,150,86)
# colour2 = (238,238,210)

# classic wood
colour1 = (182, 136, 96)
colour2 = (241, 218, 179)

highlightColour = (150, 100, 66) # the colour of the last move highlight

#####################################################################

lastMove = [0, 0, 0, 0] # startrow, startcol, endrow, endcol

startRow = 0
startCol = 0

clicked = False ## whether or not a piece has been clicked

totalMoveNumber = 0
fullMoveNumber = 0

drag = False
draggedPiece = None

class Piece:
    def __init__(self, piece, row, col):
        self.row = row
        self.col = col
        self.piece = piece
        self.numberOfMoves = 0

        if self.piece.isupper():
            self.colour = "w"
            self.oppositionColour = "b"
        else:
            self.colour = "b"
            self.oppositionColour = "w"

def getFEN(board):
    #return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    prevRow = 0
    NewFEN = ''
    for row in range(8):
        for col in range(8):
            if prevRow != row:
                NewFEN += "/"
            prevRow = row
            item = board[row][col].piece
            if item == "!":
                NewFEN += "1"
            else:
                NewFEN += item

    string=NewFEN #single string
    newstring="" #null
    count1 = 0 #count of 1s
    flag = False #boolean flag - checks if change in string

    for i in range (len(string)): #iterate through string
        if string[i] == "1": #check for 1s and increment count if so
            count1 = count1 + 1
            flag = True #set change flag to True

        elif count1 != 0 and string[i] != "1": #generate new string
            newstring = newstring + str(count1) + string[i]
            count1 = 0 # reset count

        elif count1 == 0 and string[i] != "1": #special case capture, no 1s at start
            newstring = newstring + string[i]

    if count1 != 0: #checks if final count is 0, i.e. reset
        newstring = newstring + str(count1)

    if flag == False:
        return (newstring+" w - - 0 1")

    else:
        return (newstring+" w - - 0 1")

def checkForPromotion():
    for row in range(8):
        for col in range(8):
            try: 
                piece = board[row][col]
                if piece.piece == "P" and piece.col == 0:
                    board[piece.col][piece.row].piece = "Q"
                if piece.piece == "p" and piece.col == 7:
                    board[piece.col][piece.row].piece = "q"
            except:
                pass

def getAllLegalMoves(board, colour): # colour "b" or "w"
    allLegalMoves = []
    for row in board:
        for item in row: # for each individual piece on the board
            
            if item.colour == colour: # if it is the desired colour
                for legalmove in isLegal(item): # add each legalmove to the full list of legal moves for that colour
                    allLegalMoves.append(legalmove)
    return allLegalMoves

def parseFEN(boardPositions):
    FEN = ''
    for letter in boardPositions:
        try:
            letter = int(letter)
            FEN += "!"*letter
        except:
            if letter != '/':
                FEN += letter

    if len(FEN) != 64:
        raise pygame.error('invalid FEN input')

    board = ([[[]for i in range(8)]for i in range(8)])
    currentCol = 0
    currentRow = 0
    for letter in FEN:

        board[currentCol][currentRow] = Piece(letter,currentRow, currentCol)
        currentRow += 1

        if currentRow == 8:
            currentRow = 0
            currentCol += 1
        if currentCol == 8:
            return board

def piece_symbol(row, col): #returns the piece in the given row and col
    try:
        piece = board[col][row].piece
        if piece == "!":
            return None
        else:
            return piece
    except:
        return None

def isLegal(InputPiece):  
    # + row --> right
    # - row --> left
    # + col --> down
    # - col --> up

    verticalDirection = 1 # if this is -1 the col/row numbers will be the negative verson of themself, instead of move up --> move down, left --> right

    legalMoves = []

    #print(board[][])

    if InputPiece.piece == "P":
        if InputPiece.numberOfMoves == 0:
            if board[InputPiece.row][InputPiece.col-2].piece == None: # forwards 2
                legalMoves.append((InputPiece.row, InputPiece.col-2))

        targetPiece_symbol = piece_symbol(InputPiece.row, InputPiece.col-1) # up 1
        if targetPiece_symbol == None:
            legalMoves.append((InputPiece.row, InputPiece.col-1))

        try:
            targetPiece_symbol = piece_symbol(InputPiece.row-1, InputPiece.col-1) # up and left
            if targetPiece_symbol != None:
                if targetPiece_symbol.islower():
                    legalMoves.append((InputPiece.row-1, InputPiece.col-1))
        except:
            pass

        try:
            targetPiece_symbol = piece_symbol(InputPiece.row+1, InputPiece.col-1) # up and right
            if targetPiece_symbol != None:
                if targetPiece_symbol.islower():
                    legalMoves.append((InputPiece.row+1, InputPiece.col-1))
        except:
            pass

    if InputPiece.piece == "p": # i could probably combine this and the last check
        if InputPiece.numberOfMoves == 0:
            if piece_symbol(InputPiece.row, InputPiece.col+2) == None: # down 2
                legalMoves.append((InputPiece.row, InputPiece.col+2))

        targetPiece_symbol = piece_symbol(InputPiece.row, InputPiece.col+1) ## down 1
        if targetPiece_symbol == None:
            legalMoves.append((InputPiece.row, InputPiece.col+1))

        try:
            targetPiece_symbol = piece_symbol(InputPiece.row-1, InputPiece.col+1) # down 1 and left
            if targetPiece_symbol != None:
                if targetPiece_symbol.isupper():
                    legalMoves.append((InputPiece.row-1, InputPiece.col+1))
        except:
            pass

        try:
            targetPiece_symbol = piece_symbol(InputPiece.row+1, InputPiece.col+1) # down 1 and right
            if targetPiece_symbol != None:
                if targetPiece_symbol.isupper():
                    legalMoves.append((InputPiece.row+1, InputPiece.col+1))
        except:
            pass

        ## en passant

    if InputPiece.piece.lower() == "n":
        for i in range(-1, 2, 2):
            verticalDirection = i
            possibleMoves = [(InputPiece.row+1, InputPiece.col-2*verticalDirection), (InputPiece.row-1, InputPiece.col-2*verticalDirection), (InputPiece.row+2, InputPiece.col-1*verticalDirection), (InputPiece.row-2, InputPiece.col-1*verticalDirection)]
            for j in possibleMoves:
                try:
                    targetPiece_symbol = piece_symbol(j[0], j[1])
                    if (targetPiece_symbol == None) or (InputPiece.piece.isupper() and targetPiece_symbol.islower()) or (InputPiece.piece.islower() and targetPiece_symbol.isupper()): # up/down 2 right 1
                        legalMoves.append((j))
                except:
                    pass
                 
    if InputPiece.piece.lower() == "b" or InputPiece.piece.lower() == "q":
        for j in range(-1, 2, 2):
            verticalDirection = j       
            for i in range(1, 8):
                try:
                    targetPiece_symbol = piece_symbol(InputPiece.row+i, InputPiece.col+i*verticalDirection)
                    if (targetPiece_symbol == None):
                        legalMoves.append((InputPiece.row+i, InputPiece.col+i*verticalDirection))
                    if (InputPiece.piece.isupper() and targetPiece_symbol.islower()) or (InputPiece.piece.islower() and targetPiece_symbol.isupper()):
                        legalMoves.append((InputPiece.row+i, InputPiece.col+i*verticalDirection))
                        break
                    if (InputPiece.piece.isupper() and targetPiece_symbol.isupper()) or (InputPiece.piece.islower() and targetPiece_symbol.islower()):
                        break
                except:
                    pass
            for i in range(1, 8):
                try:
                    targetPiece_symbol = piece_symbol(InputPiece.row-i, InputPiece.col+i*verticalDirection)
                    if (targetPiece_symbol == None):
                        legalMoves.append((InputPiece.row-i, InputPiece.col+i*verticalDirection))
                    if (InputPiece.piece.isupper() and targetPiece_symbol.islower()) or (InputPiece.piece.islower() and targetPiece_symbol.isupper()):
                        legalMoves.append((InputPiece.row-i, InputPiece.col+i*verticalDirection))
                        break
                    if (InputPiece.piece.isupper() and targetPiece_symbol.isupper()) or (InputPiece.piece.islower() and targetPiece_symbol.islower()):
                        break
                except:
                    pass
    
    if InputPiece.piece.lower() == "r" or InputPiece.piece.lower() == "q":
        for j in range(-1, 2, 2):
            verticalDirection = j
            for i in range(1, 8):
                try: # down/up
                    targetPiece_symbol = piece_symbol(InputPiece.row, InputPiece.col+i*verticalDirection)
                    if (targetPiece_symbol == None):
                        legalMoves.append((InputPiece.row, InputPiece.col+i*verticalDirection))

                    if (InputPiece.piece.isupper() and targetPiece_symbol.islower()) or (InputPiece.piece.islower() and targetPiece_symbol.isupper()): # if the target square is the opposition
                        legalMoves.append((InputPiece.row, InputPiece.col+i*verticalDirection))
                        break
                    elif (InputPiece.piece.isupper() and targetPiece_symbol.isupper()) or (InputPiece.piece.islower() and targetPiece_symbol.islower()):
                        break
                except:
                    pass
            for i in range(1, 8):
                try: # left/right
                    targetPiece_symbol = piece_symbol(InputPiece.row+i*verticalDirection, InputPiece.col)
                    if (targetPiece_symbol == None):
                        legalMoves.append((InputPiece.row+i*verticalDirection, InputPiece.col))

                    if (InputPiece.piece.isupper() and targetPiece_symbol.islower()) or (InputPiece.piece.islower() and targetPiece_symbol.isupper()): # if the target square is the opposition
                        legalMoves.append((InputPiece.row+i*verticalDirection, InputPiece.col))
                        break
                    elif (InputPiece.piece.isupper() and targetPiece_symbol.isupper()) or (InputPiece.piece.islower() and targetPiece_symbol.islower()):
                        break
                except:
                    pass

    if InputPiece.piece.lower() == "k":
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    if piece_symbol(InputPiece.row+i, InputPiece.col+j) == None: # forward 1 right 2
                            legalMoves.append((InputPiece.row+i, InputPiece.col+j))
                    if piece_symbol(InputPiece.row-i, InputPiece.col) == None: # forward 1 right 2
                            legalMoves.append((InputPiece.row-i, InputPiece.col))
                    if piece_symbol(InputPiece.row, InputPiece.col-i) == None: # forward 1 right 2
                            legalMoves.append((InputPiece.row, InputPiece.col-i))
                except:
                    pass

    legalMoves = list(legalMoves)
    removedOutsideGrid = []

    for move in legalMoves: # this is a temporary fix to remove possible moves that sit outside the 8x8 grid
        if not(move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0):
            removedOutsideGrid.append(move)

    return removedOutsideGrid

def movePiece(InputBoard, startrow, startcol, endrow, endcol):
    #print(f"{startrow, startcol} moved to {endrow, endcol}")
    if InputBoard[startcol][startrow].piece == "!":
        return InputBoard
    InputBoard[endcol][endrow] = InputBoard[startcol][startrow]
    InputBoard[endcol][endrow].row = endrow
    InputBoard[endcol][endrow].col = endcol
    InputBoard[endcol][endrow].numberOfMoves += 1
    InputBoard[startcol][startrow] = Piece("!", startrow, startcol) # empty node
    return InputBoard

def getKingPosition(board, colour):
    KingPosition = None
    for row in range(8):
        for col in range(8):
            targetPiece_symbol = board[row][col]
            if targetPiece_symbol.piece.lower() == "k" and targetPiece_symbol.colour == colour: # if target piece is a king AND if targetpeice is the correct colour 
                oppositionColour = targetPiece_symbol.oppositionColour 
                KingPosition = (col, row)
                
    if KingPosition == None:
        raise Exception ("No king is present")
    return KingPosition, oppositionColour

def isInCheck(board, colour):
    KingPosition, oppositionColour = getKingPosition(board, colour)

    if KingPosition in getAllLegalMoves(board, oppositionColour):
        return True ## in check
    else:
        return False # not in check

def isCheckmate(board, colour):
    (kingRow, kingCol) , oppositionColour = getKingPosition(board, colour)

    if isInCheck(board, colour) == False:
        return False

    legalKingMoves = isLegal(board[kingCol][kingRow])
    
    if legalKingMoves == []:
        return True 
    
    for move in legalKingMoves:
        row = move[0]
        col = move[1]
        
        testboard = board
        testboard = movePiece(testBoard, kingRow, kingCol, row, col)
        if not(isInCheck(testboard, "b")):
            testboard = movePiece(testBoard, row, col, kingRow, kingCol)
            return False
        
        testboard = movePiece(testBoard, row, col, kingRow, kingCol)
    return True


    return True

def makeMove(board, startrow, startcol, endrow, endcol):    
    global totalMoveNumber
    totalMoveNumber += 1
    print(totalMoveNumber,": ",currentFEN)
    
    board = movePiece(board, startrow, startcol, endrow, endcol)

    global lastMove
    lastMove = [startrow, startcol, endrow, endcol]
    
###################### getting starting board positions ######################

FENinput = "none"# input('enter FEN notation code or type none: ')

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((SCREENHEIGHT, SCREENWIDTH), pygame.RESIZABLE)

if FENinput == "none":
    FENinput = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" ## code for the normal chess starting position c
    
try:
    boardPositions, sideToMove, castlingAblility, enPassantTargetSquare, halfmoveClock, fullMoveCounter = FENinput.split(" ")
except:
    raise pygame.error('invalid FEN input')

board = parseFEN(boardPositions)

###############################################################################

################################## Main loop ##################################

consecutiveChecks = 0
currentFEN = FENinput
GameEnded = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()

        if event.type == pygame.VIDEORESIZE:
            w, h = (event.dict['size'])
            BOARDHEIGHT, BOARDWIDTH = min(w, h), min(w, h)

        keys = pygame.key.get_pressed()
        

        mousex, mousey = pygame.mouse.get_pos()
        clickedRow = mousex//BOXSIZE
        clickedCol = mousey//BOXSIZE

        if not GameEnded:
            if isCheckmate(board, "b") == True:
                # pygame.quit()
                # plt.plot(Xaxis, WYaxis)
                # plt.plot(Xaxis, BYaxis)
                # plt.show()
                GameEnded = True

            if (totalMoveNumber % 2 != 0): # if it is the computers turn (computer plays as white)
                currentFEN = getFEN(board)
                startRow, startCol, endRow, endCol = GetNextMove(currentFEN)
                makeMove(board, startRow, startCol, endRow, endCol)

            if event.type == pygame.MOUSEBUTTONDOWN: # begining of a drag
                if pygame.mouse.get_pressed() != (False, False, False):
                    if clickedRow > 7 or clickedCol > 7:
                        break
                    drag = True
                    startRow = clickedRow
                    startCol = clickedCol # clicked col is the end  col
                    draggedPieceSprite = sprites[board[startCol][startRow].piece]
                    draggedPiece = board[startCol][startRow]

            if event.type == pygame.MOUSEBUTTONUP: # end of a drag
                endRow,endCol = clickedRow, clickedCol
                drag = False
                if draggedPiece != None: # if draggedpiece has been dropped
                    if (endRow, endCol) in isLegal(draggedPiece): # if the final square is legal
                        if (totalMoveNumber % 2 == 0 and draggedPiece.piece.islower()): # if it is black's turn and the moved piece is black
 
                            testBoard = board
                            testBoard = movePiece(testBoard, startRow, startCol, endRow, endCol)

                            if isInCheck(testBoard, "b") == True or isInCheck(board, "b") == True: 
                                board = movePiece(board, endRow, endCol, startRow, startCol) # move piece back to origonal space

                            else:
                                currentFEN = getFEN(board)
                                makeMove(board, startRow, startCol, endRow, endCol)

                    #else:
                        #print(f'move to {(endRow, endCol)} is illegal')

    ## DRAW #
    window.fill((0, 0, 0))
    drawSquares(window, colour1, colour2, BOARDWIDTH, BOARDHEIGHT, BOXSIZE)

    highlightMostRecentMove(window, lastMove, highlightColour, BOXSIZE)

    if draggedPiece != None:
        highlightLegalSquares(window, isLegal(draggedPiece), BOXSIZE)

    drawPieces(window, board, BOXSIZE)
    checkForPromotion()
    displayCurrrentFEN(window, currentFEN, SCREENHEIGHT)

    if drag: # if a piece is currently being dragged
        drawPieceOnCursor(window, draggedPieceSprite, mousex, mousey)
    
    if GameEnded:
        drawCheckmateIcon(window, BOARDHEIGHT, BOARDWIDTH)

    clock.tick(20)
    pygame.display.update()
