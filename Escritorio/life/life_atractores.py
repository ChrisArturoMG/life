#import pygame, sys
import numpy as np 
import time


lenList = 2
combinationsList = []
globalCombination = ""
livingCells = 0

def getCombinations(lenList, combination):
	global combinationsList;
	newCombination = ""

	for x in range(0,2):
		if(lenList != 1):
			newCombination = combination + str(x)
			getCombinations(lenList-1, newCombination)
			newCombination = ""
		else:
			newCombination = combination + str(x)
			combinationsList.append(newCombination)
			newCombination = ""
	combination = ""

def functionLife():
	for x in range(0,lenList):
		for y in range(0,lenList):

			livingCells = combinationsList[(x-1) % lenList][(y-1) % lenList] + \
							  combinationsList[(x) % lenList][(y-1) % lenList] + \
							  combinationsList[(x+1) % lenList][(y-1) % lenList] + \
							  combinationsList[(x-1) % lenList][(y) % lenList] + \
							  combinationsList[(x+1) % lenList][(y) % lenList] + \
							  combinationsList[(x-1) % lenList][(y+1) % lenList] + \
							  combinationsList[(x) % lenList][(y+1) % lenList] + \
							  combinationsList[(x+1) % lenList][(y+1) % lenList]


			if((combinationsList[x,y] == 1) and (livingCells < 2 or livingCells > 3) ):
				combinationsList[x][y] = '0'
				
			elif ((combinationsList[x][y]) == 0 and (livingCells == 3)):
				combinationsList[x][y] = '1'


getCombinations(lenList, globalCombination)

print("Combinations ",len(combinationsList))
print(combinationsList)


