import pygame
import pygame as p
import ChessEngine
import SmartMoveFinder
pygame.display.set_caption('Chess')

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK",
              "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("C:/Users/Hanen/Downloads/Chess-main/Chess-main/Chess/Images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False  # a flag variable for when we should animate a move
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    # when a human is playing this will bw true, if an ai is playing then it will be false
    PlayerOne = False
    PlayerTwo = False
    while running:
        AgentTurn = (gs.whiteToMove and PlayerOne) or (not gs.whiteToMove and PlayerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and AgentTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(
                            playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            # KEY HANDLERS
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo last move id 'z' is pressed
                    gs.undoMove()
                    gameOver = False
                    # can do `validMoves = gs.validMoves()` but then if we change function name we will have to change the call at various places.
                    moveMade = True
                if e.key == p.K_r:  # reset the game if 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    # gameOver = False

        # AI Move finder
        if not gameOver and not AgentTurn:
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
            # If AI can't find any move -> if any move will lead to opponent giving a checkmate.
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # Highlighting the selected Square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            # transparency value -> 0 : 100% transparent | 255 : 100% Opaque
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

            # Highlighting the valid move squares
            s.fill(p.Color('yellow'))

            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(
                        s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def drawGameState(screen, gs, validMoves, sqSelected):
    # draw squares on board (should be called before drawing anything else)
    drawBoard(screen)
    drawPieces(screen, gs.board)  # draw pieces on the board
    highlightSquares(screen, gs, validMoves, sqSelected)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("thistle")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
# Highlight square selected and moves for a peice selected


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# animating a move


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # frames to move 1 square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount,
                move.startCol + dC * frame / frameCount)
        # if not whitesPerspective:
        drawBoard(screen)
        drawPieces(screen, board)
        # erase piece from endRow, endCol
        color = colors[(move.endRow + move.endCol) % 2]
        endSqaure = p.Rect(move.endCol * SQ_SIZE,
                           move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSqaure)
        # draw captured piece back
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSqaure)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(
            c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen,text):
    font = p.font.SysFont('comicsansms',32,True,False)
    textObject = font.render(text,True,p.Color('indigo'))
    shadowOffset = 4
    shadowObject = font.render(text,True,p.Color('Gray'))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH // 2 - textObject.get_width() // 2,HEIGHT // 2 - textObject.get_height() // 2)
    shadowLocation = textLocation.move(shadowOffset,shadowOffset)
    screen.blit(shadowObject,shadowLocation)
    screen.blit(textObject,textLocation)

if __name__ == '__main__':
    main()
