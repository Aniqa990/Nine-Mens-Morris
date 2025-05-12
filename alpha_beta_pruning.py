from boardFunctions import *


pruned = 0
nodes_explored = 0

def flipBoard(board):
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
        result.append(flipBoard(i))
    return result

class Evaluation():
 	
	def __init__(self):
		self.value = 0
		self.board = []


def alphaBetaPruning(board, depth, player1, alpha, beta, isStage1, heuristic):
	result = Evaluation()

	global nodes_explored
	nodes_explored += 1

	if depth != 0:
		tempEval = Evaluation()

		if player1:

			if isStage1:
				next_states = placingPhaseNextMoves(board)
			else:
				next_states = NextMoves(board)
		
		else:
			
			if isStage1:
				next_states = opponentMoves(placingPhaseNextMoves(flipBoard(board)))
			else:
				next_states = opponentMoves(NextMoves(flipBoard(board)))

		for state in next_states:

			if player1:

				tempEval = alphaBetaPruning(state, depth - 1, False, alpha, beta, isStage1, heuristic)

				if tempEval.value > alpha:
					alpha = tempEval.value
					result.board = state
			else:

				tempEval = alphaBetaPruning(state, depth - 1, True, alpha, beta, isStage1, heuristic)
				
				if tempEval.value < beta:
					beta = tempEval.value
					result.board = state

			if alpha >= beta:
				global pruned
				pruned += 1
				break

		if player1:
			result.value = alpha
		else:
			result.value = beta

	else:

		if player1:
			result.value = heuristic(board, isStage1)
		else:
			result.value = heuristic(flipBoard(board), isStage1)

	return result

def minimax(board, depth, player1, alpha, beta, isStage1, heuristic):
	result = Evaluation()

	global nodes_explored
	nodes_explored += 1

	if depth != 0:
		tempEval = Evaluation()

		if player1:

			if isStage1:
				next_states = placingPhaseNextMoves(board)
			else:
				next_states = NextMoves(board)
		
		else:
			
			if isStage1:
				next_states = opponentMoves(placingPhaseNextMoves(flipBoard(board)))
			else:
				next_states = opponentMoves(NextMoves(flipBoard(board)))

		for state in next_states:

			if player1:

				tempEval = minimax(state, depth - 1, False, alpha, beta, isStage1, heuristic)

				if tempEval.value > alpha:
					alpha = tempEval.value
					result.board = state
			else:

				tempEval = minimax(state, depth - 1, True, alpha, beta, isStage1, heuristic)
				
				if tempEval.value < beta:
					beta = tempEval.value
					result.board = state

		if player1:
			result.value = alpha
		else:
			result.value = beta

	else:

		if player1:
			result.value = heuristic(board, isStage1)
		else:
			result.value = heuristic(flipBoard(board), isStage1)

	return result

def reset_pruned_count():
	global pruned
	x = pruned
	pruned = 0
	return x

def reset_exploration_count():
	global nodes_explored
	x = nodes_explored
	nodes_explored = 0
	return x