import copy

def adjacentPositions(position):
	adjacent = [
		[1, 3],
		[0, 2, 9],
		[1, 4],
		[0, 5, 11],
		[2, 7, 12],
		[3, 6],
		[5, 7, 14],
		[4, 6],
		[9, 11],
		[1, 8, 10, 17],
		[9, 12],
		[3, 8, 13, 19],
		[4, 10, 15, 20],
		[11, 14],
		[6, 13, 15, 22],
		[12, 14],
		[17, 19],
		[9, 16, 18],
		[17, 20],
		[11, 16, 21],
		[12, 18, 23],
		[19, 22],
		[21, 23, 14],
		[20, 22]
	]
	return adjacent[position]

def checkMill(position, board, player):
	mill = [
		(isMill(player, board, 1, 2) or isMill(player, board, 3, 5)),
		(isMill(player, board, 0, 2) or isMill(player, board, 9, 17)),
		(isMill(player, board, 0, 1) or isMill(player, board, 4, 7)),
		(isMill(player, board, 0, 5) or isMill(player, board, 11, 19)),
		(isMill(player, board, 2, 7) or isMill(player, board, 12, 20)),
		(isMill(player, board, 0, 3) or isMill(player, board, 6, 7)),
		(isMill(player, board, 5, 7) or isMill(player, board, 14, 22)),
		(isMill(player, board, 2, 4) or isMill(player, board, 5, 6)),
		(isMill(player, board, 9, 10) or isMill(player, board, 11, 13)),
		(isMill(player, board, 8, 10) or isMill(player, board, 1, 17)),
		(isMill(player, board, 8, 9) or isMill(player, board, 12, 15)),
		(isMill(player, board, 3, 19) or isMill(player, board, 8, 13)),
		(isMill(player, board, 20, 4) or isMill(player, board, 10, 15)),
		(isMill(player, board, 8, 11) or isMill(player, board, 14, 15)),
		(isMill(player, board, 13, 15) or isMill(player, board, 6, 22)),
		(isMill(player, board, 13, 14) or isMill(player, board, 10, 12)),
		(isMill(player, board, 17, 18) or isMill(player, board, 19, 21)),
		(isMill(player, board, 1, 9) or isMill(player, board, 16, 18)),
		(isMill(player, board, 16, 17) or isMill(player, board, 20, 23)),
		(isMill(player, board, 16, 21) or isMill(player, board, 3, 11)),
		(isMill(player, board, 12, 4) or isMill(player, board, 18, 23)),
		(isMill(player, board, 16, 19) or isMill(player, board, 22, 23)),
		(isMill(player, board, 6, 14) or isMill(player, board, 21, 23)),
		(isMill(player, board, 18, 20) or isMill(player, board, 21, 22)),
	]

	return mill[position]

def isMill(player, board, pos1, pos2):
	if (board[pos1] == player and board[pos2] == player):
		return True
	return False

def isCloseMill(position, board):
	player = board[position]

	if (player != "X"):
		return checkMill(position, board, player)
	
	return False

def allPiecesInMill(board, player):
	for i in range(24):
		if board[i] == player and not isCloseMill(i, board):
			return False
	return True


def placingPhaseNextMoves(board):
	board_list = []

	for i in range(len(board)):
		if (board[i] == "X"):
			board_clone = copy.deepcopy(board)
			board_clone[i] = "1"

			if (isCloseMill(i, board_clone)):
				board_list = removePiece(board_clone, board_list)
			else:
				board_list.append(board_clone)
	return board_list

def movingPhaseNextMoves(board):
	board_list = []
	for i in range(len(board)):
		if (board[i] == "1"):
			adjacent_list = adjacentPositions(i)

			for pos in adjacent_list:
				if (board[pos] == "X"):
					board_clone = copy.deepcopy(board)
					board_clone[i] = "X"
					board_clone[pos] = "1"

					if isCloseMill(pos, board_clone):
						board_list = removePiece(board_clone, board_list)
					else:
						board_list.append(board_clone)
	return board_list

def flyingPhaseNextMoves(board):
	board_list = []

	for i in range(len(board)):
		if (board[i] == "1"):

			for j in range(len(board)):
				if (board[j] == "X"):
					board_clone = copy.deepcopy(board)

					board_clone[i] = "X"
					board_clone[j] = "1"

					if (isCloseMill(j, board_clone)):
						board_list = removePiece(board_clone, board_list)
					else:
						board_list.append(board_clone)
	return board_list

def NextMoves(board):
	if (countPieces(board, "1") == 3):
		return flyingPhaseNextMoves(board)
	else:
		return movingPhaseNextMoves(board)

def removePiece(board_clone, board_list):
	for i in range(len(board_clone)):
		if (board_clone[i] == "2"):

			if not isCloseMill(i, board_clone):
				new_board = copy.deepcopy(board_clone)
				new_board[i] = "X"
				board_list.append(new_board)
	return board_list

def getPossibleMillCount(board, player):
	count = 0

	for i in range(len(board)):
		if (board[i] == "X"):
			if checkMill(i, board, player):
				count += 1
	return count

def twoMillsConfiguration(position, board, player):
	adjacent_list = adjacentPositions(position)

	for i in adjacent_list:
		if (board[i] == player) and (not checkMill(position, board, player)):
			return True
	return False

def opponentThreatMillSites(board, player):
	count = 0

	for i in range(len(board)):
		if (board[i] == player):
			adjacent_list = adjacentPositions(i)
			for pos in adjacent_list:
				if (player == "1"):
					if (board[pos] == "2"):
						board[i] = "2"
						if isCloseMill(i, board):
							count += 1
						board[i] = player
				else:
					if (board[pos] == "1" and twoMillsConfiguration(pos, board, "1")):
						count += 1
	return count

def countPieces(board, value):
    return board.count(value)

def has_no_legal_moves(board, player):
	for i in range(len(board)):
		if board[i] == player:
			for neighbor in adjacentPositions(i):
				if board[neighbor] == "X":
					return False 
	return True


