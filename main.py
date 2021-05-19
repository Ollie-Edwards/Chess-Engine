import pygame

WIDTH = 400
HEIGHT = 400

BOXSIZE = WIDTH//8

colour1 = (118,150,86) # 182, 136, 96
colour2 = (238,238,210) # 241, 218, 179

startRow = 0
startCol = 0

clicked = False ## whether or not a piece has been clicked

totalMoveNumber = 0

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
    "!":"!"
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

class Piece:
    def __init__(self, piece, row, col):
        self.row = row
        self.col = col
        self.piece = piece
        self.numberOfMoves = 0

    def Move(self, endRow, endCol):
        board[endCol][endRow] = self
        board[self.col][self.row] = Piece('!', self.row, self.col)
        self.col = endCol
        self.row = endRow

def checkForPromotion():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.piece == "P" and piece.col == 0:
                board[piece.col][piece.row].piece = "Q"
            if piece.piece == "p" and piece.col == 7:
                board[piece.col][piece.row].piece = "q"

#normal chess starting position
#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
def drawpiece(piece, row, col):
    piece = pygame.transform.scale(piece, (BOXSIZE, BOXSIZE)) 
    window.blit(piece, (row*BOXSIZE, col*BOXSIZE))

def drawSquares():
    ## draw boxes
    
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

def isLegal(piece):
    ## ill just worry about white pieces for now
  
    # + row --> right
    # - row --> left
    # + col --> down
    # - col --> up

    if (piece.piece).isupper():
        verticalDirection = 1 # is this is -1 the column numbers will be the negative verson of themself, instead of moving up they will move down
                            # this means that you the legal moves for black pieces can be calcualted without having to rewrite the code
                            # 1 for white pieces and -1 for black pieces
    else:
        verticalDirection = -1

    legalMoves = []

    if piece.piece.lower() == "p":
        if piece.numberOfMoves == 0:
            if Getpiece(piece.row, piece.col-2*verticalDirection) == None: # forwards 2
                legalMoves.append((piece.row, piece.col-2*verticalDirection))

        if Getpiece(piece.row, piece.col-1*verticalDirection) == None: # forwards 1
            legalMoves.append((piece.row, piece.col-1*verticalDirection))

        if Getpiece(piece.row-1, piece.col-1*verticalDirection) != None: # forwards and left
            if Getpiece(piece.row-1, piece.col-1*verticalDirection).islower():
                legalMoves.append((piece.row-1, piece.col-1*verticalDirection))

        if Getpiece(piece.row+1, piece.col-1*verticalDirection) != None: # forwards and left
            if Getpiece(piece.row+1, piece.col-1*verticalDirection).islower():
                legalMoves.append((piece.row+1, piece.col-1*verticalDirection))
            
        ## en passant
    if piece.piece.lower() == "n":
        for i in range(-1, 2, 2):
            try:
                verticalDirection = i
                if Getpiece(piece.row+1, piece.col-2*verticalDirection) == None: # forward 2 right 1
                    legalMoves.append((piece.row+1, piece.col-2*verticalDirection))
                if Getpiece(piece.row+1, piece.col-2*verticalDirection) == None: # forward 2 right 1
                    legalMoves.append((piece.row-1, piece.col-2*verticalDirection))

                if Getpiece(piece.row+2, piece.col-1*verticalDirection) == None: # forward 1 right 2
                    legalMoves.append((piece.row+2, piece.col-1*verticalDirection))
                if Getpiece(piece.row-2, piece.col-1*verticalDirection) == None: # forward 1 left 2
                    legalMoves.append((piece.row-2, piece.col-1*verticalDirection))  
            except:
                pass
    if piece.piece.lower() == "b" or piece.piece.lower() == "q":
        for j in range(-1, 2, 2):
            verticalDirection = j
            for i in range(1, 8):
                try:
                    if Getpiece(piece.row-i*verticalDirection, piece.col-i*verticalDirection) == None: # forward 1 right 2
                        legalMoves.append((piece.row-i*verticalDirection, piece.col-i*verticalDirection))
                    else:
                       pass

                except:
                    pass

                try:
                    if Getpiece(piece.row+i*verticalDirection, piece.col-i*verticalDirection) == None: # forward 1 right 2
                        legalMoves.append((piece.row+i*verticalDirection, piece.col-i*verticalDirection))
                    else:
                        pass
                except:
                    pass
    if piece.piece.lower() == "r" or piece.piece.lower() == "q":
        for j in range(-1, 2, 2):
            verticalDirection = j
            print(verticalDirection)
            for i in range(1, 8):
                try:
                    if Getpiece(piece.row, piece.col-i*verticalDirection) == None: # forward 1 right 2
                        legalMoves.append((piece.row, piece.col-i*verticalDirection))
                    else:
                        pass
                except:
                    pass
                try:
                    if Getpiece(piece.row-i*verticalDirection, piece.col) == None: # forward 1 right 2
                        legalMoves.append((piece.row-i*verticalDirection, piece.col))
                    else:
                        pass
                except:
                    pass
    if piece.piece.lower() == "k":
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    if Getpiece(piece.row+i, piece.col+j) == None: # forward 1 right 2
                            legalMoves.append((piece.row+i, piece.col+j))
                    if Getpiece(piece.row-i, piece.col) == None: # forward 1 right 2
                            legalMoves.append((piece.row-i, piece.col))
                    if Getpiece(piece.row, piece.col-i) == None: # forward 1 right 2
                            legalMoves.append((piece.row, piece.col-i))
                except:
                    pass

# if target piece != None
# if targetnode == oppostie colour
#   add to legalmoves
#   break

    print(f"for the point {piece.row, piece.col}, the legal moves are:{legalMoves}")
    return legalMoves
            
def highlightLegalSquares(piece):
    legalmoves = isLegal(piece)
    for item in legalmoves:
        row = item[0]
        col = item[1]
        rect = pygame.Rect(row*BOXSIZE, col*BOXSIZE, BOXSIZE, BOXSIZE) #left, top, width, height 
        pygame.draw.rect(window, (0, 0, 100), rect)

###################### getting starting board positions ######################

FENinput = input('enter FEN notation code or type none: ')

if FENinput == "none":#rnbqkbnr/pppppppp/8/8/rnbqkbnr/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

    FENinput = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" ## code for the normal chess starting position
    
try:
    boardPositions, sideToMove, castlingAblility, enPassantTargetSquare, halfmoveClock, fullMoveCounter = FENinput.split(" ")
except:
    raise pygame.error('invalid FEN input')

board = parseFEN(boardPositions)

###############################################################################

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))

drag = False
clickedPieceSprite = blackKing
clickedPiece = None

startRow = 0 # the row/col of where the most recent piece has been moved from
startCol = 0

################################## Main loop ##################################

while True:
    checkForPromotion()

    ## DRAW ##
    drawSquares()

    if clickedPiece != None:
        highlightLegalSquares(clickedPiece)

    drawPieces()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()

        mousex, mousey = pygame.mouse.get_pos()
        clickedRow = mousex//BOXSIZE
        clickedCol = mousey//BOXSIZE

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed() != (False, False, False):
                drag = True
                startRow = clickedRow
                startCol = clickedCol
                clickedPieceSprite = sprites[board[clickedCol][clickedRow].piece]
                clickedPiece = board[clickedCol][clickedRow]
 
        if event.type == pygame.MOUSEBUTTONUP:
            drag = False
            if clickedPiece != None:
                if (clickedRow, clickedCol) in isLegal(clickedPiece):
                    if (totalMoveNumber % 2 == 0 and clickedPiece.piece.isupper()) or (totalMoveNumber % 2 != 0 and clickedPiece.piece.islower()):
                
                        board[clickedCol][clickedRow] = clickedPiece
                        board[clickedCol][clickedRow].row = clickedRow
                        board[clickedCol][clickedRow].col = clickedCol
                        board[clickedCol][clickedRow].numberOfMoves += 1
                        board[startCol][startRow] = Piece("!", startRow, startCol) # empty node
                        totalMoveNumber += 1
        
        if drag:
            if clickedPieceSprite != "!":
                window.blit(clickedPieceSprite, (mousex-22.5, mousey-22.5))

    if clicked: # this checks whether the board has been clicked since startup
        rect = pygame.Rect(clickedRow*BOXSIZE, clickedCol*BOXSIZE, BOXSIZE, BOXSIZE) #left, top, width, height 
        pygame.draw.rect(window, (0, 128, 0), rect)


    clock.tick(20)
    pygame.display.update()
