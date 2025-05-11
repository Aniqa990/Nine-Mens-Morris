from boardFunctions import *


pruned = 0
states_reached = 0

def InvertBoard(board):
    invertedboard = []
    for i in board:
        if i == "1":
            invertedboard.append("2")
        elif i == "2":
            invertedboard.append("1")
        else:
            invertedboard.append("X")
    return invertedboard

def opponentMoves(pos_list):
    result = []
    for i in pos_list:
        result.append(InvertBoard(i))
    return result

class evaluator():
 	
	def __init__(self):
		self.evaluator = 0
		self.board = []


def alphaBetaPruning(board, depth, player1, alpha, beta, isStage1, heuristic):
	finalEvaluation = evaluator()

	global states_reached
	states_reached += 1

	if depth != 0:
		currentEvaluation = evaluator()

		if player1:

			if isStage1:
				possible_configs = placingPhaseNextMoves(board)
			else:
				possible_configs = NextMoves(board)
		
		else:
			
			if isStage1:
				possible_configs = opponentMoves(placingPhaseNextMoves(InvertBoard(board)))
			else:
				possible_configs = opponentMoves(NextMoves(InvertBoard(board)))

		for move in possible_configs:

			if player1:

				currentEvaluation = alphaBetaPruning(move, depth - 1, False, alpha, beta, isStage1, heuristic)

				if currentEvaluation.evaluator > alpha:
					alpha = currentEvaluation.evaluator
					finalEvaluation.board = move
			else:

				currentEvaluation = alphaBetaPruning(move, depth - 1, True, alpha, beta, isStage1, heuristic)
				
				if currentEvaluation.evaluator < beta:
					beta = currentEvaluation.evaluator
					finalEvaluation.board = move

			if alpha >= beta:
				global pruned
				pruned += 1
				break

		if player1:
			finalEvaluation.evaluator = alpha
		else:
			finalEvaluation.evaluator = beta

	else:

		if player1:
			finalEvaluation.evaluator = heuristic(board, isStage1)
		else:
			finalEvaluation.evaluator = heuristic(InvertBoard(board), isStage1)

	return finalEvaluation

def minimax(board, depth, player1, alpha, beta, isStage1, heuristic):
	finalEvaluation = evaluator()

	global states_reached
	states_reached += 1

	if depth != 0:
		currentEvaluation = evaluator()

		if player1:

			if isStage1:
				possible_configs = placingPhaseNextMoves(board)
			else:
				possible_configs = NextMoves(board)
		
		else:
			
			if isStage1:
				possible_configs = opponentMoves(placingPhaseNextMoves(InvertBoard(board)))
			else:
				possible_configs = opponentMoves(NextMoves(InvertBoard(board)))

		for move in possible_configs:

			if player1:

				currentEvaluation = minimax(move, depth - 1, False, alpha, beta, isStage1, heuristic)

				if currentEvaluation.evaluator > alpha:
					alpha = currentEvaluation.evaluator
					finalEvaluation.board = move
			else:

				currentEvaluation = minimax(move, depth - 1, True, alpha, beta, isStage1, heuristic)
				
				if currentEvaluation.evaluator < beta:
					beta = currentEvaluation.evaluator
					finalEvaluation.board = move

		if player1:
			finalEvaluation.evaluator = alpha
		else:
			finalEvaluation.evaluator = beta

	else:

		if player1:
			finalEvaluation.evaluator = heuristic(board, isStage1)
		else:
			finalEvaluation.evaluator = heuristic(InvertBoard(board), isStage1)

	return finalEvaluation

def getPruned():
	global pruned
	x = pruned
	pruned = 0
	return x

def getStatesReached():
	global states_reached
	x = states_reached
	states_reached = 0
	return x