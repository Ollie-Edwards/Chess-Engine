import pygame
# from pygame import color
# from pygame import draw
# from pygame.mixer import pre_init

WIDTH = 400
HEIGHT = 400

BOXSIZE = WIDTH//8

board = ([[[]for i in range(8)]for i in range(8)])

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))

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

def drawpiece(piece, row, col):
    piece = pygame.transform.scale(piece, (BOXSIZE, BOXSIZE)) 
    window.blit(piece, (row*BOXSIZE, col*BOXSIZE))

#startig position
#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w
### load FEN input
#importBoard = input('enter FEN code: ')

#boardPositions, sideToMove = importBoard.split(" ")

#rowNum, colNum = 0, 0

board = [
    [["r"],["b"],["n"],["q"],["k"],["n"],["b"],["r"]],
    [["p"],["p"],["p"],["p"],["p"],["p"],["p"],["p"]],
    [[""],[""],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[]],
    [["P"],["P"],["P"],["P"],["P"],["P"],["P"],["P"]],
    [["R"],["B"],["N"],["K"],["Q"],["N"],["B"],["R"]]
]

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
            letter = str(board[col][row])  # returns "[]", "['p']" esc

            if letter != "[]":
                letter = letter[2]

            if letter == "P":
                drawpiece(blackPawn, row, col)
            if letter == "N":
                drawpiece(blackKnight, row, col)
            if letter == "B":
                drawpiece(blackBishop, row, col)
            if letter == "R":
                drawpiece(blackRook, row, col)
            if letter == "Q":
                drawpiece(blackQueen, row, col)
            if letter == "K":
                drawpiece(blackKing, row, col)
            if letter == "p":
                drawpiece(whitePawn, row, col)
            if letter == "n":
                drawpiece(whiteKnight, row, col)
            if letter == "b":
                drawpiece(whiteBishop, row, col)
            if letter == "r":
                drawpiece(whiteRook, row, col)
            if letter == "q":
                drawpiece(whiteQueen, row, col)
            if letter == "k":
                drawpiece(whiteKing, row, col)  

def isValid():
    pass

def move(startRow, startCol, endRow, endCol):
    # isValid()
    piece = board[startRow][startCol]
    if piece != []:
        board[startCol][startRow] = []
        board[endCol][endRow] = piece

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
