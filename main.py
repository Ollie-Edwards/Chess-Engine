import pygame
from pygame.constants import K_q, K_w

from API import *
check()

WIDTH = 400
HEIGHT = 400

BOXSIZE = WIDTH//8

#colour1 = (118,150,86)
colour2 = (238,238,210)

colour1 = (182, 136, 96)
#colour2 = (241, 218, 179)

startRow = 0
startCol = 0

clicked = False ## whether or not a piece has been clicked

totalMoveNumber = 0
fullMoveNumber = 0

blackBishop = pygame.image.load(r"Chess\Sprites\blackBishop.png")
blackKing = pygame.image.load(r"Chess\Sprites\blackKing.png")
blackKnight = pygame.image.load(r"Chess\Sprites\blackKnight.png")
blackPawn = pygame.image.load(r"Chess\Sprites\blackPawn.png")
blackQueen = pygame.image.load(r"Chess\Sprites\blackQueen.png")
blackRook = pygame.image.load(r"Chess\Sprites\blackRook.png")
 
whiteBishop = pygame.image.load(r"Chess\Sprites\whiteBishop.png")
whiteKing = pygame.image.load(r"Chess\Sprites\whiteKing.png")
whiteKnight = pygame.image.load(r"Chess\Sprites\whiteKnight.png")
whitePawn = pygame.image.load(r"Chess\Sprites\whitePawn.png")
whiteQueen = pygame.image.load(r"Chess\Sprites\whiteQueen.png")
whiteRook = pygame.image.load(r"Chess\Sprites\whiteRook.png")

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
        print(newstring+" w - - 0 1") #output if no changes made
        return (newstring+" w - - 0 1")

    else:
        print(newstring+" w - - 0 1") #output new string
        return (newstring+" w - - 0 1")

def checkForPromotion():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.piece == "P" and piece.col == 0:
                board[piece.col][piece.row].piece = "Q"
            if piece.piece == "p" and piece.col == 7:
                board[piece.col][piece.row].piece = "q"

def drawpiece(piece, row, col):
    piece = pygame.transform.scale(piece, (BOXSIZE, BOXSIZE)) 
    window.blit(piece, (row*BOXSIZE, col*BOXSIZE))

def drawSquares(): ## draw boxes
    for row in range(WIDTH//BOXSIZE):
        for col in range(HEIGHT//BOXSIZE):
            if row % 2 == 0:
                if col % 2 == 0:
                    colour = colour1
                else:
                    colour = colour2
            else:
                if col % 2 == 0:
                    colour = colour2
                else:
                    colour = colour1

            rect = pygame.Rect(row*BOXSIZE, col*BOXSIZE, BOXSIZE, BOXSIZE) #left, top, width, height 
            pygame.draw.rect(window, colour, rect)

def drawPieces():
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

def movePiece(startrow, startcol, endrow, endcol):
    print(f"{startrow, startcol} moved to {endrow, endcol}")
    board[endcol][endrow] = board[startcol][startrow]
    board[endcol][endrow].row = endrow
    board[endcol][endrow].col = endcol
    board[endcol][endrow].numberOfMoves += 1
    board[startcol][startrow] = Piece("!", startrow, startcol) # empty node

###################### getting starting board positions ######################

FENinput = input('enter FEN notation code or type none: ')

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))

#normal chess starting position
#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

if FENinput == "none":

    FENinput = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" ## code for the normal chess starting position
    
try:
    boardPositions, sideToMove, castlingAblility, enPassantTargetSquare, halfmoveClock, fullMoveCounter = FENinput.split(" ")
except:
    raise pygame.error('invalid FEN input')

board = parseFEN(boardPositions)

###############################################################################

def getAllLegalMoves(colour): # colour "b" or "w"
    allLegalMoves = []
    for row in board:
        for item in row: # for each individual piece on the board
            
            if item.colour == colour: # if it is the desired colour
                for legalmove in isLegal(item): # add each legalmove to the full list of legal moves for that colour
                    allLegalMoves.append(legalmove)
    return allLegalMoves

################################## Main loop ##################################

while True:
    ## DRAW #
    drawSquares()

    if draggedPiece != None:
        highlightLegalSquares(draggedPiece)

    drawPieces()
    checkForPromotion()

    if (totalMoveNumber % 2 == 0): # if it is the computers turn (computer plays as white)
        startRow, startCol, endRow, endCol = GetNextMove(getFEN(board))
        movePiece(startRow, startCol, endRow, endCol)
        totalMoveNumber += 1 

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()

        keys = pygame.key.get_pressed()

        mousex, mousey = pygame.mouse.get_pos()
        clickedRow = mousex//BOXSIZE
        clickedCol = mousey//BOXSIZE

        if event.type == pygame.MOUSEBUTTONDOWN: # begining of a drag
            if pygame.mouse.get_pressed() != (False, False, False):
                drag = True
                startRow = clickedRow
                startCol = clickedCol # clicked col is the end  col
                draggedPieceSprite = sprites[board[startCol][startRow].piece]
                draggedPiece = board[startCol][startRow]
 
        if event.type == pygame.MOUSEBUTTONUP: # end of a drag
            endRow = clickedRow
            endCol = clickedCol
            drag = False
            if draggedPiece != None:
                if (endRow, endCol) in isLegal(draggedPiece):
                    if (totalMoveNumber % 2 != 0 and draggedPiece.piece.islower()):
                        movePiece(startRow, startCol, endRow, endCol)
                        totalMoveNumber += 1 
                        fullMoveNumber += 1
                        drawSquares()
                        drawPieces()
                        pygame.display.update()
                else:
                    print(f'move to {(endRow, endCol)} is illegal')
        
        if drag: # if a piece is currently being dragged
            if draggedPieceSprite != "!":
                try:
                    window.blit(draggedPieceSprite, (mousex-22.5, mousey-22.5)) # draw the dragged piece onto the mouse cursor 
                except:
                    pass

        if keys[K_q]:
            print('1')
            for square in getAllLegalMoves("w"):
                rect = pygame.Rect(square[0]*BOXSIZE, square[1]*BOXSIZE, BOXSIZE, BOXSIZE) #left, top, width, height 
                pygame.draw.rect(window, (100, 100, 100), rect)
            pygame.display.update()
            pygame.time.delay(500)

        if keys[K_w]:
            for square in getAllLegalMoves("b"):
                rect = pygame.Rect(square[0]*BOXSIZE, square[1]*BOXSIZE, BOXSIZE, BOXSIZE) #left, top, width, height 
                pygame.draw.rect(window, (100, 100, 100), rect)
            pygame.display.update()
            pygame.time.delay(500)

    clock.tick(20)
    pygame.display.update()
