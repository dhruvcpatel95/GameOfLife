import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse 

def gameTypeOptions(valueStr):
	valueStr = valueStr.upper()
	gameTypeOptionsList = ['R', 'G', 'GG', 'C']
	if valueStr not in gameTypeOptionsList:
		raise argparse.ArgumentTypeError("{} is an invalid gameType.".format(valueStr))
	return valueStr

def intGreaterThanThree(valueStr):
	value = int(valueStr)
	if value <= 3:
		raise argparse.ArgumentTypeError("{} is an invalid integer greater than 3.".format(valueStr))
	return value

def getGameType():
	while True:
		try:
			inputValue = input("Enter a 'R' for a random game, 'G' for a glider, 'GG' for glider gun, or 'C' for custom game. : ")
			gameType = gameTypeOptions(inputValue)
			break
		except Exception as err:
			print(err)

	return gameType

def getGridSize():
	while True:
		try:
			inputValue = int(input("Enter an integer greater than 3 to specify the grid size."))
			gridSize = intGreaterThanThree(inputValue)
			break
		except Exception as err:
			print(err)

	return gridSize


parser = argparse.ArgumentParser()
parser.add_argument('-gt','--gameType', type = gameTypeOptions, help = "Enter a 'R' for a random game, 'G' for a glider, 'GG' for glider gun.")
parser.add_argument('-gs','--gridSize', type = intGreaterThanThree, help = "Enter an integer greater than 3 to specify the grid size.")
args = parser.parse_args()

# Get game type if -gt argument was not passed 
if args.gameType == None:
	gameType = getGameType()
else:
	gameType = args.gameType

# Get grid size if -gs argument was not passed
if args.gridSize == None:
	n = getGridSize()
	
else:
	n = args.gridSize



def getInitialState():
	# Get initial state of the game and save it to data/workingFile.csv

	#Check game type
	if gameType == "R":
		initialState = randomGame()
	elif gameType == "G":
		initialState = initializeGlider()
	elif gameType == "GG":
		initialState = initializeGosperGlider()
	elif gameType == "C":
		####NOTE### 
		#Add verification steps to make sure file exists.
		#Add verification steps to make sure file contains information in the expected format.
		initialState = np.loadtxt(open("data/customInput.csv", 'rb'), delimiter = ",", dtype = bool)

	np.savetxt("data/workingFile.csv", initialState, delimiter =",", fmt = '%d')


def randomGame():
	#Return initial state for a random game

	arr = np.random.randint(2, size = (n, n))
	return arr

def initializeGlider():
	#Return initial state with glider placed in postion (row, column)

	print("Where do you want to place your glider. Note the both row and column values must be between 0 and " , n-3, "inclusive.")
	while True:
		try: 
			row =  int(input("Enter the row where you want your glider to be placed: "))
			if not((row >= 0 ) and row <= n-3):
				raise ValueError("Invalid value was entered for row.")
			break
		except ValueError as err:
			print(err)
	while True:
		try: 
			column =  int(input("Enter the column where you want your glider to be placed: "))
			if not((column >= 0 ) and column <= n-3):
				raise ValueError("Invalid value was entered for row.")
			break
		except ValueError as err:
			print(err)

	glider = np.zeros((n, n), dtype = bool)

	#Place glider at (row, column) 
	glider[row, column+1] = True
	glider[row+1, column+2] = True
	glider[row+2, column] = True
	glider[row+2, column+1] = True
	glider[row+2, column+2] = True

	return glider

def initializeGosperGlider():
	#Return initial state with gosper glider placed in postion (row, column)

	print("Where do you want to place your glider.")
	print("Note the row value must be between 0 and " , n-9, "inclusive,")
	print("and the column value must be between 0 and " , n-36, "inclusive.")
	while True:
		try: 
			row =  int(input("Enter the row where you want your glider to be placed: "))
			if not((row >= 0 ) and row <= n-9):
				raise ValueError("Invalid value was entered for row.")
			break
		except ValueError as err:
			print(err)
	while True:
		try: 
			column =  int(input("Enter the column where you want your glider to be placed: "))
			if not((column >= 0 ) and column <= n-36):
				raise ValueError("Invalid value was entered for row.")
			break
		except ValueError as err:
			print(err)

	#Retrieve gosper glider from csv
	gosperGliderSchematic = np.loadtxt(open("data/gosperGliderGun.csv", 'rb'), delimiter = ",", dtype = bool) 
	
	gosperGlider = np.zeros((n, n), dtype = bool)

	#Place gsoper glider in gosperGlider array at location (row, column) 
	gosperGlider[row:row+9, column:column+36] = gosperGliderSchematic

	return gosperGlider


getInitialState()
currentState = np.loadtxt(open("data/workingFile.csv", 'rb'), delimiter = ",", dtype = bool)
plt.figure()
plt.imshow(currentState)
plt.show()






















