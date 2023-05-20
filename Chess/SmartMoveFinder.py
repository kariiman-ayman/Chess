import random
# A map of piece to score value -> Standard chess scores
# making King = 0, as no one can actually take the king
pieceScore = {'K': 0, "p": 1, "N": 3, "B": 3, "R": 5, "Q": 10}
CHECKMATE = 1000    # if you lead to checkmate you win -> hence max attainable score
# If you can win(capture opponent's piece) avoid it but if you loosing(opponent can give you Checkmate) try it hence 0 and not -1000
STALEMATE = 0
DEPTH = 3        # Depth for recursive calls

# Function to calculate RANDOM move from the list of valid moves.


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


'''
    Function to find the BEST move , min max without recursion
'''


def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else - \
        1    # for allowing AI to play as any color
    # as AI is playing Black this is the worst possible score -> AI will start from worst and try to improve
    playerMaxScore = -CHECKMATE
    bestMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:   # not assigning colors so AI can play as both: playerMove -> move of the current player || opponentMove -> opponent's move
        gs.makeMove(playerMove)
        opponentMinScore = CHECKMATE
        opponentMoves = gs.getValidMoves()
        if gs.checkMate:
            gs.undoMove()
            return playerMove
        elif gs.staleMate:
            opponentMinScore = STALEMATE
        else:
            for opponentMove in opponentMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = -CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = turnMultiplier * boardScore(gs.board)
                if score < opponentMinScore:
                    opponentMinScore = score
                gs.checkMate = False
                gs.staleMate = False
                gs.undoMove()
        if playerMaxScore < opponentMinScore:
            playerMaxScore = opponentMinScore
            bestMove = playerMove
        gs.undoMove()
    return bestMove

'''
   Helper method to call recursion for the 1st time 
'''
def findBestMove(gs, validMoves):
    global nextMove     # to find the next move
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    #findMoveMinMax(gs, validMoves, DEPTH, -CHECKMATE, gs.whiteToMove)
    #findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH,-CHECKMATE, CHECKMATE, 1 if gs.getValidMoves else -1)
    return nextMove

'''
    Find the best move based on material itself
'''
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:      # We have reached the bottom of the tree -> with fixed depth == DEPTH
        return boardScore(gs)   #return the score

    if whiteToMove:  # Try to maximise score
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:   # Try to minimise score
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

'''
BEST Move calculator using NegaMax Algorithm
'''
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * boardScore(gs.board)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)   # negative for NEGA Max
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return score

'''
BEST Move calculator using NegaMax Algorithm along with  Alpha Beta Pruning
'''

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * boardScore(gs)

    # Move Ordering -> (TODO)
    # Traverse better moves 1st -> ones with checks and captures -> will lead to more pruning and more optimised algorithm
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)  # negative for NEGA Max
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  #purning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''
    Gives the score of the board according to the material on it -> White piece positive material and Black piece negative material.
    Assuming that Human is playing White and BOT is playing black
'''


def boardScore(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
