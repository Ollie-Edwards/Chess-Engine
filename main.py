import pygame
import datetime

from API import *
check()

BOARDWIDTH = 400
BOARDHEIGHT = 400

SCREENWIDTH = 420
SCREENHEIGHT = 400

BOXSIZE = BOARDWIDTH//8

# green shades
colour1 = (118,150,86)
colour2 = (238,238,210)

# classic wood
# colour1 = (182, 136, 96)
# colour2 = (241, 218, 179)

startRow = 0
startCol = 0

clicked = False ## whether or not a piece has been clicked

totalMoveNumber = 0
fullMoveNumber = 0

blackBishop = pygame.image.load(r"Sprites\blackBishop.png")
blackKing = pygame.image.load(r"Sprites\blackKing.png")
blackKnight = pygame.image.load(r"Sprites\blackKnight.png")
blackPawn = pygame.image.load(r"Sprites\blackPawn.png")
blackQueen = pygame.image.load(r"Sprites\blackQueen.png")
blackRook = pygame.image.load(r"Sprites\blackRook.png")
 
whiteBishop = pygame.image.load(r"Sprites\whiteBishop.png")
whiteKing = pygame.image.load(r"Sprites\whiteKing.png")
whiteKnight = pygame.image.load(r"Sprites\whiteKnight.png")
whitePawn = pygame.image.load(r"Sprites\whitePawn.png")
whiteQueen = pygame.image.load(r"Sprites\whiteQueen.png")
whiteRook = pygame.image.load(r"Sprites\whiteRook.png")

checkmateIcon = pygame.image.load(r"Sprites\CheckmateIcon.png")

sprites = {
    "p":blackPawn, "P":whitePawn,
    "n":blackKnight, "N":whiteKnight,
    "b":blackBishop, "B":whiteBishop,
    "r":blackRook, "R":whiteRook,
    "q":blackQueen, "Q":whiteQueen,
    "k":blackKing, "K":whiteKing,
    "!":None
}
'''
white = uppercase 
pawn = p
knight = n
bishop = b
rook = r
queen = q
king = k
none = !
'''

totalMoveNumber = 0
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
            piece = board[row][col]
            if piece.piece == "P" and piece.col == 0:
                board[piece.col][piece.row].piece = "Q"
            if piece.piece == "p" and piece.col == 7:
                board[piece.col][piece.row].piece = "q"

def getAllLegalMoves(board, colour): # colour "b" or "w"
    allLegalMoves = []
    for row in board:
        for item in row: # for each individual piece on the board
            
            if item.colour == colour: # if it is the desired colour
                for legalmove in isLegal(item): # add each legalmove to the full list of legal moves for that colour
                    allLegalMoves.append(legalmove)
    return allLegalMoves

def drawpiece(piece, row, col):
    piece = pygame.transform.scale(piece, (BOXSIZE, BOXSIZE)) 
    window.blit(piece, (row*BOXSIZE, col*BOXSIZE))

def drawSquares(): ## draw boxes
    rowLetters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    colNumbers = ["8", "7", "6", "5", "4", "3", "2", "1"]

    font = pygame.font.SysFont(None, 16)
    offset = 10

    for row in range(BOARDWIDTH//BOXSIZE):
        for col in range(BOARDHEIGHT//BOXSIZE):
            rowColSum = row+col
            if rowColSum % 2 == 0:
                colour = colour1
                oppositecolour = colour2
            else:
                colour = colour2
                oppositecolour = colour1

            rect = pygame.Rect(row*BOXSIZE, col*BOXSIZE, BOXSIZE, BOXSIZE) #left, top, width, height 
            pygame.draw.rect(window, colour, rect)

            # window.blit(img, (WIDTH+offset*2, offset+(row*BOXSIZE)))

            if col == 7:
                img = font.render(rowLetters[row], True, oppositecolour)
                window.blit(img, (((row+1)*BOXSIZE)-offset, BOARDHEIGHT-offset))
            
            if row == 7:
                img = font.render(colNumbers[col], True, colour)
                window.blit(img, (offset//3, offset//3+(col*BOXSIZE)))

def drawPieces(board):
    for row in range(8):
        for col in range(8):
            letter = board[col][row].piece  # the character representation of the chess piece eg. k, n, p esc
            if letter != "!":
                drawpiece(sprites[letter], row, col)

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

def Getpiece(row, col): #returns the piece in the given row and col
    piece = board[col][row].piece
    if piece == "!":
        return None
    else:
        return piece

def isLegal(InputPiece):  
    # + row --> right
    # - row --> left
    # + col --> down
    # - col --> up

    verticalDirection = 1 # if this is -1 the col/row numbers will be the negative verson of themself, instead of move up --> move down, left --> right

    legalMoves = []

    if InputPiece.piece == "P":
        if InputPiece.numberOfMoves == 0:
            if Getpiece(InputPiece.row, InputPiece.col-2) == None: # forwards 2
                legalMoves.append((InputPiece.row, InputPiece.col-2))

        targetPiece = Getpiece(InputPiece.row, InputPiece.col-1) # up 1
        if targetPiece == None:
            legalMoves.append((InputPiece.row, InputPiece.col-1))

        try:
            targetPiece = Getpiece(InputPiece.row-1, InputPiece.col-1) # up and left
            if targetPiece != None:
                if targetPiece.islower():
                    legalMoves.append((InputPiece.row-1, InputPiece.col-1))
        except:
            pass

        try:
            targetPiece = Getpiece(InputPiece.row+1, InputPiece.col-1) # up and right
            if targetPiece != None:
                if targetPiece.islower():
                    legalMoves.append((InputPiece.row+1, InputPiece.col-1))
        except:
            pass

    if InputPiece.piece == "p": # i could probably combine this and the last check
        if InputPiece.numberOfMoves == 0:
            if Getpiece(InputPiece.row, InputPiece.col+2) == None: # down 2
                legalMoves.append((InputPiece.row, InputPiece.col+2))

        targetPiece = Getpiece(InputPiece.row, InputPiece.col+1) ## down 1
        if targetPiece == None:
            legalMoves.append((InputPiece.row, InputPiece.col+1))

        try:
            targetPiece = Getpiece(InputPiece.row-1, InputPiece.col+1) # down 1 and left
            if targetPiece != None:
                if targetPiece.isupper():
                    legalMoves.append((InputPiece.row-1, InputPiece.col+1))
        except:
            pass

        try:
            targetPiece = Getpiece(InputPiece.row+1, InputPiece.col+1) # down 1 and right
            if targetPiece != None:
                if targetPiece.isupper():
                    legalMoves.append((InputPiece.row+1, InputPiece.col+1))
        except:
            pass

        ## en passant
    #good

    if InputPiece.piece.lower() == "n":
        for i in range(-1, 2, 2):
            verticalDirection = i
            possibleMoves = [(InputPiece.row+1, InputPiece.col-2*verticalDirection), (InputPiece.row-1, InputPiece.col-2*verticalDirection), (InputPiece.row+2, InputPiece.col-1*verticalDirection), (InputPiece.row-2, InputPiece.col-1*verticalDirection)]
            for j in possibleMoves:
                try:
                    targetPiece = Getpiece(j[0], j[1])
                    if (targetPiece == None) or (InputPiece.piece.isupper() and targetPiece.islower()) or (InputPiece.piece.islower() and targetPiece.isupper()): # up/down 2 right 1
                        legalMoves.append((j))
                except:
                    pass
    #good

    if InputPiece.piece.lower() == "b" or InputPiece.piece.lower() == "q":
        for j in range(-1, 2, 2):
            verticalDirection = j       
            for i in range(1, 8):
                try:
                    targetPiece = Getpiece(InputPiece.row+i, InputPiece.col+i*verticalDirection)
                    if (targetPiece == None):
                        legalMoves.append((InputPiece.row+i, InputPiece.col+i*verticalDirection))
                    if (InputPiece.piece.isupper() and targetPiece.islower()) or (InputPiece.piece.islower() and targetPiece.isupper()):
                        legalMoves.append((InputPiece.row+i, InputPiece.col+i*verticalDirection))
                        break
                    if (InputPiece.piece.isupper() and targetPiece.isupper()) or (InputPiece.piece.islower() and targetPiece.islower()):
                        break
                except:
                    pass
            for i in range(1, 8):
                try:
                    targetPiece = Getpiece(InputPiece.row-i, InputPiece.col+i*verticalDirection)
                    if (targetPiece == None):
                        legalMoves.append((InputPiece.row-i, InputPiece.col+i*verticalDirection))
                    if (InputPiece.piece.isupper() and targetPiece.islower()) or (InputPiece.piece.islower() and targetPiece.isupper()):
                        legalMoves.append((InputPiece.row-i, InputPiece.col+i*verticalDirection))
                        break
                    if (InputPiece.piece.isupper() and targetPiece.isupper()) or (InputPiece.piece.islower() and targetPiece.islower()):
                        break
                except:
                    pass
    #not good
    
    if InputPiece.piece.lower() == "r" or InputPiece.piece.lower() == "q":
        for j in range(-1, 2, 2):
            verticalDirection = j
            for i in range(1, 8):
                try: # down/up
                    targetPiece = Getpiece(InputPiece.row, InputPiece.col+i*verticalDirection)
                    if (targetPiece == None):
                        legalMoves.append((InputPiece.row, InputPiece.col+i*verticalDirection))

                    if (InputPiece.piece.isupper() and targetPiece.islower()) or (InputPiece.piece.islower() and targetPiece.isupper()): # if the target square is the opposition
                        legalMoves.append((InputPiece.row, InputPiece.col+i*verticalDirection))
                        break
                    elif (InputPiece.piece.isupper() and targetPiece.isupper()) or (InputPiece.piece.islower() and targetPiece.islower()):
                        break
                except:
                    pass
            for i in range(1, 8):
                try: # left/right
                    targetPiece = Getpiece(InputPiece.row+i*verticalDirection, InputPiece.col)
                    if (targetPiece == None):
                        legalMoves.append((InputPiece.row+i*verticalDirection, InputPiece.col))

                    if (InputPiece.piece.isupper() and targetPiece.islower()) or (InputPiece.piece.islower() and targetPiece.isupper()): # if the target square is the opposition
                        legalMoves.append((InputPiece.row+i*verticalDirection, InputPiece.col))
                        break
                    elif (InputPiece.piece.isupper() and targetPiece.isupper()) or (InputPiece.piece.islower() and targetPiece.islower()):
                        break
                except:
                    pass
    #good

    if InputPiece.piece.lower() == "k":
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    if Getpiece(InputPiece.row+i, InputPiece.col+j) == None: # forward 1 right 2
                            legalMoves.append((InputPiece.row+i, InputPiece.col+j))
                    if Getpiece(InputPiece.row-i, InputPiece.col) == None: # forward 1 right 2
                            legalMoves.append((InputPiece.row-i, InputPiece.col))
                    if Getpiece(InputPiece.row, InputPiece.col-i) == None: # forward 1 right 2
                            legalMoves.append((InputPiece.row, InputPiece.col-i))
                except:
                    pass

    legalMoves = list(legalMoves)
    removedOutsideGrid = []

    for move in legalMoves: # this is a temporary fix to remove possible moves that sit outside the 8x8 grid
        if not(move[0] > 7 or move[0] < 0 or move[1] > 7 or move[1] < 0):
            removedOutsideGrid.append(move)

    return removedOutsideGrid
            
def highlightLegalSquares(piece):
    legalmoves = isLegal(piece)
    for item in legalmoves:
        row = item[0]
        col = item[1]
        rect = pygame.Rect(row*BOXSIZE, col*BOXSIZE, BOXSIZE, BOXSIZE) #left, top, width, height 
        pygame.draw.rect(window, (18, 72, 181), rect)

def movePiece(InputBoard, startrow, startcol, endrow, endcol):
    print(f"{startrow, startcol} moved to {endrow, endcol}")
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
            targetPiece = board[row][col]
            if targetPiece.piece.lower() == "k" and targetPiece.colour == colour: # if target piece is a king AND if targetpeice is the correct colour 
                oppositionColour = targetPiece.oppositionColour 
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

def displayCurrrentFEN(FEN):
    font = pygame.font.SysFont(None, 12)
    offset = 10

    img = font.render(f"Current FEN: {FEN}", True, (255, 255, 255))
    window.blit(img, (0+offset,SCREENHEIGHT+offset//2))    

def isCheckmate(board, colour):
    (kingRow, kingCol) , oppositionColour = getKingPosition(board, colour)

    if isInCheck(board, colour) == False:
        return False

    legalKingMoves = isLegal(board[kingCol][kingRow])
    
    if legalKingMoves == []:
        return True 
    
    for move in legalKingMoves:
        print('LOJBDOJGB', move)
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

###################### getting starting board positions ######################

FENinput = input('enter FEN notation code or type none: ')

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((SCREENHEIGHT, SCREENWIDTH))

#normal chess starting position
#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

# check situation
# 1q4r1/4k3/8/8/8/8/8/Q1K5 w - - 0 1

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

        keys = pygame.key.get_pressed()

        mousex, mousey = pygame.mouse.get_pos()
        clickedRow = mousex//BOXSIZE
        clickedCol = mousey//BOXSIZE

        if not GameEnded:
            if isCheckmate(board, "b") == True:
                GameEnded = True

            if (totalMoveNumber % 2 != 0): # if it is the computers turn (computer plays as white)
                currentFEN = getFEN(board)
                print(currentFEN)   

                startRow, startCol, endRow, endCol = GetNextMove(currentFEN)
                board = movePiece(board, startRow, startCol, endRow, endCol)
                totalMoveNumber += 1 

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
                endRow = clickedRow
                endCol = clickedCol
                drag = False
                print('start')
                if draggedPiece != None: # if draggedpiece has been dropped
                    if (endRow, endCol) in isLegal(draggedPiece): # if the final square is legal
                        if (totalMoveNumber % 2 == 0 and draggedPiece.piece.islower()): # if it is black's turn and the moved piece is black
                            currentFEN = getFEN(board)
                            print(currentFEN)

                            testBoard = board
                            movePiece(testBoard, startRow, startCol, endRow, endCol)

                            drawSquares()
                            drawPieces(testBoard)
                            pygame.display.update() 

                            if isInCheck(testBoard, "b") == True or isInCheck(board, "b") == True: 
                                board = movePiece(board, endRow, endCol, startRow, startCol) # move the peice from start to finish
                                print("you're in check")

                            else:
                                board = movePiece(board, startRow, startCol, endRow, endCol) # move the peice from start to finish

                                totalMoveNumber += 1 
                                fullMoveNumber += 1

                    else:
                        print(f'move to {(endRow, endCol)} is illegal')
                print('\n')

            if keys[pygame.K_a]:
                isInCheck(board, "b")

    ## DRAW #
    window.fill((0, 0, 0))
    drawSquares()

    if draggedPiece != None:
        highlightLegalSquares(draggedPiece)

    drawPieces(board)
    checkForPromotion()
    displayCurrrentFEN(currentFEN)

    if drag: # if a piece is currently being dragged
        if draggedPieceSprite != "!":
            try:
                window.blit(draggedPieceSprite, (mousex-22.5, mousey-22.5)) # draw the dragged piece onto the mouse cursor 
            except:
                pass
    
    if GameEnded:
        checkmateIcon = pygame.transform.scale(checkmateIcon, (BOARDHEIGHT//3, BOARDWIDTH//3)) 
        window.blit(checkmateIcon, ((BOARDHEIGHT//3), BOARDWIDTH//3)) 

    clock.tick(20)
    pygame.display.update()
