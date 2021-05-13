import pygame

WIDTH = 400
HEIGHT = 400

BOXSIZE = WIDTH//8

colour1 = (238,238,210)
colour2 = (118,150,86)

startRow = 0
startCol = 0

drag = False ## whether or not a piece has been clicked

'''
side to move = uppercase 

None = . 
pawn = p
knight = n
bishop = b
rook = r
queen = q
king = k
none = !
'''

blackBishop = pygame.image.load(r"Chess-Engine\Sprites\blackBishop.png")
blackKing = pygame.image.load(r"Chess-Engine\Sprites\blackKing.png")
blackKnight = pygame.image.load(r"Chess-Engine\Sprites\blackKnight.png")
blackPawn = pygame.image.load(r"Chess-Engine\Sprites\blackPawn.png")
blackQueen = pygame.image.load(r"Chess-Engine\Sprites\blackQueen.png")
blackRook = pygame.image.load(r"Chess-Engine\Sprites\blackRook.png")

whiteBishop = pygame.image.load(r"Chess-Engine\Sprites\whiteBishop.png")
whiteKing = pygame.image.load(r"Chess-Engine\Sprites\whiteKing.png")
whiteKnight = pygame.image.load(r"Chess-Engine\Sprites\whiteKnight.png")
whitePawn = pygame.image.load(r"Chess-Engine\Sprites\whitePawn.png")
whiteQueen = pygame.image.load(r"Chess-Engine\Sprites\whiteQueen.png")
whiteRook = pygame.image.load(r"Chess-Engine\Sprites\whiteRook.png")

#normal chess starting position
#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

def drawpiece(piece, row, col):
    piece = pygame.transform.scale(piece, (BOXSIZE, BOXSIZE)) 
    window.blit(piece, (row*BOXSIZE, col*BOXSIZE))

def drawBoard():
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

            ## draw pieces
    for row in range(WIDTH//BOXSIZE):
        for col in range(HEIGHT//BOXSIZE):
            letter = str(board[col][row])  # the character representation of the chess piece eg. k, n, p esc

            if letter == "p":
                drawpiece(blackPawn, row, col)
            if letter == "n":
                drawpiece(blackKnight, row, col)
            if letter == "b":
                drawpiece(blackBishop, row, col)
            if letter == "r":
                drawpiece(blackRook, row, col)
            if letter == "q":
                drawpiece(blackQueen, row, col)
            if letter == "k":
                drawpiece(blackKing, row, col)
            if letter == "P":
                drawpiece(whitePawn, row, col)
            if letter == "N":
                drawpiece(whiteKnight, row, col)
            if letter == "B":
                drawpiece(whiteBishop, row, col)
            if letter == "R":
                drawpiece(whiteRook, row, col)
            if letter == "Q":
                drawpiece(whiteQueen, row, col)
            if letter == "K":
                drawpiece(whiteKing, row, col)  
            if letter == "!":
                pass

def isValid():
    pass

def move(startRow, startCol, endRow, endCol):
    # isValid()
    piece = board[startRow][startCol]
    if piece != []:
        board[startCol][startRow] = []
        board[endCol][endRow] = piece

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

    currentCol = 0
    currentRow = 0
    board = ([[[]for i in range(8)]for i in range(8)])
    for letter in FEN:

        board[currentCol][currentRow] = letter
        currentRow += 1

        if currentRow == 8:
            currentRow = 0
            currentCol += 1
        if currentCol == 8:
            return board

###################### getting starting board positions ######################

FENinput = input('enter FEN notation code or type none: ')

if FENinput == "none":
    FENinput = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" ## code for the normal chess starting position
    
try:
    boardPositions, sideToMove, castlingAblility, enPassantTargetSquare, halfmoveClock, fullMoveCounter = FENinput.split(" ")
except:
    raise pygame.error('invalid FEN input')

board = parseFEN(boardPositions)

###############################################################################

################################## Main loop ##################################

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()

        mousex, mousey = pygame.mouse.get_pos()
        clickedRow = mousex//BOXSIZE
        clickedCol = mousey//BOXSIZE

        if pygame.mouse.get_pressed()[0]: # left click
            if drag == False:
                startCol = clickedCol
                startRow = clickedRow

                board[startCol][startRow] = [""]

                print(f"picked up {startCol}, {startRow}")
                drag = True
            else:
                endCol, endRow = clickedCol, clickedRow

                move(startRow, startCol, endRow, endCol)
                print('placed')
                drag = False

    drawBoard()
    clock.tick(5)
    pygame.display.update()
