#import pygame, sys
import numpy as np 
import time
import math
#import pygame, sys
import networkx as nx
import matplotlib.pyplot as plt

lenList = 16
combinationsList = []
globalCombination = ""
livingCells = 0
cases = []

BLACK = (0,	0, 0)
WHITE = (255,255,255)

def showList(combinationsList):
	for x in range(0,len(combinationsList)):
		print(combinationsList[x])


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


def stringToMatriz(combination):
	column = []
	row = []
	STOP = int(math.sqrt(lenList))
	index = 0

	for x in range(0,len(combination)):
		for y in range(0,len(combination[x])):

			if(index < STOP):
				row.append(int(combination[x][y]))

				if( index == STOP -1):
					column.append(row.copy())
					row.clear()
					index = 0
				else:
					index += 1
								
		cases.append(column.copy())
		column.clear()
	return cases
	

def copyListOfLists(combinationsList):
	newCombinationsList = combinationsList.copy()
	
	for c in range(0, len(combinationsList)):
		newCombinationsList[c] = combinationsList[c].copy()	
	
	return newCombinationsList

def functionLife(lenList, combinationsList):

	newCombinationsList = copyListOfLists(combinationsList)

	for x in range(0,lenList ):
		for y in range(0,lenList ):

			livingCells = int(combinationsList[(x-1) % lenList][(y-1) % lenList]) + \
							  int(combinationsList[(x) % lenList][(y-1) % lenList]) + \
							  int(combinationsList[(x+1) % lenList][(y-1) % lenList]) + \
							  int(combinationsList[(x-1) % lenList][(y) % lenList]) + \
							  int(combinationsList[(x+1) % lenList][(y) % lenList]) + \
							  int(combinationsList[(x-1) % lenList][(y+1) % lenList]) + \
							  int(combinationsList[(x) % lenList][(y+1) % lenList]) + \
							  int(combinationsList[(x+1) % lenList][(y+1) % lenList])

			if((combinationsList[x][y] == 1) and (livingCells < 2 or livingCells > 3) ):
				newCombinationsList[x][y] = 0
				
			elif ((combinationsList[x][y]) == 0 and (livingCells == 3)):
				newCombinationsList[x][y] = 1

	#print("List return ")
	#showList(newCombinationsList)
	return newCombinationsList

def sumElementsList(list):
	total = 0
	for x in list:
		total = total + sum(x)

	return total 

def createGraph(graph):

	#Graph created
	G = nx.Graph()

	for x in graph:
		G.add_node(x)

	#for x in range(1, len(graph)):
	G.add_edge(0, 1)
	G.add_edge(0, 3)

	nx.draw_circular(G, node_size=80, width=0.1,font_size=5)
	plt.show()		

	'''Todo esto si va	

	#Node added
	G.add_node(1)
	G.add_node("Tom")
	G.add_node("Kevin")
	#Edge added
	G.add_edge("Kevin", "Chris")
	#Edges added
	G.add_edges_from([("Tom", "Chris"), ("Tom", "Kevin")])

	nx.draw_circular(G, node_size=80, width=0.1,font_size=5)
	plt.show()

'''
#def createCycledGraph(positionX, positionY):
	
#	pygame.draw.circle(screen, WHITE, (positionX, positionY), 30)	
#	pygame.draw.circle(screen, WHITE, (positionX + 20, positionY-20), 25,1)

#def createUnionGraph():
#	pass

	
getCombinations(lenList, globalCombination )

print("Generated combination ",len(combinationsList))

stringToMatriz(combinationsList)
'''
cases.clear()

validate = [

	[0,0,0,1],
	[0,0,0,0],
	[0,1,1,0],
	[0,0,0,0]
]
cases.append(validate)
'''
graph = [] 

G = nx.Graph()

for x in range(0,len(cases)):
	
	aux = 0
	
	#print("List evaluated ",x)
	
	#showList(cases[x])
	aux = sumElementsList(cases[x])
	variableFunctionLife = cases[x].copy()
	#print("livingCells", aux)

	#showList(variableFunctionLife)
	#print("")
	#print(G.edges)

	while(True):
		#print(G.nodes)
		if(aux in graph):
			#print(" equal ")
			G.add_edge(graph[len(graph) - 1], aux)
			#print(G.edges)
			break

		else:
			#print("sino")
			graph.append(aux)
			G.add_node(aux)
			if(len(graph) != 1):
				G.add_edge(graph[len(graph)-2],aux)

			variableFunctionLife = functionLife(len(variableFunctionLife),variableFunctionLife) 
			aux = sumElementsList(variableFunctionLife)

			#print("")
			#showList(variableFunctionLife)
			#print("Applied Life function to list" , x, "livingCells", aux)
			#print(G.edges)
			

nx.draw_circular(G, node_size=80, width=0.1,font_size=5)
plt.show()	



print("grafo ", graph)
print("-----------")


print(G.nodes)
print(G.edges)


#pygame.init()
#width, height = 500, 500
#screen = pygame.display.set_mode((height, width))
#screen.fill(BLACK)

#while  True:
#	for event in pygame.event.get():
#		if event.type == pygame.QUIT:
#			sys.exit()

#	screen.fill(BLACK)

#	createCycledGraph(100, 100)

#	pygame.draw.circle(screen, WHITE, (100, 100), 30)	
#	pygame.draw.circle(screen, WHITE, (120, 80), 25,1)
	
#	pygame.display.flip()
	


