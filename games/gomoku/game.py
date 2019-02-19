import numpy as np
import logging
from utlis import winners_gomoku

class Game:

	def __init__(self):		
		self.currentPlayer = 1
		self.gameState = GameState(np.array([0 for x in range(15 * 15)], dtype=np.int), 1)
		self.actionSpace = np.array([0 for x in range(15 * 15)], dtype=np.int)
		self.pieces = {'1':'B', '0': '-', '-1':'W'}
		self.grid_shape = (15,15)
		self.input_shape = (2,15,15)
		self.name = 'gomoku'
		self.state_size = len(self.gameState.binary)
		self.action_size = len(self.actionSpace)

	def reset(self):
		self.gameState = GameState(np.array([0 for x in range(15 * 15)], dtype=np.int), 1)
		self.currentPlayer = 1
		return self.gameState

	def step(self, action):
		next_state, value, done = self.gameState.takeAction(action)
		self.gameState = next_state
		self.currentPlayer = -self.currentPlayer
		info = None
		return ((next_state, value, done, info))

	def identities(self, state, actionValues):
		identities = []

		currentBoard = state.board
		currentAV = actionValues
		for n in range(5):
			currentBoard = np.array([
						currentBoard[210], currentBoard[195], currentBoard[180], currentBoard[165], currentBoard[150], currentBoard[135], currentBoard[120], currentBoard[105], currentBoard[90], currentBoard[75], currentBoard[60], currentBoard[45], currentBoard[30], currentBoard[15], currentBoard[0],
						currentBoard[211], currentBoard[196], currentBoard[181], currentBoard[166], currentBoard[151], currentBoard[136], currentBoard[121], currentBoard[106], currentBoard[91], currentBoard[76], currentBoard[61], currentBoard[46], currentBoard[31], currentBoard[16], currentBoard[1],
						currentBoard[212], currentBoard[197], currentBoard[182], currentBoard[167], currentBoard[152], currentBoard[137], currentBoard[122], currentBoard[107], currentBoard[92], currentBoard[77], currentBoard[62], currentBoard[47], currentBoard[32], currentBoard[17], currentBoard[2],
						currentBoard[213], currentBoard[198], currentBoard[183], currentBoard[168], currentBoard[153], currentBoard[138], currentBoard[123], currentBoard[108], currentBoard[93], currentBoard[78], currentBoard[63], currentBoard[48], currentBoard[33], currentBoard[18], currentBoard[3],
						currentBoard[214], currentBoard[199], currentBoard[184], currentBoard[169], currentBoard[154], currentBoard[139], currentBoard[124], currentBoard[109], currentBoard[94], currentBoard[79], currentBoard[64], currentBoard[49], currentBoard[34], currentBoard[19], currentBoard[4],
						currentBoard[215], currentBoard[200], currentBoard[185], currentBoard[170], currentBoard[155], currentBoard[140], currentBoard[125], currentBoard[110], currentBoard[95], currentBoard[80], currentBoard[65], currentBoard[50], currentBoard[35], currentBoard[20], currentBoard[5],
						currentBoard[216], currentBoard[201], currentBoard[186], currentBoard[171], currentBoard[156], currentBoard[141], currentBoard[126], currentBoard[111], currentBoard[96], currentBoard[81], currentBoard[66], currentBoard[51], currentBoard[36], currentBoard[21], currentBoard[6],
						currentBoard[217], currentBoard[202], currentBoard[187], currentBoard[172], currentBoard[157], currentBoard[142], currentBoard[127], currentBoard[112], currentBoard[97], currentBoard[82], currentBoard[67], currentBoard[52], currentBoard[37], currentBoard[22], currentBoard[7],
						currentBoard[218], currentBoard[203], currentBoard[188], currentBoard[173], currentBoard[158], currentBoard[143], currentBoard[128], currentBoard[113], currentBoard[98], currentBoard[83], currentBoard[68], currentBoard[53], currentBoard[38], currentBoard[23], currentBoard[8],
						currentBoard[219], currentBoard[204], currentBoard[189], currentBoard[174], currentBoard[159], currentBoard[144], currentBoard[129], currentBoard[114], currentBoard[99], currentBoard[84], currentBoard[69], currentBoard[54], currentBoard[39], currentBoard[24], currentBoard[9],
						currentBoard[220], currentBoard[205], currentBoard[190], currentBoard[175], currentBoard[160], currentBoard[145], currentBoard[130], currentBoard[115], currentBoard[100], currentBoard[85], currentBoard[70], currentBoard[55], currentBoard[40], currentBoard[25], currentBoard[10],
						currentBoard[221], currentBoard[206], currentBoard[191], currentBoard[176], currentBoard[161], currentBoard[146], currentBoard[131], currentBoard[116], currentBoard[101], currentBoard[86], currentBoard[71], currentBoard[56], currentBoard[41], currentBoard[26], currentBoard[11],
						currentBoard[222], currentBoard[207], currentBoard[192], currentBoard[177], currentBoard[162], currentBoard[147], currentBoard[132], currentBoard[117], currentBoard[102], currentBoard[87], currentBoard[72], currentBoard[57], currentBoard[42], currentBoard[27], currentBoard[12],
						currentBoard[223], currentBoard[208], currentBoard[193], currentBoard[178], currentBoard[163], currentBoard[148], currentBoard[133], currentBoard[118], currentBoard[103], currentBoard[88], currentBoard[73], currentBoard[58], currentBoard[43], currentBoard[28], currentBoard[13],
						currentBoard[224], currentBoard[209], currentBoard[194], currentBoard[179], currentBoard[164], currentBoard[149], currentBoard[134], currentBoard[119], currentBoard[104], currentBoard[89], currentBoard[74], currentBoard[59], currentBoard[44], currentBoard[29], currentBoard[14],
					])

			currentAV = np.array([
						currentBoard[210], currentBoard[195], currentBoard[180], currentBoard[165], currentBoard[150], currentBoard[135], currentBoard[120], currentBoard[105], currentBoard[90], currentBoard[75], currentBoard[60], currentBoard[45], currentBoard[30], currentBoard[15], currentBoard[0],
						currentBoard[211], currentBoard[196], currentBoard[181], currentBoard[166], currentBoard[151], currentBoard[136], currentBoard[121], currentBoard[106], currentBoard[91], currentBoard[76], currentBoard[61], currentBoard[46], currentBoard[31], currentBoard[16], currentBoard[1],
						currentBoard[212], currentBoard[197], currentBoard[182], currentBoard[167], currentBoard[152], currentBoard[137], currentBoard[122], currentBoard[107], currentBoard[92], currentBoard[77], currentBoard[62], currentBoard[47], currentBoard[32], currentBoard[17], currentBoard[2],
						currentBoard[213], currentBoard[198], currentBoard[183], currentBoard[168], currentBoard[153], currentBoard[138], currentBoard[123], currentBoard[108], currentBoard[93], currentBoard[78], currentBoard[63], currentBoard[48], currentBoard[33], currentBoard[18], currentBoard[3],
						currentBoard[214], currentBoard[199], currentBoard[184], currentBoard[169], currentBoard[154], currentBoard[139], currentBoard[124], currentBoard[109], currentBoard[94], currentBoard[79], currentBoard[64], currentBoard[49], currentBoard[34], currentBoard[19], currentBoard[4],
						currentBoard[215], currentBoard[200], currentBoard[185], currentBoard[170], currentBoard[155], currentBoard[140], currentBoard[125], currentBoard[110], currentBoard[95], currentBoard[80], currentBoard[65], currentBoard[50], currentBoard[35], currentBoard[20], currentBoard[5],
						currentBoard[216], currentBoard[201], currentBoard[186], currentBoard[171], currentBoard[156], currentBoard[141], currentBoard[126], currentBoard[111], currentBoard[96], currentBoard[81], currentBoard[66], currentBoard[51], currentBoard[36], currentBoard[21], currentBoard[6],
						currentBoard[217], currentBoard[202], currentBoard[187], currentBoard[172], currentBoard[157], currentBoard[142], currentBoard[127], currentBoard[112], currentBoard[97], currentBoard[82], currentBoard[67], currentBoard[52], currentBoard[37], currentBoard[22], currentBoard[7],
						currentBoard[218], currentBoard[203], currentBoard[188], currentBoard[173], currentBoard[158], currentBoard[143], currentBoard[128], currentBoard[113], currentBoard[98], currentBoard[83], currentBoard[68], currentBoard[53], currentBoard[38], currentBoard[23], currentBoard[8],
						currentBoard[219], currentBoard[204], currentBoard[189], currentBoard[174], currentBoard[159], currentBoard[144], currentBoard[129], currentBoard[114], currentBoard[99], currentBoard[84], currentBoard[69], currentBoard[54], currentBoard[39], currentBoard[24], currentBoard[9],
						currentBoard[220], currentBoard[205], currentBoard[190], currentBoard[175], currentBoard[160], currentBoard[145], currentBoard[130], currentBoard[115], currentBoard[100], currentBoard[85], currentBoard[70], currentBoard[55], currentBoard[40], currentBoard[25], currentBoard[10],
						currentBoard[221], currentBoard[206], currentBoard[191], currentBoard[176], currentBoard[161], currentBoard[146], currentBoard[131], currentBoard[116], currentBoard[101], currentBoard[86], currentBoard[71], currentBoard[56], currentBoard[41], currentBoard[26], currentBoard[11],
						currentBoard[222], currentBoard[207], currentBoard[192], currentBoard[177], currentBoard[162], currentBoard[147], currentBoard[132], currentBoard[117], currentBoard[102], currentBoard[87], currentBoard[72], currentBoard[57], currentBoard[42], currentBoard[27], currentBoard[12],
						currentBoard[223], currentBoard[208], currentBoard[193], currentBoard[178], currentBoard[163], currentBoard[148], currentBoard[133], currentBoard[118], currentBoard[103], currentBoard[88], currentBoard[73], currentBoard[58], currentBoard[43], currentBoard[28], currentBoard[13],
						currentBoard[224], currentBoard[209], currentBoard[194], currentBoard[179], currentBoard[164], currentBoard[149], currentBoard[134], currentBoard[119], currentBoard[104], currentBoard[89], currentBoard[74], currentBoard[59], currentBoard[44], currentBoard[29], currentBoard[14],
					])			
			identities.append((GameState(currentBoard, state.playerTurn), currentAV))

		currentBoard = np.array([
						currentBoard[14], currentBoard[13], currentBoard[12], currentBoard[11], currentBoard[10], currentBoard[9], currentBoard[8], currentBoard[7], currentBoard[6], currentBoard[5], currentBoard[4], currentBoard[3], currentBoard[2], currentBoard[1], currentBoard[0],
						currentBoard[29], currentBoard[28], currentBoard[27], currentBoard[26], currentBoard[25], currentBoard[24], currentBoard[23], currentBoard[22], currentBoard[21], currentBoard[20], currentBoard[19], currentBoard[18], currentBoard[17], currentBoard[16], currentBoard[15],
						currentBoard[44], currentBoard[43], currentBoard[42], currentBoard[41], currentBoard[40], currentBoard[39], currentBoard[38], currentBoard[37], currentBoard[36], currentBoard[35], currentBoard[34], currentBoard[33], currentBoard[32], currentBoard[31], currentBoard[30],
						currentBoard[59], currentBoard[58], currentBoard[57], currentBoard[56], currentBoard[55], currentBoard[54], currentBoard[53], currentBoard[52], currentBoard[51], currentBoard[50], currentBoard[49], currentBoard[48], currentBoard[47], currentBoard[46], currentBoard[45],
						currentBoard[74], currentBoard[73], currentBoard[72], currentBoard[71], currentBoard[70], currentBoard[69], currentBoard[68], currentBoard[67], currentBoard[66], currentBoard[65], currentBoard[64], currentBoard[63], currentBoard[62], currentBoard[61], currentBoard[60],
						currentBoard[89], currentBoard[88], currentBoard[87], currentBoard[86], currentBoard[85], currentBoard[84], currentBoard[83], currentBoard[82], currentBoard[81], currentBoard[80], currentBoard[79], currentBoard[78], currentBoard[77], currentBoard[76], currentBoard[75],
						currentBoard[104], currentBoard[103], currentBoard[102], currentBoard[101], currentBoard[100], currentBoard[99], currentBoard[98], currentBoard[97], currentBoard[96], currentBoard[95], currentBoard[94], currentBoard[93], currentBoard[92], currentBoard[91], currentBoard[90],
						currentBoard[119], currentBoard[118], currentBoard[117], currentBoard[116], currentBoard[115], currentBoard[114], currentBoard[113], currentBoard[112], currentBoard[111], currentBoard[110], currentBoard[109], currentBoard[108], currentBoard[107], currentBoard[106], currentBoard[105],
						currentBoard[134], currentBoard[133], currentBoard[132], currentBoard[131], currentBoard[130], currentBoard[129], currentBoard[128], currentBoard[127], currentBoard[126], currentBoard[125], currentBoard[124], currentBoard[123], currentBoard[122], currentBoard[121], currentBoard[120],
						currentBoard[149], currentBoard[148], currentBoard[147], currentBoard[146], currentBoard[145], currentBoard[144], currentBoard[143], currentBoard[142], currentBoard[141], currentBoard[140], currentBoard[139], currentBoard[138], currentBoard[137], currentBoard[136], currentBoard[135],
						currentBoard[164], currentBoard[163], currentBoard[162], currentBoard[161], currentBoard[160], currentBoard[159], currentBoard[158], currentBoard[157], currentBoard[156], currentBoard[155], currentBoard[154], currentBoard[153], currentBoard[152], currentBoard[151], currentBoard[150],
						currentBoard[179], currentBoard[178], currentBoard[177], currentBoard[176], currentBoard[175], currentBoard[174], currentBoard[173], currentBoard[172], currentBoard[171], currentBoard[170], currentBoard[169], currentBoard[168], currentBoard[167], currentBoard[166], currentBoard[165],
						currentBoard[194], currentBoard[193], currentBoard[192], currentBoard[191], currentBoard[190], currentBoard[189], currentBoard[188], currentBoard[187], currentBoard[186], currentBoard[185], currentBoard[184], currentBoard[183], currentBoard[182], currentBoard[181], currentBoard[180],
						currentBoard[209], currentBoard[208], currentBoard[207], currentBoard[206], currentBoard[205], currentBoard[204], currentBoard[203], currentBoard[202], currentBoard[201], currentBoard[200], currentBoard[199], currentBoard[198], currentBoard[197], currentBoard[196], currentBoard[195],
						currentBoard[224], currentBoard[223], currentBoard[222], currentBoard[221], currentBoard[220], currentBoard[219], currentBoard[218], currentBoard[217], currentBoard[216], currentBoard[215], currentBoard[214], currentBoard[213], currentBoard[212], currentBoard[211], currentBoard[210],
					])

		currentAV = np.array([
						currentBoard[14], currentBoard[13], currentBoard[12], currentBoard[11], currentBoard[10], currentBoard[9], currentBoard[8], currentBoard[7], currentBoard[6], currentBoard[5], currentBoard[4], currentBoard[3], currentBoard[2], currentBoard[1], currentBoard[0],
						currentBoard[29], currentBoard[28], currentBoard[27], currentBoard[26], currentBoard[25], currentBoard[24], currentBoard[23], currentBoard[22], currentBoard[21], currentBoard[20], currentBoard[19], currentBoard[18], currentBoard[17], currentBoard[16], currentBoard[15],
						currentBoard[44], currentBoard[43], currentBoard[42], currentBoard[41], currentBoard[40], currentBoard[39], currentBoard[38], currentBoard[37], currentBoard[36], currentBoard[35], currentBoard[34], currentBoard[33], currentBoard[32], currentBoard[31], currentBoard[30],
						currentBoard[59], currentBoard[58], currentBoard[57], currentBoard[56], currentBoard[55], currentBoard[54], currentBoard[53], currentBoard[52], currentBoard[51], currentBoard[50], currentBoard[49], currentBoard[48], currentBoard[47], currentBoard[46], currentBoard[45],
						currentBoard[74], currentBoard[73], currentBoard[72], currentBoard[71], currentBoard[70], currentBoard[69], currentBoard[68], currentBoard[67], currentBoard[66], currentBoard[65], currentBoard[64], currentBoard[63], currentBoard[62], currentBoard[61], currentBoard[60],
						currentBoard[89], currentBoard[88], currentBoard[87], currentBoard[86], currentBoard[85], currentBoard[84], currentBoard[83], currentBoard[82], currentBoard[81], currentBoard[80], currentBoard[79], currentBoard[78], currentBoard[77], currentBoard[76], currentBoard[75],
						currentBoard[104], currentBoard[103], currentBoard[102], currentBoard[101], currentBoard[100], currentBoard[99], currentBoard[98], currentBoard[97], currentBoard[96], currentBoard[95], currentBoard[94], currentBoard[93], currentBoard[92], currentBoard[91], currentBoard[90],
						currentBoard[119], currentBoard[118], currentBoard[117], currentBoard[116], currentBoard[115], currentBoard[114], currentBoard[113], currentBoard[112], currentBoard[111], currentBoard[110], currentBoard[109], currentBoard[108], currentBoard[107], currentBoard[106], currentBoard[105],
						currentBoard[134], currentBoard[133], currentBoard[132], currentBoard[131], currentBoard[130], currentBoard[129], currentBoard[128], currentBoard[127], currentBoard[126], currentBoard[125], currentBoard[124], currentBoard[123], currentBoard[122], currentBoard[121], currentBoard[120],
						currentBoard[149], currentBoard[148], currentBoard[147], currentBoard[146], currentBoard[145], currentBoard[144], currentBoard[143], currentBoard[142], currentBoard[141], currentBoard[140], currentBoard[139], currentBoard[138], currentBoard[137], currentBoard[136], currentBoard[135],
						currentBoard[164], currentBoard[163], currentBoard[162], currentBoard[161], currentBoard[160], currentBoard[159], currentBoard[158], currentBoard[157], currentBoard[156], currentBoard[155], currentBoard[154], currentBoard[153], currentBoard[152], currentBoard[151], currentBoard[150],
						currentBoard[179], currentBoard[178], currentBoard[177], currentBoard[176], currentBoard[175], currentBoard[174], currentBoard[173], currentBoard[172], currentBoard[171], currentBoard[170], currentBoard[169], currentBoard[168], currentBoard[167], currentBoard[166], currentBoard[165],
						currentBoard[194], currentBoard[193], currentBoard[192], currentBoard[191], currentBoard[190], currentBoard[189], currentBoard[188], currentBoard[187], currentBoard[186], currentBoard[185], currentBoard[184], currentBoard[183], currentBoard[182], currentBoard[181], currentBoard[180],
						currentBoard[209], currentBoard[208], currentBoard[207], currentBoard[206], currentBoard[205], currentBoard[204], currentBoard[203], currentBoard[202], currentBoard[201], currentBoard[200], currentBoard[199], currentBoard[198], currentBoard[197], currentBoard[196], currentBoard[195],
						currentBoard[224], currentBoard[223], currentBoard[222], currentBoard[221], currentBoard[220], currentBoard[219], currentBoard[218], currentBoard[217], currentBoard[216], currentBoard[215], currentBoard[214], currentBoard[213], currentBoard[212], currentBoard[211], currentBoard[210],
					])

		for n in range(5):
			currentBoard = np.array([
						currentBoard[210], currentBoard[195], currentBoard[180], currentBoard[165], currentBoard[150], currentBoard[135], currentBoard[120], currentBoard[105], currentBoard[90], currentBoard[75], currentBoard[60], currentBoard[45], currentBoard[30], currentBoard[15], currentBoard[0],
						currentBoard[211], currentBoard[196], currentBoard[181], currentBoard[166], currentBoard[151], currentBoard[136], currentBoard[121], currentBoard[106], currentBoard[91], currentBoard[76], currentBoard[61], currentBoard[46], currentBoard[31], currentBoard[16], currentBoard[1],
						currentBoard[212], currentBoard[197], currentBoard[182], currentBoard[167], currentBoard[152], currentBoard[137], currentBoard[122], currentBoard[107], currentBoard[92], currentBoard[77], currentBoard[62], currentBoard[47], currentBoard[32], currentBoard[17], currentBoard[2],
						currentBoard[213], currentBoard[198], currentBoard[183], currentBoard[168], currentBoard[153], currentBoard[138], currentBoard[123], currentBoard[108], currentBoard[93], currentBoard[78], currentBoard[63], currentBoard[48], currentBoard[33], currentBoard[18], currentBoard[3],
						currentBoard[214], currentBoard[199], currentBoard[184], currentBoard[169], currentBoard[154], currentBoard[139], currentBoard[124], currentBoard[109], currentBoard[94], currentBoard[79], currentBoard[64], currentBoard[49], currentBoard[34], currentBoard[19], currentBoard[4],
						currentBoard[215], currentBoard[200], currentBoard[185], currentBoard[170], currentBoard[155], currentBoard[140], currentBoard[125], currentBoard[110], currentBoard[95], currentBoard[80], currentBoard[65], currentBoard[50], currentBoard[35], currentBoard[20], currentBoard[5],
						currentBoard[216], currentBoard[201], currentBoard[186], currentBoard[171], currentBoard[156], currentBoard[141], currentBoard[126], currentBoard[111], currentBoard[96], currentBoard[81], currentBoard[66], currentBoard[51], currentBoard[36], currentBoard[21], currentBoard[6],
						currentBoard[217], currentBoard[202], currentBoard[187], currentBoard[172], currentBoard[157], currentBoard[142], currentBoard[127], currentBoard[112], currentBoard[97], currentBoard[82], currentBoard[67], currentBoard[52], currentBoard[37], currentBoard[22], currentBoard[7],
						currentBoard[218], currentBoard[203], currentBoard[188], currentBoard[173], currentBoard[158], currentBoard[143], currentBoard[128], currentBoard[113], currentBoard[98], currentBoard[83], currentBoard[68], currentBoard[53], currentBoard[38], currentBoard[23], currentBoard[8],
						currentBoard[219], currentBoard[204], currentBoard[189], currentBoard[174], currentBoard[159], currentBoard[144], currentBoard[129], currentBoard[114], currentBoard[99], currentBoard[84], currentBoard[69], currentBoard[54], currentBoard[39], currentBoard[24], currentBoard[9],
						currentBoard[220], currentBoard[205], currentBoard[190], currentBoard[175], currentBoard[160], currentBoard[145], currentBoard[130], currentBoard[115], currentBoard[100], currentBoard[85], currentBoard[70], currentBoard[55], currentBoard[40], currentBoard[25], currentBoard[10],
						currentBoard[221], currentBoard[206], currentBoard[191], currentBoard[176], currentBoard[161], currentBoard[146], currentBoard[131], currentBoard[116], currentBoard[101], currentBoard[86], currentBoard[71], currentBoard[56], currentBoard[41], currentBoard[26], currentBoard[11],
						currentBoard[222], currentBoard[207], currentBoard[192], currentBoard[177], currentBoard[162], currentBoard[147], currentBoard[132], currentBoard[117], currentBoard[102], currentBoard[87], currentBoard[72], currentBoard[57], currentBoard[42], currentBoard[27], currentBoard[12],
						currentBoard[223], currentBoard[208], currentBoard[193], currentBoard[178], currentBoard[163], currentBoard[148], currentBoard[133], currentBoard[118], currentBoard[103], currentBoard[88], currentBoard[73], currentBoard[58], currentBoard[43], currentBoard[28], currentBoard[13],
						currentBoard[224], currentBoard[209], currentBoard[194], currentBoard[179], currentBoard[164], currentBoard[149], currentBoard[134], currentBoard[119], currentBoard[104], currentBoard[89], currentBoard[74], currentBoard[59], currentBoard[44], currentBoard[29], currentBoard[14],
					])

			currentAV = np.array([
						currentBoard[210], currentBoard[195], currentBoard[180], currentBoard[165], currentBoard[150], currentBoard[135], currentBoard[120], currentBoard[105], currentBoard[90], currentBoard[75], currentBoard[60], currentBoard[45], currentBoard[30], currentBoard[15], currentBoard[0],
						currentBoard[211], currentBoard[196], currentBoard[181], currentBoard[166], currentBoard[151], currentBoard[136], currentBoard[121], currentBoard[106], currentBoard[91], currentBoard[76], currentBoard[61], currentBoard[46], currentBoard[31], currentBoard[16], currentBoard[1],
						currentBoard[212], currentBoard[197], currentBoard[182], currentBoard[167], currentBoard[152], currentBoard[137], currentBoard[122], currentBoard[107], currentBoard[92], currentBoard[77], currentBoard[62], currentBoard[47], currentBoard[32], currentBoard[17], currentBoard[2],
						currentBoard[213], currentBoard[198], currentBoard[183], currentBoard[168], currentBoard[153], currentBoard[138], currentBoard[123], currentBoard[108], currentBoard[93], currentBoard[78], currentBoard[63], currentBoard[48], currentBoard[33], currentBoard[18], currentBoard[3],
						currentBoard[214], currentBoard[199], currentBoard[184], currentBoard[169], currentBoard[154], currentBoard[139], currentBoard[124], currentBoard[109], currentBoard[94], currentBoard[79], currentBoard[64], currentBoard[49], currentBoard[34], currentBoard[19], currentBoard[4],
						currentBoard[215], currentBoard[200], currentBoard[185], currentBoard[170], currentBoard[155], currentBoard[140], currentBoard[125], currentBoard[110], currentBoard[95], currentBoard[80], currentBoard[65], currentBoard[50], currentBoard[35], currentBoard[20], currentBoard[5],
						currentBoard[216], currentBoard[201], currentBoard[186], currentBoard[171], currentBoard[156], currentBoard[141], currentBoard[126], currentBoard[111], currentBoard[96], currentBoard[81], currentBoard[66], currentBoard[51], currentBoard[36], currentBoard[21], currentBoard[6],
						currentBoard[217], currentBoard[202], currentBoard[187], currentBoard[172], currentBoard[157], currentBoard[142], currentBoard[127], currentBoard[112], currentBoard[97], currentBoard[82], currentBoard[67], currentBoard[52], currentBoard[37], currentBoard[22], currentBoard[7],
						currentBoard[218], currentBoard[203], currentBoard[188], currentBoard[173], currentBoard[158], currentBoard[143], currentBoard[128], currentBoard[113], currentBoard[98], currentBoard[83], currentBoard[68], currentBoard[53], currentBoard[38], currentBoard[23], currentBoard[8],
						currentBoard[219], currentBoard[204], currentBoard[189], currentBoard[174], currentBoard[159], currentBoard[144], currentBoard[129], currentBoard[114], currentBoard[99], currentBoard[84], currentBoard[69], currentBoard[54], currentBoard[39], currentBoard[24], currentBoard[9],
						currentBoard[220], currentBoard[205], currentBoard[190], currentBoard[175], currentBoard[160], currentBoard[145], currentBoard[130], currentBoard[115], currentBoard[100], currentBoard[85], currentBoard[70], currentBoard[55], currentBoard[40], currentBoard[25], currentBoard[10],
						currentBoard[221], currentBoard[206], currentBoard[191], currentBoard[176], currentBoard[161], currentBoard[146], currentBoard[131], currentBoard[116], currentBoard[101], currentBoard[86], currentBoard[71], currentBoard[56], currentBoard[41], currentBoard[26], currentBoard[11],
						currentBoard[222], currentBoard[207], currentBoard[192], currentBoard[177], currentBoard[162], currentBoard[147], currentBoard[132], currentBoard[117], currentBoard[102], currentBoard[87], currentBoard[72], currentBoard[57], currentBoard[42], currentBoard[27], currentBoard[12],
						currentBoard[223], currentBoard[208], currentBoard[193], currentBoard[178], currentBoard[163], currentBoard[148], currentBoard[133], currentBoard[118], currentBoard[103], currentBoard[88], currentBoard[73], currentBoard[58], currentBoard[43], currentBoard[28], currentBoard[13],
						currentBoard[224], currentBoard[209], currentBoard[194], currentBoard[179], currentBoard[164], currentBoard[149], currentBoard[134], currentBoard[119], currentBoard[104], currentBoard[89], currentBoard[74], currentBoard[59], currentBoard[44], currentBoard[29], currentBoard[14],
					])
			identities.append((GameState(currentBoard, state.playerTurn), currentAV))

		return identities




class GameState():
	def __init__(self, board, playerTurn):
		self.board = board
		self.pieces = {'1':'B', '0': '-', '-1':'W'}
		self.winners = winners_gomoku
		self.playerTurn = playerTurn
		self.binary = self._binary()
		self.id = self._convertStateToId()
		self.allowedActions = self._allowedActions()
		self.isEndGame = self._checkForEndGame()
		self.value = self._getValue()
		self.score = self._getScore()

	def _allowedActions(self):
		allowed = []
		for i in range(len(self.board)):
			if self.board[i]==0:
				allowed.append(i)
		return allowed

	def _binary(self):

		currentplayer_position = np.zeros(len(self.board), dtype=np.int)
		currentplayer_position[self.board==self.playerTurn] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-self.playerTurn] = 1

		position = np.append(currentplayer_position,other_position)

		return (position)

	def _convertStateToId(self):
		player1_position = np.zeros(len(self.board), dtype=np.int)
		player1_position[self.board==1] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-1] = 1

		position = np.append(player1_position,other_position)

		id = ''.join(map(str,position))

		return id

	def _checkForEndGame(self):
		if np.count_nonzero(self.board) == 255:
			return 1

		for x,y,z,a,b in self.winners:
			if (self.board[x] + self.board[y] + self.board[z] + self.board[a] + self.board[b] == 5 * -self.playerTurn):
				return 1
		return 0


	def _getValue(self):
		# This is the value of the state for the current player
		# i.e. if the previous player played a winning move, you lose
		for x,y,z,a,b in self.winners:
			if (self.board[x] + self.board[y] + self.board[z] + self.board[a] + self.board[b] == 5 * -self.playerTurn):
				return (-1, -1, 1)
		return (0, 0, 0)


	def _getScore(self):
		tmp = self.value
		return (tmp[1], tmp[2])




	def takeAction(self, action):
		newBoard = np.array(self.board)
		newBoard[action]=self.playerTurn
		
		newState = GameState(newBoard, -self.playerTurn)

		value = 0
		done = 0

		if newState.isEndGame:
			value = newState.value[0]
			done = 1

		return (newState, value, done) 




	def render(self, logger):
		for r in range(15):
			logger.info([self.pieces[str(x)] for x in self.board[15*r : (15*r + 15)]])
		logger.info('--------------')



