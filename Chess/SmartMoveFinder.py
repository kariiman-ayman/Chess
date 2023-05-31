import random
# A map of piece to score value -> Standard chess scores
# making King = 0, as no one can actually take the king
pieceScore = {'K': 0, "p": 1, "N": 3, "B": 3, "R": 5, "Q": 10}
CHECKMATE = 1000    # if you lead to checkmate you win -> hence max attainable score
# If you can win(capture opponent's piece) avoid it but if you loosing(opponent can give you Checkmate) try it hence 0 and not -1000
STALEMATE = 0
DEPTH = 2      # Depth for recursive calls

# Function to calculate RANDOM move from the list of valid moves.


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

'''
Helper method to call recursion for the 1st time 
'''
def findBestMove(gs, validMoves):
    global nextMove     # to find the next move
    nextMove = None
    random.shuffle(validMoves)
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveMinMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.getValidMoves else -1)
    return nextMove

'''
Find the best move based on material itself
'''
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:      # We have reached the bottom of the tree -> with fixed depth == DEPTH
        return boardScore(gs.board)   #return the score

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
BEST Move calculator using MinMax Algorithm along with  Alpha Beta Pruning
'''
def findMoveMinMaxAlphaBeta(gs, validMoves, depth, alpha, beta, whiteToMove):
    global nextMove
    if depth == 0:  # Base case: Reached the maximum depth
        return boardScore(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, False)

            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    if maxScore > alpha:
                        alpha = maxScore
                    if alpha >= beta:     # pruning happens
                        break

            gs.undoMove()

        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, True)

            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
                    if minScore < beta:
                        beta = minScore
                    if alpha >= beta:    # pruning happens
                        break

            gs.undoMove()

        return minScore

'''
    Gives the score of the board according to the material on it -> White piece positive material and Black piece negative material.
    Assuming that Computer is playing White and Agent is playing black
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
