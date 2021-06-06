
import pygame

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

def drawpiece(window, boxSize, piece, row, col):
    piece = pygame.transform.scale(piece, (boxSize, boxSize)) 
    window.blit(piece, (row*boxSize, col*boxSize))

def drawSquares(window, colour1, colour2, boardWidth, boardHeight, boxSize): ## draw boxes
    rowLetters = ["a", "b", "c", "d", "e", "f", "g", "h"]
    colNumbers = ["8", "7", "6", "5", "4", "3", "2", "1"]

    font = pygame.font.SysFont(None, 16)
    offset = 10

    for row in range(boardWidth//boxSize):
        for col in range(boardHeight//boxSize):
            rowColSum = row+col
            if rowColSum % 2 == 0:
                colour = colour1
                oppositecolour = colour2
            else:
                colour = colour2
                oppositecolour = colour1

            rect = pygame.Rect(row*boxSize, col*boxSize, boxSize, boxSize) #left, top, width, height 
            pygame.draw.rect(window, colour, rect)

            # window.blit(img, (WIDTH+offset*2, offset+(row*BOXSIZE)))

            if col == 7:
                img = font.render(rowLetters[row], True, oppositecolour)
                window.blit(img, (((row+1)*boxSize)-offset, boardHeight-offset))
            
            if row == 7:
                img = font.render(colNumbers[col], True, colour)
                window.blit(img, (offset//3, offset//3+(col*boxSize)))

def drawPieces(window, board, boxSize):
    for row in range(8):
        for col in range(8):
            letter = board[col][row].piece  # the character representation of the chess piece eg. k, n, p esc
            if letter != "!":
                drawpiece(window, boxSize, sprites[letter], row, col)

def highlightLegalSquares(window, legalmoves, boxSize):
    #legalmoves = isLegal(piece)
    for item in legalmoves:
        row = item[0]
        col = item[1]
        rect = pygame.Rect(row*boxSize, col*boxSize, boxSize, boxSize) #left, top, width, height 
        pygame.draw.rect(window, (18, 72, 181), rect)

def displayCurrrentFEN(window, FEN, screenHeight):
    font = pygame.font.SysFont(None, 12)
    offset = 10

    img = font.render(f"Current FEN: {FEN}", True, (255, 255, 255))
    window.blit(img, (0+offset,screenHeight+offset//2))    

def highlightMostRecentMove(window, lastMove, colour, boxSize):
    startRow, startCol, endRow, endCol = lastMove

    rect = pygame.Rect(startRow*boxSize, startCol*boxSize, boxSize, boxSize)
    pygame.draw.rect(window, colour, rect)
    rect = pygame.Rect(endRow*boxSize, endCol*boxSize, boxSize, boxSize)
    pygame.draw.rect(window, colour, rect) 

def drawCheckmateIcon(window, boardHeight, boardWidth):
    transformedCheckmateIcon = pygame.transform.scale(checkmateIcon, (boardHeight//3, boardWidth//3)) 
    window.blit(transformedCheckmateIcon, ((boardHeight//3), boardWidth//3)) 

def drawPieceOnCursor(window, draggedPieceSprite, x, y):
    if draggedPieceSprite != "!":
        try:
            window.blit(draggedPieceSprite, (x-22.5, y-22.5)) # draw the dragged piece onto the mouse cursor 
        except:
            pass
