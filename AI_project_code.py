import board
import random
import math

# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.
class Player:
	
	def __init__(self, name):
		self.name = name
		self.numExpanded = 0 # Use this to track the number of nodes you expand
		self.numPruned = 0 # Use this to track the number of times you prune 
		self.transpositionTable={}
	

	def getMove(self, gameBoard):
		bestScore=float('-inf')
		bestMove=None
		maxDepth=4
		for columnMove in range(gameBoard.numColumns):
			#condition to check if a space is available in the board
			if (gameBoard.colFills[columnMove]<gameBoard.numRows):
				gameBoard.addPiece(columnMove,self.name)
				score=self.minimax(gameBoard,maxDepth,False)
				gameBoard.removePiece(columnMove) #to come to the original state
				if(score is not None): 
					if(score>bestScore):
						bestScore=max(score,bestScore)
						bestMove=columnMove
		maxDepth=maxDepth+1
		if (bestMove is not None):
			return bestMove #returns the column where our move is to be placed
		return 0


	#The evaluation function assigns a utility score for a node in terminal state

	def evaluationFunction(self,gameBoard):
		if(gameBoard.checkWin()):
			if(gameBoard.lastPlay[2]==self.name):
				return 1;
			else:
				return -1;
		elif(gameBoard.checkFull()):
			return 0; 
		else:
			return self.addHeuristics(gameBoard)
	
	#the addHeuristics method improves the efficiency of the minimax algorithm making player X make more optimal moves
	def addHeuristics(self,gameBoard):
		totalScore=0
		if(gameBoard.checkWin()):
			if(gameBoard.lastPlay[2]==self.name):
				totalScore+=1000 #terminal state moves of both players
			else:
				totalScore-=1000
		else:
			#block the opponent from winning 
			opponent='O' if self.name=='X' else 'X'
			if(gameBoard.checkWin()):
				totalScore+=50
			
			#Starting from the center of the board leads to making most optimal decisions
			columnCenter=gameBoard.numColumns//2 # '//' denotes integer division
			for row in range(gameBoard.numRows):
				if(gameBoard.gameBoard[row][columnCenter]==self.name):
					totalScore+=100

			#Checking for every possible winning moves
			for column in range(gameBoard.numColumns):
				for row in range(gameBoard.numRows):
					if gameBoard.gameBoard[row][column]==self.name:
						
						#iterating horizontally through the board
						totalCountHorizontal=1
						for i in range(1,gameBoard.winNum):
							if((column+i)<gameBoard.numRows and gameBoard.gameBoard[row][column+i]==self.name):
								totalCountHorizontal+=1
							else:
								break
						if totalCountHorizontal==gameBoard.winNum:
							totalScore+=300

						#iterating vertically through the board
						totalCountVertical=1
						for i in range(1,gameBoard.winNum):
							if((row+i)<gameBoard.numRows and gameBoard.gameBoard[row+i][column]==self.name):
								totalCountVertical+=1
							else:
								break
						if (totalCountVertical==gameBoard.winNum):
							totalScore+=300

						#iterating diagonally (left to right) through the board
						totalCountDiagonal1=1
						for i in range(1,gameBoard.winNum):
							if((row+i)<gameBoard.numRows and (column+i)<gameBoard.numColumns and gameBoard.gameBoard[row+i][column+i]==self.name):
								totalCountDiagonal1+=1
							else:
								break
						if(totalCountDiagonal1==gameBoard.winNum):
							totalScore+=300

						#iterating diagonally (right to left) through the board
						totalCountDiagonal2=1
						for i in range(1,gameBoard.winNum):
							if((row+i)<gameBoard.numRows and (column-i)>=0 and gameBoard.gameBoard[row][column-i]==self.name):
								totalCountDiagonal2+=1
							else:
								break
						if(totalCountDiagonal2==gameBoard.winNum):
							totalScore+=300
		
		return totalScore	

	def minimax(self,gameBoard,depth,isMaximize):
		result=gameBoard.checkWin()
		if(result==True or depth==0): #the terminal condition
			self.numExpanded+=1
			return self.evaluationFunction(gameBoard)

		if(isMaximize):
			bestScore=float('-inf')
			for columnMove in range(gameBoard.numColumns):
				if(gameBoard.colFills[columnMove]<gameBoard.numRows):
					gameBoard.addPiece(columnMove,self.name)
					score=self.minimax(gameBoard,depth-1,False) #recursion is performed by the process of depth first search
					gameBoard.removePiece(columnMove)
					bestScore=max(bestScore,score)
			return bestScore
		else:
			bestScore=float('inf')
			for columnMove in range(gameBoard.numColumns):
				if(gameBoard.colFills[columnMove]<gameBoard.numRows):
					gameBoard.addPiece(columnMove,'O')
					score=self.minimax(gameBoard,depth-1,True) #recursion is performed
					gameBoard.removePiece(columnMove)
					bestScore=min(bestScore,score)
			return bestScore

	def getMoveAlphaBeta(self, gameBoard):
		bestScore=float('-inf')
		bestMove=None
		alpha=float('-inf')#lower bound for maximizing player
		beta=float('inf')#upper bound for minimizing player
		for columnMove in range(gameBoard.numColumns):
			if(gameBoard.colFills[columnMove]<gameBoard.numRows):
				gameBoard.addPiece(columnMove,self.name)
				score=self.minimaxAlphaBetaPruning(gameBoard,5,False,alpha,beta)
				gameBoard.removePiece(columnMove)
				if(score>bestScore):
					bestScore=score
					bestMove=columnMove
				alpha=max(alpha,bestScore)
	
		if bestMove is not None:
			return bestMove
		return 0

	def minimaxAlphaBetaPruning(self,gameBoard,depth,isMaximize,alpha,beta):
		result=gameBoard.checkWin()
		if(result == True or depth==0):
			return self.evaluationFunction(gameBoard)

		hashBoard=self.generateHash(gameBoard)
		transposition=self.extractTranspositionElements(hashBoard, depth)

		if transposition:
			return transposition['value']
		
		if isMaximize:
			bestScore=float('-inf')
			for columnMove in range(gameBoard.numColumns):
				if(gameBoard.colFills[columnMove]<gameBoard.numRows):
					gameBoard.addPiece(columnMove,self.name)
					self.numExpanded+=1
					score=self.minimaxAlphaBetaPruning(gameBoard,depth-1,False,alpha,beta)
					gameBoard.removePiece(columnMove)#piece is removed to preserve the board state
					bestScore=max(bestScore,score)
					alpha=max(alpha,bestScore)
					if(alpha>=beta):
						self.numPruned+=1
						break	
			self.transpositionStorage(hashBoard,bestScore,depth)
			 
		else:
			bestScore=float('inf')
			for columnMove in range(gameBoard.numColumns):
				if(gameBoard.colFills[columnMove]<gameBoard.numRows):
					gameBoard.addPiece(columnMove,'O')
					self.numExpanded+=1
					score=self.minimaxAlphaBetaPruning(gameBoard,depth-1,True,alpha,beta)
					gameBoard.removePiece(columnMove)
					bestScore=min(bestScore,score)
					beta=min(beta,bestScore)
					if(beta<=alpha):
						self.numPruned+=1
						break
			self.transpositionStorage(hashBoard,bestScore,depth)
		return bestScore

	def transpositionStorage(self,hashBoard,evaluationValue,depth):#the value will be the utility scores from terminal states
		self.transpositionTable[hashBoard]={'value':evaluationValue,'depth':depth}#A dictionary to store the hash of the current board state
	
	def extractTranspositionElements(self,key,depth):#extracts specific depth for current board state
		transpositionKeys=self.transpositionTable.get(key)
		if(transpositionKeys and transpositionKeys['depth']>=depth):
			return transpositionKeys
		return None
	
	def generateHash(self,gameBoard):
		return str(hash(tuple(tuple(row) for row in gameBoard.gameBoard)))




	