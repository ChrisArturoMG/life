import pygame, sys
import numpy as np
import time

import matplotlib.pyplot as plt
from matplotlib import pyplot 
from matplotlib.animation import FuncAnimation


import matplotlib.animation as animation
from random import randrange
from datetime import datetime


#IMPORTAMOS TODA LA LIBRERIA
from tkinter import filedialog
import tkinter

from OpenGL.GL import *
from OpenGL.GLU import *

import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

import pylab

import pygame
from pygame.locals import *

xe = [0]
ye = [0]
cadena = ""
ventan = tkinter.Tk()
v = tkinter.Entry(ventan)
supervivencia1 = tkinter.Entry(ventan)
nacimiento1 = tkinter.Entry(ventan)

supervivencia2 = tkinter.Entry(ventan)
nacimiento2 = tkinter.Entry(ventan)

estados = []
newestados = []
variable = 0
planox=0
planoy = 0

#CREAMOS LAS VENTANAS 

def abrirArchivo():
	global cadena
	archivo = filedialog.askopenfilename(title="Archivo", filetypes=[("Archivos de textos","*.txt")])
	f = open(archivo)
	cadena = f.read()


def funcion():
	global xe
	global ye
	global v
	global estados
	global newestados
	global variable
	global planox
	global planoy
	global nacimiento1
	global nacimiento2
	global supervivencia1
	global supervivencia2

	iteraciones = 0
	vivas = 0

	variable = (int)(v.get())

	min_nacimientos = (int)(nacimiento1.get())
	max_nacimientos = (int)(nacimiento2.get())

	min_supervivencia =(int)(supervivencia1.get())
	max_supervivencia =(int)(supervivencia2.get())

#	print(variable)
	ventan.destroy()

	##SE CREA LA PANTALLA
	pygame.init()
	width, height = 1000,1000
	 
	#SE CREA LA PANTALLA 
	screen = pygame.display.set_mode((height, width))

	#COLOR DE LA PANTALLA
	bg = 25, 25, 25
	 
	screen.fill(bg)

	nxC, nyC = variable, variable
	
	if variable >=1000:
		dimCH = 5
		dimCW = 5
	else:
		dimCW = (width / nxC) 
		dimCH = (height / nyC)

	#ESTADO DE LA CELDA VIVA O MUERTA

	gameState = np.zeros((nxC, nyC))

#	print("tamnio",len(cadena))
	
	aux = ""
	for x in range(0,len(cadena)-1):
		try: 
			entero = int(cadena[x])
			#print(entero)
			aux = aux + cadena[x]
		except ValueError:
			#print(int(aux), "termino de linea")
			if cadena[x] == '\n':
				gameState[posiX, int(aux)] = 1
				estados.append((posiX, int(aux))) 
			else: 
				posiX = int(aux)
			aux = ""

	#control de flujo la ejecucion

	pauseExect = True
	grafica = False


	#BUCLE DE EJECUCION
	while True: 

		#SALIR DE LA PANTALLA
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		newGameState = np.copy(gameState)	

		#PINTAR LA PANTALLA
		screen.fill(bg)

		#ZONA DE DIBUJO
		time.sleep(0.01)
		ev = pygame.event.get()

		for event in ev:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					pauseExect = not pauseExect
					iteraciones = iteraciones - 1

				if event.key == pygame.K_RIGHT:
					pauseExect = not pauseExect
					iteraciones = iteraciones - 1
					guardado = filedialog.asksaveasfile(mode='w', title="Guardar",confirmoverwrite=True, defaultextension=[('Archivos de textos','*.txt')], filetypes=[('Archivos de textos','*.txt')])  
					if guardado is None:
						print("No se guardo")					
					for x in range(0, nxC):
						for y in range(0, nyC):
							if newGameState[x,y] == 1:
								texto = str(x) +" "+ str(y) + '\n'
								guardado.write(texto)					
					guardado.close()
	
				if event.key == pygame.K_UP:
					grafica = not grafica


			mouseClick = pygame.mouse.get_pressed()

			#DIBUJAR CELULAS
			if sum(mouseClick) > 0:
				posX, posY = pygame.mouse.get_pos()
				celX, celY = int(np.floor(posX/ dimCW)), int(np.floor(posY / dimCH))
				if(newGameState[celX, celY] != 1):
					estados.append((celX, celY))

				newGameState[celX, celY] = not mouseClick[2]


			if event.type == pygame.MOUSEBUTTONDOWN:
				posX, posY = pygame.mouse.get_pos()
				celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

				print(planox)
				print(planoy)

				if event.button == 4:
					posX, posY = pygame.mouse.get_pos()
					celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
			
					dimCW= dimCW + 1;
					dimCH = dimCH + 1;
					planox = planox - celX
					planoy = planoy - celY

					#variable = variable - 1
				elif event.button == 5 and dimCW > 1 and dimCH > 1:
					if (dimCH) * (variable) > width:
						
						dimCW= dimCW - 1;
						dimCH = dimCH - 1;

						planox = planox + celX
						planoy = planoy + celY
		vivas = 0
		a=0 
		b=0

		newestados = estados.copy()
		

		for x in range(0, len(estados)):
			a,b = estados[x]
			if newGameState[a,b] == 1:
				vivas = vivas + 1
			if not pauseExect:
				n_height =  gameState[(a-1) % nxC, (b-1) % nyC] + \
								gameState[(a) % nxC, (b-1) % nyC] + \
								gameState[(a+1) % nxC, (b-1) % nyC] + \
								gameState[(a-1) % nxC, (b) % 	nyC] + \
								gameState[(a+1) % nxC, (b) % 	nyC] + \
								gameState[(a-1) % nxC, (b+1) % nyC] + \
								gameState[(a) % nxC, (b+1) % nyC] + \
								gameState[(a+1) % nxC, (b+1) % nyC] 



					#regla 2
				if gameState[a,b] == 1 and (n_height < min_supervivencia or n_height > max_supervivencia):
					newGameState[a,b] = 0
					newestados.remove(estados[x])	
				
				#regla 1 

				if gameState[(a-1) % nxC,(b-1) % nyC] == 0:
					ceroX = (a-1) % nxC
					ceroY = (b-1) % nyC
					ceros =  gameState[(ceroX-1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY+1) % nyC] 
					
					if ceros >= min_nacimientos and ceros <= max_nacimientos:
						newGameState[ceroX,ceroY] = 1
						newestados.append((ceroX,ceroY))	
						
						poly = 	[(   ((ceroX) *	 dimCW) + planox,   (ceroY * dimCH) + planoy),	
						(     ((ceroX+1) * dimCW) + planox,	  (ceroY * dimCH) + planoy),
						(     ((ceroX+1) * dimCW) + planox,	 ((ceroY+1) * dimCH) + planoy),
						(     ((ceroX) *   dimCW) + planox,  ((ceroY+1) * dimCH) + planoy)]

						pygame.draw.polygon(screen, (255,255,255), poly, 1)	

				if gameState[(a-1) % nxC ,(b+1) % nyC] == 0:
					ceroX = (a-1) % nxC
					ceroY = (b+1) % nyC
					ceros =  gameState[(ceroX-1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY+1) % nyC] 

					if ceros >= min_nacimientos and ceros <= max_nacimientos:
						newGameState[ceroX,ceroY] = 1
						newestados.append((ceroX,ceroY))	

						poly = 	[(   ((ceroX) *	 dimCW) + planox,   (ceroY * dimCH) + planoy),	
						(     ((ceroX+1) * dimCW) + planox,	  (ceroY * dimCH) + planoy),
						(     ((ceroX+1) * dimCW) + planox,	 ((ceroY+1) * dimCH) + planoy),
						(     ((ceroX) *   dimCW) + planox,  ((ceroY+1) * dimCH) + planoy)]

						pygame.draw.polygon(screen, (255,255,255), poly, 1)	

				if gameState[(a+1) % nxC,(b-1) % nyC] == 0:
					ceroX = (a+1) % nxC
					ceroY = (b-1) % nyC
					ceros =  gameState[(ceroX-1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY+1) % nyC] 

					if ceros >= min_nacimientos and ceros <= max_nacimientos:
						newGameState[ceroX,ceroY] = 1
						newestados.append((ceroX,ceroY))	

						poly = 	[(   ((ceroX) *	 dimCW) + planox,   (ceroY * dimCH) + planoy),	
						(     ((ceroX+1) * dimCW) + planox,	  (ceroY * dimCH) + planoy),
						(     ((ceroX+1) * dimCW) + planox,	 ((ceroY+1) * dimCH) + planoy),
						(     ((ceroX) *   dimCW) + planox,  ((ceroY+1) * dimCH) + planoy)]

						pygame.draw.polygon(screen, (255,255,255), poly, 1)	

				if gameState[(a+1) % nxC,(b+1) % nyC] == 0:
					ceroX = (a+1) % nxC
					ceroY = (b+1) % nyC
					ceros =  gameState[(ceroX-1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY+1) % nyC] 

					if ceros >= min_nacimientos and ceros <= max_nacimientos:
						newGameState[ceroX,ceroY] = 1
						newestados.append((ceroX,ceroY))	

						poly = 	[(   ((ceroX) *	 dimCW) + planox,   (ceroY * dimCH) + planoy),	
						(     ((ceroX+1) * dimCW) + planox,	  (ceroY * dimCH) + planoy),
						(     ((ceroX+1) * dimCW) + planox,	 ((ceroY+1) * dimCH) + planoy),
						(     ((ceroX) *   dimCW) + planox,  ((ceroY+1) * dimCH) + planoy)]

						pygame.draw.polygon(screen, (255,255,255), poly, 1)	


				if gameState[(a) % nxC, (b-1) % nyC] == 0:
					ceroX = (a) % nxC
					ceroY = (b-1) % nyC
					ceros =  gameState[(ceroX-1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY+1) % nyC] 
					
					if ceros >= min_nacimientos and ceros <= max_nacimientos:
						newGameState[ceroX,ceroY] = 1
						newestados.append((ceroX,ceroY))	

						poly = 	[(   ((ceroX) *	 dimCW) + planox,   (ceroY * dimCH) + planoy),	
						(     ((ceroX+1) * dimCW) + planox,	  (ceroY * dimCH) + planoy),
						(     ((ceroX+1) * dimCW) + planox,	 ((ceroY+1) * dimCH) + planoy),
						(     ((ceroX) *   dimCW) + planox,  ((ceroY+1) * dimCH) + planoy)]

						pygame.draw.polygon(screen, (255,255,255), poly, 1)	

				if gameState[(a-1) % nxC, (b) % 	nyC] == 0:
					ceroX =(a-1) % nxC
					ceroY =(b) % nyC
					ceros =  gameState[(ceroX-1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY+1) % nyC] 

					if ceros >= min_nacimientos and ceros <= max_nacimientos:
						newGameState[ceroX,ceroY] = 1
						newestados.append((ceroX,ceroY))	

						poly = 	[(   ((ceroX) *	 dimCW) + planox,   (ceroY * dimCH) + planoy),	
						(     ((ceroX+1) * dimCW) + planox,	  (ceroY * dimCH) + planoy),
						(     ((ceroX+1) * dimCW) + planox,	 ((ceroY+1) * dimCH) + planoy),
						(     ((ceroX) *   dimCW) + planox,  ((ceroY+1) * dimCH) + planoy)]

						pygame.draw.polygon(screen, (255,255,255), poly, 1)	
					

				if gameState[(a+1) % nxC, (b) % 	nyC] == 0:
					ceroX = (a+1) % nxC
					ceroY = (b) % 	nyC
					ceros =  gameState[(ceroX-1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY+1) % nyC] 

					if ceros >= min_nacimientos and ceros <= max_nacimientos:
						newGameState[ceroX,ceroY] = 1
						newestados.append((ceroX,ceroY))	

						poly = 	[(   ((ceroX) *	 dimCW) + planox,   (ceroY * dimCH) + planoy),	
						(     ((ceroX+1) * dimCW) + planox,	  (ceroY * dimCH) + planoy),
						(     ((ceroX+1) * dimCW) + planox,	 ((ceroY+1) * dimCH) + planoy),
						(     ((ceroX) *   dimCW) + planox,  ((ceroY+1) * dimCH) + planoy)]
						
						pygame.draw.polygon(screen, (255,255,255), poly, 1)	

				if gameState[(a) % nxC, (b+1) % nyC] == 0:
					ceroX = (a) % nxC
					ceroY = (b+1) % nyC
					ceros =  gameState[(ceroX-1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY-1) % nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY) % 	nyC] + \
								gameState[(ceroX-1) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX) % nxC, (ceroY+1) % nyC] + \
								gameState[(ceroX+1) % nxC, (ceroY+1) % nyC] 

					if ceros >= min_nacimientos and ceros <= max_nacimientos:
						newGameState[ceroX,ceroY] = 1
						newestados.append((ceroX,ceroY))	
						
						poly = 	[(   ((ceroX) *	 dimCW) + planox,   (ceroY * dimCH) + planoy),	
						(     ((ceroX+1) * dimCW) + planox,	  (ceroY * dimCH) + planoy),
						(     ((ceroX+1) * dimCW) + planox,	 ((ceroY+1) * dimCH) + planoy),
						(     ((ceroX) *   dimCW) + planox,  ((ceroY+1) * dimCH) + planoy)]

						pygame.draw.polygon(screen, (255,255,255), poly, 1)
			
			 						#DIBUJAMOS EL CUADRAD
			poly = 	[ ( ((a) *dimCW) + planox,   (b * dimCH) + planoy),	
					( ((a+1) * dimCW) + planox,	  (b * dimCH) + planoy),
					( ((a+1) * dimCW) + planox,	  ((b+1) * dimCH) + planoy),
					( ((a) *   dimCW) + planox,  ((b+1) * dimCH) + planoy)]

			if newGameState[a,b] == 0: 
				pygame.draw.polygon(screen, (25,25,25), poly, 1)
			else:
			 	pygame.draw.polygon(screen, (255,255,255), poly, 1)	

		newestados = list(set(newestados))

		estados = newestados.copy()

		if pauseExect == False:
			ye.append(vivas)
			#print(ye)

		#GRAFICA
		if grafica == True:
			fig = pylab.figure(figsize=[4, 4],
		                   dpi=200,        
		                   )
			ax = fig.gca()
			ax.plot(ye)

			canvas = agg.FigureCanvasAgg(fig)
			canvas.draw()
			renderer = canvas.get_renderer()
			raw_data = renderer.tostring_rgb()

			pygame.init()

			size = canvas.get_width_height()

			surf = pygame.image.fromstring(raw_data, size, "RGB")
			screen.blit(surf, (0,0))

		gameState = np.copy(newGameState)

		#ACTUALIZAR PANTALLA 
		pygame.display.flip()	



def ventana():	
	global ventan,v
	global nacimiento1
	global nacimiento2
	global supervivencia1
	global supervivencia2

	ventan.geometry("400x350")
	variable = 0

	tamanio = tkinter.Label(ventan, text ="Tamaño universo")
	tamanio.grid(row=0, column=0, padx=20)

	v.grid(row=0, column=1, pady=10)

	##REGLA DE NACIMIENTO
	mas_nacido = tkinter.Label(ventan, text ="Reglas de nacimiento")
	mas_nacido.grid(row=1, column=0, padx=20)

	mas_nacido = tkinter.Label(ventan, text ="min")
	mas_nacido.grid(row=2, column=0, padx=20)
	
	nacimiento1.grid(row=2, column=1, pady=10)


	menos_nacido = tkinter.Label(ventan, text ="max")
	menos_nacido.grid(row=3, column=0, padx=20)
	
	nacimiento2.grid(row=3, column=1, pady=10)

	##REGLA DE SUPERVIVENCIA
	mas_super = tkinter.Label(ventan, text ="Reglas de supervivencia")
	mas_super.grid(row=4, column=0, padx=20)

	mas_super = tkinter.Label(ventan, text ="min")
	mas_super.grid(row=5, column=0, padx=20)
	
	supervivencia1.grid(row=5, column=1, pady=10)


	menos_super = tkinter.Label(ventan, text ="max")
	menos_super.grid(row=6, column=0, padx=20)
	
	supervivencia2.grid(row=6, column=1, pady=10)




	guardar = tkinter.Button(ventan, text="Abrir archivo", command=abrirArchivo)
	guardar.grid(row=7, column=0 , pady=10)

	b = tkinter.Button(ventan, text ="Iniciar", width=0, height=0, command=funcion)
	b.grid(row=8, column=0)

	ventan.mainloop()

def grafica():
	fig = pylab.figure(figsize=[4, 4], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
	ax = fig.gca()
	ax.plot([1, 2, 4])

	canvas = agg.FigureCanvasAgg(fig)
	canvas.draw()
	renderer = canvas.get_renderer()
	raw_data = renderer.tostring_rgb()


	pygame.init()

	window = pygame.display.set_mode((600, 400), DOUBLEBUF)
	screen = pygame.display.get_surface()

	size = canvas.get_width_height()

	surf = pygame.image.fromstring(raw_data, size, "RGB")
	screen.blit(surf, (0,0))
	pygame.display.flip()

	crashed = False
	while not crashed:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True



ventana()







