import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse 
import sys


def gameTypeOptions(valueStr):
	valueStr = valueStr.upper()
	gameTypeOptionsList = ['R', 'G', 'GG', 'C']
	if valueStr not in gameTypeOptionsList:
		raise argparse.ArgumentTypeError("{} is an invalid gameType.".format(valueStr))
	return valueStr

def intGreaterThanThree(valueStr):
	value = int(valueStr)
	if value <= 3:
		raise argparse.ArgumentTypeError("{} is an invalid integer greater than 3. : ".format(valueStr))
	return value

def positiveInt(valueStr):
	value = int(valueStr)
	if value <= 0:
		raise argparse.ArgumentTypeError("{} is an invalid positive integer. : ".format(valueStr))
	return value

def getGameType():
	while True:
		try:
			inputValue = input("Enter 'R' for a random game, 'G' for a Glider, 'GG' for Gosper Glider Gun, or 'C' for custom game. For a custom game you must set up 'customInput.csv' file in the 'data' directory. : ")
			gameType = gameTypeOptions(inputValue)
			break
		except Exception as err:
			print(err)

	return gameType

def getGridSize():
	while True:
		try:
			inputValue = int(input("Enter an integer greater than 3 to specify the grid size. : "))
			gridSize = intGreaterThanThree(inputValue)
			break
		except Exception as err:
			print(err)

	return gridSize

def getIterations():
	while True:
		try:
			inputValue = int(input("Enter an positive integer to specify the number of iterations. : "))
			iterations = positiveInt(inputValue)
			break
		except Exception as err:
			print(err)

	return iterations



def getInitialState(gameType, gridSize):
	## Get initial state of the game and save it to data/workingFile.csv

	#Check game type
	if gameType == "R":
		initialState = randomGame(gridSize)
	elif gameType == "G":
		initialState = initializeGlider(gridSize)
	elif gameType == "GG":
		initialState = initializeGosperGlider(gridSize)
	elif gameType == "C":
		initialState = initializeCustomGame(gridSize)

	return initialState

def randomGame(gridSize):
	##Return initial state for a random game

	arr = np.random.randint(2, size = (gridSize, gridSize))
	return arr

def getLocationToPlace(placeWhat, gridSize):
	##Get (row, column) location data from user to place gilder/gosper glider

	if(placeWhat == "G"):
		rowConstraint = gridSize-3
		columnConstraint = gridSize-3
		print("Where do you want to place your glider. Note both row and column values must be between 0 and " , rowConstraint, "inclusive.")
	elif(placeWhat == "GG"):
		rowConstraint = gridSize-9
		columnConstraint = gridSize-36
		print("Where do you want to place your gosper glider.")
		print("Note the row value must be between 0 and " , rowConstraint, "inclusive,")
		print("and the column value must be between 0 and " , columnConstraint, "inclusive.")


	while True:
		try: 
			row =  int(input("Enter the row where you want your glider to be placed: "))
			if not((row >= 0 ) and row <= rowConstraint):
				raise ValueError("Invalid value was entered for row.")
			break
		except ValueError as err:
			print(err)
	while True:
		try: 
			column =  int(input("Enter the column where you want your glider to be placed: "))
			if not((column >= 0 ) and column <= columnConstraint):
				raise ValueError("Invalid value was entered for row.")
			break
		except ValueError as err:
			print(err)

	return [row, column]

def initializeGlider(gridSize):
	##Return initial state with glider placed in postion (row, column)

	row, column = getLocationToPlace("G", gridSize)

	glider = np.zeros((gridSize, gridSize), dtype = bool)

	#Place glider at (row, column) 
	glider[row, column+1] = True
	glider[row+1, column+2] = True
	glider[row+2, column] = True
	glider[row+2, column+1] = True
	glider[row+2, column+2] = True

	return glider

def initializeGosperGlider(gridSize):
	##Return initial state with gosper glider placed in postion (row, column)

	row, column = getLocationToPlace("GG", gridSize)

	#Retrieve gosper glider from csv
	gosperGliderSchematic = np.loadtxt(open("data/gosperGliderGun.csv", 'rb'), delimiter = ",", dtype = bool) 
	
	gosperGlider = np.zeros((gridSize, gridSize), dtype = bool)

	#Place gsoper glider in gosperGlider array at location (row, column) 
	gosperGlider[row:row+9, column:column+36] = gosperGliderSchematic

	return gosperGlider

def initializeCustomGame(gridSize):
	##Return initial state for a random game

		#Open 'customInput.csv' if it exits and load data
		try:
			initialState = np.loadtxt(open("data/customInput.csv", 'rb'), delimiter = ",", dtype = bool)
		except FileNotFoundError as err:
			print(err)
			sys.exit()
		except Exception as err:
			print(err)
			sys.exit()

		#Check if 
		if initialState.shape[0] != initialState.shape[1]:
			print("Received data of dimension {}x{}. Expected square matrix data.".format(initialState.shape[0], initialState.shape[1]))
			sys.exit()
		return initialState



def getNextGen(currentState, gridSize):
	##Get next generation with constant 0 boundry condition 

	nextState = np.zeros((gridSize, gridSize), dtype = bool)

	for index, value in np.ndenumerate(currentState):
		liveNeighborsCount = currentState[max(0, index[0]-1):index[0]+2, max(0, index[1]-1):index[1]+2].sum() - currentState[index[0], index[1]]
		
		if(liveNeighborsCount < 2):
			nextState[index[0], index[1]] = False
		elif( (currentState[index[0], index[1]] == True) and ( (liveNeighborsCount == 2) or (liveNeighborsCount == 3) ) ):
			nextState[index[0], index[1]] = True
		elif( (currentState[index[0], index[1]] == True) and (liveNeighborsCount > 3) ):
			nextState[index[0], index[1]] = False
		elif( (currentState[index[0], index[1]] == False) and (liveNeighborsCount == 3) ):
			nextState[index[0], index[1]] = True

	return nextState




def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-gt','--gameType', type = gameTypeOptions, help = "Accepts 'R', 'G', 'GG', or 'C' to specify game type. 'R' for random game, 'G' for Glider game, 'GG' for Gosper Glider game, or 'C' for custom game. For a custom game you must set up 'customInput.csv' file in the 'data' directory.")
	parser.add_argument('-gs','--gridSize', type = intGreaterThanThree, help = "Integer greater than 3 to specify gird size.")
	parser.add_argument('-i','--iterations', type = positiveInt, help = "Positive intger to specify number of iterations.")
	parser.add_argument('-ts','--timeStep', type = float, default = 0.5, help = "Positive number of seconds to specify minimum time in between iterations. (Absolute value of the number will be used when a negative number is received.)")
	args = parser.parse_args()


	# Get game type if -gameType argument was not passed 
	if args.gameType == None:
		gameType = getGameType()
	else:
		gameType = args.gameType

	# Get grid size if -gridSize argument was not passed
	if args.gridSize == None:
		gridSize = getGridSize()
	else:
		gridSize = args.gridSize

	# Get number of iterations to perform if -iterations argument was not passed
	if args.iterations == None:
		iterations = getIterations()
	else:
		iterations = args.iterations


	#Set up matplotlib figure
	fig=plt.figure()
	ax1 = fig.add_subplot(111)

	currentState = getInitialState(gameType, gridSize)

	if gameType == 'C':
		gridSize = currentState.shape[0]

	for i in range(iterations+1):
		ax1.clear()
		ax1.imshow(currentState)
		#ax1.set_axis_off()
		plt.xlabel("Iteration: {}".format(i))
	
		currentState = getNextGen(currentState, gridSize)
		plt.pause(args.timeStep)
		i = i+1

	plt.show()

if __name__ == "__main__":
    main()



