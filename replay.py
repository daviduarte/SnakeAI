# Import the pygame module
import pygame
import time
import numpy as np
#from random import randrange
#from random import uniform
import random
import time
import copy
from sklearn.preprocessing import normalize
import os
import pickle
import math
import timeit
from print_nn import DrawNN



# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


#### Begin Function #####

"""
Given a position in pixel, discovery a new position multiple of PIXEL_DIM (worm dimensions)
"""
def roundPosition(pos):
	return int(pos/PIXEL_DIM)


def pixel2position(pix):
	return pix*PIXEL_DIM

def position2pixel(pos):
	return pos/PIXEL_DIM

"""
 Draw a square 
 @param size_x
 @param size_y
 @param x
 @param y
 """

def drawSquare(size_x, size_y, x, y, color):

	# Create a surface and pass in a tuple containing its length and width
	surf = pygame.Surface((size_x, size_y))
	# Give the surface a color to separate it from the background
	
	if color == 'red':
		surf.fill((255, 0, 0))
	elif color == 'black':
		surf.fill((0, 0, 0))

	rect = surf.get_rect()

	# This line says "Draw surf onto the screen at this cordinates"
	screen.blit(surf, (x, y))
	pygame.display.flip()



def drawWorm(i):

	global worm_set


	for j in range(len(worm_set[i])-1):
		drawSquare(50, 50, worm_set[i][j][0]*50, worm_set[i][j][1]*50, 'black')




def drawFood():

	global food
	drawSquare(50, 50, food[0]*50, food[1]*50, 'red')

def drawScore(i):
	myfont = pygame.font.SysFont('Comic Sans MS', 30)
	textsurface = myfont.render('Score: ' + str(score_set[i]), False, (0, 0, 0))
	screen.blit(textsurface,(10,10))
	pygame.display.flip()


def drawDottedLine(point1, point2):

	#pass
	pygame.draw.line(screen, (255,0,255), (point1[0]+ PIXEL_DIM/2, point1[1] + PIXEL_DIM/2), (point2[0]+ PIXEL_DIM/2, point2[1]+ PIXEL_DIM/2))
	pygame.display.flip()





def hitWall(i):

	if (worm_set[i][0][0] < 0 or
		worm_set[i][0][0] >= roundPosition(SCREEN_WIDTH) or
		worm_set[i][0][1] < 0 or
		worm_set[i][0][1] >= roundPosition(SCREEN_HEIGHT) ):

		return 1
	else:
		return 0


""" 
Loop over all points of worm's body and change it position
 @Param movement The movement of head	
 @return true if the worm eats the food
 @return false if the worm not eat the food
"""
def movementWormBody(movement, i):

	# Define the first point position	
	if (movement == 'left'):
		newPointX = worm_set[i][0][0] - 1
		newPointY = worm_set[i][0][1]

	elif (movement == 'up'):
		newPointX = worm_set[i][0][0]
		newPointY = worm_set[i][0][1] - 1

	elif (movement == 'right'):
		newPointX = worm_set[i][0][0] + 1
		newPointY = worm_set[i][0][1]			

	elif (movement == 'down'):
		newPointX = worm_set[i][0][0]
		newPointY = worm_set[i][0][1] + 1

	
	if(newPointX == food[0] and newPointY == food[1]):
		#worm_set[i].splice(0, 0, [food[0], food[1]])
		worm_set[i].insert(0, [food[0], food[1]])
		return 1
	

	formerPoint = [worm_set[i][0][0], worm_set[i][0][1]]
	worm_set[i][0][0] = newPointX
	worm_set[i][0][1] = newPointY			
	

	# In worm body, change the second point position to first point position, the third point position to second point position, and so on
	for j in range(1, len(worm_set[i])-1): # For each worm's body segment, excluding the status sting, in the last position of array
	#for (var j = 1; j<worm_set[i].length ; j++):
		aux = [worm_set[i][j][0], worm_set[i][j][1]]
		worm_set[i][j][0] = formerPoint[0]
		worm_set[i][j][1] = formerPoint[1]

		formerPoint = aux
	
	

"""
	Start new worms with random brains
"""
def newGame():
	global worm_set
	global score_set
	global last_position
	global individuals
	global current_individual
	global initial_food_position
	global initial_snake_position
	global food

	worm_set = []
	score_set = []
	initial_snake_position = []
	initial_food_position = []
	for i in range(0, individuals):

	#for(var i = 0 ; i < individuals ; i++):

		# Set initial worm value			
		#initial_point = getRandomVector()
		initial_point = getRandomVector()

		worm = []
		worm.append([copy.deepcopy(initial_point[0]), copy.deepcopy(initial_point[1])])
		initial_snake_position.append([copy.deepcopy(initial_point[0]), copy.deepcopy(initial_point[1])])

		worm.append("alive")
		worm_set.append(copy.deepcopy(worm))

		#newFoodPosition(i)	# newFoodPosition alters the global 'food'
		initial_food_position.append(time.time())

		last_position.append("qualquer_lado")

		# Set score to 0
		#score = -10
		zeroScore()


	current_individual = 0
	


def zeroScore():
	global score_set
	score_set = []
	for i in range(individuals):
		score_set.append(0)

def update(movement, i):

	global current_individual
	global wormLoop
	global food
	global current_snake_food

	if movement == 'right':
		if last_position[i] != 'left':
			movement = 'right'	
		else:
			movement = "left"
	
	if movement == 'up':
		if last_position[i] != 'down':
			movement = 'up'
		else:
			movement = "down"
		
	if movement == 'left':
		if(last_position[i] != 'right'):
			movement = 'left'
		else:
			movement = "right"

	if movement == 'down':
		if last_position[i] != 'up':
			movement = 'down'
		else:
			movement = "up"

	last_position[i] = movement
	
	

	# Moviment the worm
	eatTheFood = movementWormBody(movement, i)
	if(eatTheFood):
		newFoodPosition(current_individual)
		current_snake_food.append(copy.deepcopy(food))
		updateScore(i)
		wormLoop = 0

	
	if ( hitWall(i) == 1):
		worm_set[i][len(worm_set[i])-1] = 'dead'
		return 'dead'	

	# Verify if worm is dead by headitting on the only body
	if(stuckTheBody(i)):
		worm_set[i][len(worm_set[i])-1] = "dead"
		return 'dead'

	
# Get a random vector containing a valid position in screen
def getRandomVector():

	return [roundPosition(random.randrange(SCREEN_WIDTH)), 
            roundPosition(random.randrange(SCREEN_HEIGHT))]	

# TODO: Better way to get valid food position
def newFoodPosition(i):
		global food
		global worm_set
		global replay
		global foods
		global currentFood

		# Set initial food value
		flag = 1
		while (flag):
			initial_point = getRandomVector()

			# If the food is in the same place of some point of worm body, cast to the next superior int
			flag = 0
		#	for h in range(len(worm_set)):
			worm_ = worm_set[i]
			for j in range(len(worm_)):
				body = [worm_[j][0], worm_[j][1]]
				if initial_point[0] == body[0] and initial_point[1] == body[1]:
					flag = 1
					break

			if flag == 1:
				break

		if replay == 1:
			print("Loadando food")
			food = foods[currentFood]
			currentFood += 1
		else:
			food = copy.deepcopy(initial_point)
	
# Verify if the head exists in the same coordinates of some point of the body
# @return true if Worm hit your own body. His dead :/
# @return false if Worm NOT hit your own body. His alive :)

def stuckTheBody(i):
	head = [worm_set[i][0][0], worm_set[i][0][1]]

	# Start in the second position
	for j in range(1, len(worm_set[i])):
	#for (var j = 1 ; j < worm_set[i].length ; j++){
		body = [worm_set[i][j][0], worm_set[i][j][1]]
		if head[0] == body[0] and head[1] == body[1]:
			return True
		
	

	return False
	

# (i) Draw a white square in the last food and the segment of worm and
#def eraseLastWorm(i):



def updateScore(i):
	score_set[i] += 1000

def updateScoreAlive(i):
	score_set[i] += 1

def draw(i):
	# Fill the screen with white
	screen.fill((255, 255, 255, 128))

	#network.draw()
	drawFood()
	drawScore(i)

	drawWorm(i)



# Positive Diagonal line, buttom head
# Positive Diagonal line, buttom head
"""
      -----.-
	  ----.--  
	  ---*---
      -------
      -------
"""
def p1(head, point):
	# tng in infinity. Thus, verify if x coordinates is same
	m = -1
	suposto_y = m*point[0] - m*(head[0] + 2) + (head[1] - 2)

	if suposto_y == point[1] and point[1] < head[1] :

		oi = np.linalg.norm(np.asarray(head)-np.asarray(point))				

		if oi == 0:
			return 1

		return 1/oi

	else:
		return 0
	
""" 
	Perpendicular line above worm head
      -------
	  -------  
	  ---*---
      ---.---
      ---.---	
"""
def p2(head, point):
	# tng in infinity. Thus, just verify if x coordinates is same
	if head[0] == point[0] and point[1] > head[1]:
		oi = np.linalg.norm(np.asarray(head)-np.asarray(point))		
		
		if oi == 0:
			return 1		
		return 1/oi
	else:
		return 0
	
		
# Negative Diagonal line, buttom head
"""
      -------
	  -------  
	  ---*---
      ----.--
      -----.-
"""
def p3(head, point):
	# tng in infinity. Thus, verify if x coordinates is same
	m = 1

	suposto_y = m*point[0] - m*(head[0] - 2) + (head[1] - 2)	
	if suposto_y == point[1] and point[1] > head[1] :
		oi = np.linalg.norm(np.asarray(head)-np.asarray(point))
		
		if oi == 0:
			return 1
		return 1/oi
	else:
		return 0



""" 
	Perpendicular line in right site of worm head
      -------
	  -------  
	  ...*---
      -------
      -------	
"""
def p4(head, point):
	# tng in infinity. Thus, just verify if x coordinates is same
	if head[1] == point[1] and point[0] < head[0]:
		oi = np.linalg.norm(np.asarray(head)-np.asarray(point))		
		
		if oi == 0:
			return 1
		return 1/oi
	else:
		return 0


# Positive Diagonal line, buttom head
"""
      -------
	  -------  
	  ---*---
      --.----
      -.-----
"""
def p5(head, point):
	# tng in infinity. Thus, verify if x coordinates is same
	m = -1
	suposto_y = m*point[0] - m*(head[0] + 2) + (head[1] - 2)	

	if suposto_y == point[1] and point[1] > head[1] :
		oi = np.linalg.norm(np.asarray(head)-np.asarray(point))
		
		if oi == 0:
			return 1
		return 1/oi
	else:
		return 0


""" 
	Perpendicular line above head
      ---.---
	  ---.---  
	  ---*---
      -------
      -------	
"""
def p6(head, point):
	# tng in infinity. Thus, just verify if x coordinates is same
	if head[0] == point[0] and point[1] < head[1]:
		oi = np.linalg.norm(np.asarray(head)-np.asarray(point))		
		
		if oi == 0:
			return 1
		return 1/oi
	else:
		return 0

""" 
	Negative Perpendicular line above head
      .------
	  -.-----  
	  ---*---
      -------
      -------	
"""
def p7(head, point):
	# tng in infinity. Thus, verify if x coordinates is same
	m = 1
	suposto_y = m*point[0] - m*(head[0] - 2) + (head[1] - 2)	

	if suposto_y == point[1] and point[1] < head[1] :
		oi = np.linalg.norm(np.asarray(head)-np.asarray(point))

		if oi == 0:
			return 1
		return 1/oi
	else:
		return 0


""" 
	Perpendicular line in the left side head
      -------
	  -------  
	  ---*...
      -------
      -------	
"""
def p8(head, point):
	# tng in infinity. Thus, just verify if x coordinates is same
	if head[1] == point[1] and point[0] > head[0]:
		oi = np.linalg.norm(np.asarray(head)-np.asarray(point))				
		
		if oi == 0:
			return 1
		return 1/oi
	else:
		return 0


#
#	Diagonal line from head to up border OR right border
#
def border1(head):

	# First verif if the line hit top border
	m = -1 # 45 degrees
	head_pixel_0 = head[0]
	head_pixel_1 = head[1]
	game_area_width_ = SCREEN_WIDTH
	game_area_height_ = SCREEN_HEIGHT
	#console.log(cols)
	#console.log(rows)
	suposto_x = (0 + m*(head_pixel_0 + 2) - (head_pixel_1 - 2))/m

	ponto = []
	if suposto_x < game_area_width_:
		ponto = [suposto_x, 0]
	else:
		y = (m*game_area_width_) + (-m*(suposto_x)) + (0)
		ponto = [game_area_width_, y]
	
	print(head)
	drawDottedLine([head[0]*PIXEL_DIM , head[1]*PIXEL_DIM ], [ponto[0]*PIXEL_DIM, ponto[1]*PIXEL_DIM])

	#ctx.fillStyle = "blue";
	#ctx.fillRect((ponto[0]*pixel_worm_size)-10, ponto[1]*pixel_worm_size, 10, 10);

	oi = np.linalg.norm(np.asarray(head)-np.asarray(ponto))

	if oi == 0:
		return 1
	return 1/oi


#
#	Diagonal line from head to up border OR right border
#
def border3(head):

	# First verif if the line hit top border
	m = 1 # 45 degrees
	head_pixel_0 = head[0]
	head_pixel_1 = head[1]
	game_area_width_ = roundPosition(SCREEN_WIDTH)
	game_area_height_ = roundPosition(SCREEN_HEIGHT)
	#console.log(cols)
	#console.log(rows)
	suposto_x = (0 + m*(head_pixel_0 - 2) - (head_pixel_1 - 2))/m

	ponto = []
	if suposto_x > 0:
		ponto = [suposto_x, 0]	
	else:
		y = (m*0) + (-m*(suposto_x)) + (0)
		ponto = [0, y]
	
	#drawSquare(5,5, ponto[0]+10, ponto[1]+10)
	#ctx.fillStyle = "blue";
	#ctx.fillRect((ponto[0]*pixel_worm_size)-10, ponto[1]*pixel_worm_size, 10, 10);

	drawDottedLine([head[0]*PIXEL_DIM , head[1]*PIXEL_DIM ], [ponto[0]*PIXEL_DIM, ponto[1]*PIXEL_DIM])

	oi = np.linalg.norm(np.asarray(head)-np.asarray(ponto))
	if oi == 0:
		return 1	
	return 1/oi

	
def border5(head):

	# First verif if the line hit top border
	m = -1 # 45 degrees
	head_pixel_0 = head[0]
	head_pixel_1 = head[1]
	game_area_width_ = roundPosition(SCREEN_WIDTH)
	game_area_height_ = roundPosition(SCREEN_HEIGHT)
	suposto_x = (game_area_height_ + m*(head_pixel_0 - 2) - (head_pixel_1 + 2))/m
	
	ponto = []
	if(suposto_x > 0):
		ponto = [suposto_x, game_area_height_]
	else:
		y = (m*0) + (-m*(suposto_x)) + (game_area_height_)
		ponto = [0, y]
	
	drawDottedLine([head[0]*PIXEL_DIM , head[1]*PIXEL_DIM ], [ponto[0]*PIXEL_DIM, ponto[1]*PIXEL_DIM])

	#ctx.fillStyle = "blue";
	#ctx.fillRect(ponto[0]*pixel_worm_size, (ponto[1]*pixel_worm_size)-10, 10, 10);	
	#drawSquare(5,5, ponto[0]+10, ponto[1]-10)
	oi = np.linalg.norm(np.asarray(head)-np.asarray(ponto))
	if oi == 0:
		return 1
	return 1/oi


def border7(head):
	# First verif if the line hit top border

	m = 1 # 45 degrees
	head_pixel_0 = head[0]
	head_pixel_1 = head[1]
	game_area_width_ = roundPosition(SCREEN_WIDTH)
	game_area_height_ = roundPosition(SCREEN_HEIGHT)
	suposto_x = (game_area_height_ + m*(head_pixel_0 - 2) - (head_pixel_1 - 2))/m

	ponto = []
	if suposto_x < game_area_width_:	
		ponto = [suposto_x, game_area_height_]
	else:
		y = (m*game_area_width_) + (-m*(suposto_x)) + (game_area_height_)
		ponto = [game_area_width_, y]			
	
	#drawSquare(5,5, ponto[0]-10, ponto[1]-10)

	drawDottedLine([head[0]*PIXEL_DIM , head[1]*PIXEL_DIM ], [ponto[0]*PIXEL_DIM, ponto[1]*PIXEL_DIM])

	oi = np.linalg.norm(np.asarray(head)-np.asarray(ponto))

	if oi == 0:
		return 1
	return 1/oi
	

"""
* Vertical line, from head to up border
"""
def border2(head):
	ponto = [head[0], 0]		
	#ctx.fillStyle = "blue";
	oi = np.linalg.norm(np.asarray(head)-np.asarray(ponto))
	#drawSquare(5,5, ponto[0], ponto[1])
	#ctx.fillRect(ponto[0]*pixel_worm_size, ponto[1]*pixel_worm_size, 10, 10);	

	drawDottedLine([head[0]*PIXEL_DIM , head[1]*PIXEL_DIM ], [ponto[0]*PIXEL_DIM, ponto[1]*PIXEL_DIM])

	if oi == 0:
		return 1
	return 1/oi


"""
* Horizontal line, from head to left border
"""
def border4(head):
	ponto = [0, head[1]]
	#ctx.fillStyle = "blue";
	#console.log(ponto)
	oi = np.linalg.norm(np.asarray(head)-np.asarray(ponto))
	#drawSquare(5,5, ponto[0], ponto[1])
	#ctx.fillRect(ponto[0]*pixel_worm_size, ponto[1]*pixel_worm_size, 10, 10);		

	drawDottedLine([head[0]*PIXEL_DIM , head[1]*PIXEL_DIM ], [ponto[0]*PIXEL_DIM, ponto[1]*PIXEL_DIM])

	if oi == 0:
		return 1	
	return 1/oi


"""
* Vertical line, from head to down border
"""
def border6(head):
	game_area_height_ = roundPosition(SCREEN_HEIGHT)
	ponto = [head[0], game_area_height_]
	#ctx.fillStyle = "blue";
	#console.log(ponto)
	oi = np.linalg.norm(np.asarray(head)-np.asarray(ponto))
	#drawSquare(5,5, ponto[0]-10, ponto[1]-10)
	#ctx.fillRect(ponto[0]*pixel_worm_size, (ponto[1]*pixel_worm_size)-10, 10, 10);			
	#ctx.fillRect(ponto[0]*pixel_worm_size, ponto[1]*pixel_worm_size, 10, 10);	

	drawDottedLine([head[0]*PIXEL_DIM , head[1]*PIXEL_DIM ], [ponto[0]*PIXEL_DIM, ponto[1]*PIXEL_DIM])

	if oi == 0:
		return 1
	return 1/oi


"""
* Horizontal line, from head to right border
"""	
def border8(head):
	game_area_width_ = roundPosition(SCREEN_WIDTH)
	ponto = [game_area_width_, head[1]]
	#ctx.fillStyle = "blue";
	#console.log(ponto)
	oi = np.linalg.norm(np.asarray(head)-np.asarray(ponto))
	#drawSquare(5,5, ponto[0]-10, ponto[1]-10)

	#ctx.fillRect((ponto[0]*pixel_worm_size)-10, ponto[1]*pixel_worm_size, 10, 10);			
	#ctx.fillRect(ponto[0]*pixel_worm_size, ponto[1]*pixel_worm_size, 10, 10);		

	drawDottedLine([head[0]*PIXEL_DIM , head[1]*PIXEL_DIM ], [ponto[0]*PIXEL_DIM, ponto[1]*PIXEL_DIM])

	if oi == 0:
		return 1
	return 1/oi
	

"""
*	Diagonal line from head (up-right). Verify if hit worm body
"""
def border1_body(worm):


	# First verif if the line hit top border
	m = -1 # 45 degrees
	init_x = worm[0][0]
	init_y = worm[0][1]


	# The worm ywt has no body
	if (len(worm) == 1):
		return 0
	
	# Iterate over worm body and verify if belongs to line
	for i in range(len(worm)-1):
	#for (i = 1 ; i < worm.length ; i++){
		worm_x = worm[i][0]
		worm_y = worm[i][1]
		y = -m*(init_x + 2) + m*worm_x + (init_y - 2)

		if worm_y == y and worm_x > init_x and worm_y < init_y:
			oi = np.linalg.norm(np.asarray([init_x, init_y])-np.asarray([worm_x, worm_y]))

			if oi == 0:
				return 1
			return 1/oi
			#return dist([init_x, init_y], [worm_x, worm_y])
		
	
	return 0;

"""
*	Up head
"""
def border2_body(worm):


	# First verif if the line hit top border
	m = -1 # 45 degrees
	init_x = worm[0][0]
	init_y = worm[0][1]


	# The worm ywt has no body
	if (len(worm) == 1):
		return 0
	
	# Iterate over worm body and verify if belongs to line
	for i in range(len(worm)-1):
	#for (i = 1 ; i < worm.length ; i++){
		worm_x = worm[i][0]
		worm_y = worm[i][1]

		if worm_x == init_x and worm_y < init_y:
			oi = np.linalg.norm(np.asarray([init_x, init_y])-np.asarray([worm_x, worm_y]))

			if oi == 0:
				return 1
			return 1/oi
	
		
	
	return 0;	


""" 
      .------
	  -.-----  
	  ---*---
      -------
      -------	
"""
def border3_body(worm):


	# First verif if the line hit top border
	m = 1 # 45 degrees
	init_x = worm[0][0]
	init_y = worm[0][1]


	# The worm ywt has no body
	if (len(worm) == 1):
		return 0
	
	# Iterate over worm body and verify if belongs to line
	for i in range(len(worm)-1):
	#for (i = 1 ; i < worm.length ; i++){
		worm_x = worm[i][0]
		worm_y = worm[i][1]
		y = -m*(init_x - 2) + m*worm_x + (init_y - 2)

		if worm_y == y and worm_x < init_x and worm_y < init_y:
			oi = np.linalg.norm(np.asarray([init_x, init_y])-np.asarray([worm_x, worm_y]))

			if oi == 0:
				return 1
			return 1/oi
			#return dist([init_x, init_y], [worm_x, worm_y])
		
	
	return 0;


""" 
      -------
	  -------  
	  ...*---
      -------
      -------	
"""
def border4_body(worm):


	# First verif if the line hit top border
	m = -1 # 45 degrees
	init_x = worm[0][0]
	init_y = worm[0][1]


	# The worm ywt has no body
	if (len(worm) == 1):
		return 0
	
	# Iterate over worm body and verify if belongs to line
	for i in range(len(worm)-1):
	#for (i = 1 ; i < worm.length ; i++){
		worm_x = worm[i][0]
		worm_y = worm[i][1]

		if worm_y == init_y and worm_x < init_x:
			oi = np.linalg.norm(np.asarray([init_x, init_y])-np.asarray([worm_x, worm_y]))

			if oi == 0:
				return 1
			
			return 1/oi
	
		
	
	return 0;	

""" 
      -------
	  -------  
	  ---*---
      -.-----
      .------	
"""
def border5_body(worm):


	# First verif if the line hit top border
	m = -1 # 45 degrees
	init_x = worm[0][0]
	init_y = worm[0][1]


	# The worm ywt has no body
	if (len(worm) == 1):
		return 0
	
	# Iterate over worm body and verify if belongs to line
	for i in range(len(worm)-1):
	#for (i = 1 ; i < worm.length ; i++){
		worm_x = worm[i][0]
		worm_y = worm[i][1]
		y = -m*(init_x - 2) + m*worm_x + (init_y + 2)

		if worm_y == y and worm_x < init_x and worm_y > init_y:
			oi = np.linalg.norm(np.asarray([init_x, init_y])-np.asarray([worm_x, worm_y]))
			
			if oi == 0:
				return 1
			return 1/oi
			#return dist([init_x, init_y], [worm_x, worm_y])
		
	
	return 0;


""" 
      -------
	  -------  
	  ---*---
      ---.---
      ---.---	
"""
def border6_body(worm):


	# First verif if the line hit top border
	m = -1 # 45 degrees
	init_x = worm[0][0]
	init_y = worm[0][1]


	# The worm ywt has no body
	if (len(worm) == 1):
		return 0
	
	# Iterate over worm body and verify if belongs to line
	for i in range(len(worm)-1):
	#for (i = 1 ; i < worm.length ; i++){
		worm_x = worm[i][0]
		worm_y = worm[i][1]

		if worm_x == init_x and worm_y > init_y:
			oi = np.linalg.norm(np.asarray([init_x, init_y])-np.asarray([worm_x, worm_y]))
			
			if oi == 0:
				return 1
			return 1/oi
	
		
	
	return 0;		


""" 
      -------
	  -------  
	  ---*---
      -----.-
      ------.	
"""
def border7_body(worm):


	# First verif if the line hit top border
	m = 1 # 45 degrees
	init_x = worm[0][0]
	init_y = worm[0][1]


	# The worm ywt has no body
	if (len(worm) == 1):
		return 0
	
	# Iterate over worm body and verify if belongs to line
	for i in range(len(worm)-1):
	#for (i = 1 ; i < worm.length ; i++){
		worm_x = worm[i][0]
		worm_y = worm[i][1]
		y = -m*(init_x + 2) + m*worm_x + (init_y + 2)

		if worm_y == y and worm_x > init_x and worm_y > init_y:
			oi = np.linalg.norm(np.asarray([init_x, init_y])-np.asarray([worm_x, worm_y]))
			
			if oi == 0:
				return 1
			return 1/oi
			#return dist([init_x, init_y], [worm_x, worm_y])
		
	
	return 0;

""" 
      -------
	  -------  
	  ---*...
      -------
      -------	
"""
def border8_body(worm):


	# First verif if the line hit top border
	m = -1 # 45 degrees
	init_x = worm[0][0]
	init_y = worm[0][1]


	# The worm ywt has no body
	if (len(worm) == 1):
		return 0
	
	# Iterate over worm body and verify if belongs to line
	for i in range(len(worm)-1):
	#for (i = 1 ; i < worm.length ; i++){
		worm_x = worm[i][0]
		worm_y = worm[i][1]

		if worm_y == init_y and worm_x > init_x:
			oi = np.linalg.norm(np.asarray([init_x, init_y])-np.asarray([worm_x, worm_y]))

			if oi == 0:
				return 1
			return 1/oi
	
		
	
	return 0;		

def sigmoid(mat, bias):

	result = []	
	for i in range(len(mat)):
	#for(i ; i < mat.length ; i++){
		result.append(1 / (1 + math.exp(-mat[i] + bias)))
	
	return result	


def normalize_values(input):

	#norm1 = input / np.linalg.norm(input)
	norm1 = 2.*(input - np.min(input))/np.ptp(input)-1

		
	return norm1

"""
*	Receie a matrix, apply reLU in every element of this matrix
*	@return the matrix applied to reLU
"""
def relu(mat, bias):

	result = []	
	sum = 0
	for i in range(len(mat)):
	#for(i ; i < mat.length ; i++){
		result.append(np.amax([0, mat[i] + bias ] ))
	
	return result


def neural_network_inference(input, i):	


	#print(input)

	#input = normalize_values(input)
	#print(input)
	network.setInput(input)

	layer1 = np.matmul(input, brain_set[i][0])	
	layer1 = relu(layer1, brain_set[i][3])
	network.setLayer1(layer1)

	#print(layer1)

	layer2 = np.matmul(layer1, brain_set[i][1])
	layer2 = relu(layer2, brain_set[i][4])
	network.setLayer2(layer2)

	#print(layer2)

	output = np.matmul(layer2, brain_set[i][2])
	output = sigmoid(output, brain_set[i][5])
	network.setOutput(output)

	#print(output)

	#print(output)

	return output

# 3 layers, 1 input layer (24 neurons), 1 hidden layer (16 neurons) and 1 output lauer (4 neurons)
def initialize_neural_network(l1, l2, l3):


	# Init layer l1
	for i in range(INPUT_NEURON):
	#for (i = 0 ; i < input_neuron ; i++){
		l1.append([])
		for j in range(HIDDEN_NEURON1):
		#for (j = 0 ; j < hidden_neuron ; j++){
			l1[i].append(random.uniform(-1,1))
		
	
	# Init layer l2
	for i in range(HIDDEN_NEURON1):
	#for (i = 0 ; i < hidden_neuron ; i++){
		l2.append([])
		for j in range(HIDDEN_NEURON2):
		#for (j = 0 ; j < hidden_neuron2 ; j++){
			l2[i].append(random.uniform(-1,1))
		

	# Init layer l3
	for i in range(HIDDEN_NEURON2):
	#for (i = 0 ; i < hidden_neuron2 ; i++){
		l3.append([])
		for j in range(OUTPUT_NEURON):
		#for (j = 0 ; j < output_neuron ; j++){
			l3[i].append(random.uniform(-1,1))


		


def neural_network():

	# Initialize brains with random values
	for i in range(individuals):
	#for (var i = 0 ; i < individuals ; i++){
		l1 = []
		l2 = []
		l3 = []

		initialize_neural_network(l1, l2, l3)

		b1 = random.uniform(-1,1)
		b2 = random.uniform(-1,1)
		b3 = random.uniform(-1,1)

		brain = []
		brain.append(l1)
		brain.append(l2)
		brain.append(l3)
		brain.append(b1)
		brain.append(b2)
		brain.append(b3)

		brain_set.append(brain)

def saveMostApt(index_fittest1,score_most_fittest):
	global currentGeneration
	global best_snake_brain
	global best_snake_food
	global best_snake_head

	np.save('checkpoints/'+str(currentGeneration)+'/brain_'+str(score_most_fittest)+'.npy', np.asarray(best_snake_brain))
	np.save('checkpoints/'+str(currentGeneration)+'/food', np.asarray(best_snake_food))
	np.save('checkpoints/'+str(currentGeneration)+'/head', np.asarray(best_snake_head))	


def replicate():
	
	global currentGeneration
	global current_snake_score
	global best_snake_brain
	global best_snake_head
	global best_snake_food
	global best_snake_score


	# Select 5 most fittest individuals, them, make a random selection for crossing over
	most_fittest_array = []

	index_fittest1 = np.argmax(score_set)

	file = open('checkpoints/scores.txt', 'a')
	score_most_fittest = score_set[index_fittest1]
	file.write(str(score_most_fittest)+'\n')
	file.close()

	print(score_set[index_fittest1])
	score_set[index_fittest1] = float('-Inf')

	index_fittest2 = np.argmax(score_set)
	print(score_set[index_fittest2])
	score_set[index_fittest2] = float('-Inf')

	index_fittest3 = np.argmax(score_set)
	print(score_set[index_fittest3])
	score_set[index_fittest3] = float('-Inf')


	most_fittest_array.append(index_fittest1)
	most_fittest_array.append(index_fittest2)
	most_fittest_array.append(index_fittest3)


	# Salva o mais apto
	saveMostApt(index_fittest1, score_most_fittest)
	currentGeneration += 1


	weightsLen = INPUT_NEURON*HIDDEN_NEURON1 + HIDDEN_NEURON1*HIDDEN_NEURON2 + HIDDEN_NEURON2*OUTPUT_NEURON + 3
	crossoverPoint = random.randrange(weightsLen)

	"""
	counter = 0
	# For each layer
	for i in range(3):
		for j in range(len(brain_set[most_fitted_individual][i])):
			for k in range(len(brain_set[most_fitted_individual][i][j])):
				if counter > weightsLen:
					brain_set[most_fitted_individual][i][j][k] = brain_set[most_fitted_individual2][i][j][k]
					counter += 1

	print("Crossover point: ")
	print(crossoverPoint)
	print(brain_set[most_fitted_individual])					
	print(brain_set[most_fitted_individua2])					
	"""	




	for i in range(individuals):	
		crossoverPoint = random.randrange(weightsLen)
		most_fittest_array_aux	= []
		most_fittest_array_aux = copy.deepcopy(most_fittest_array)
		index = random.randrange(3)
		most_fitted_individual = copy.deepcopy(brain_set[most_fittest_array_aux[index]])
		del most_fittest_array_aux[index]
		index2 = random.randrange(2)
		most_fitted_individual2 = copy.deepcopy(brain_set[most_fittest_array_aux[index2]])

		# Count the genes for single point crossingover. We consider the entire NN as a big single cromossomos
		counter = 0
		for j in range(INPUT_NEURON):

			for k in range (HIDDEN_NEURON1):
				prob = random.uniform(0, 100)

				if prob < MUTATION_PROBABILITY:
					brain_set[i][0][j][k] += np.random.normal(0, 1/6)
					#brain_set[i][0][j][k] = random.uniform(-1,1)


					if brain_set[i][0][j][k] > 1:
						brain_set[i][0][j][k] = 1
					if brain_set[i][0][j][k] < -1:
						brain_set[i][0][j][k] = -1						

				else:
					if counter > crossoverPoint:
						brain_set[i][0][j][k] = copy.deepcopy(most_fitted_individual2[0][j][k])
					else:
						brain_set[i][0][j][k] = copy.deepcopy(most_fitted_individual[0][j][k])

				counter += 1

			# Crossover the bias
			if counter > crossoverPoint:
				brain_set[i][3] = copy.deepcopy(most_fitted_individual2[3])
			else:
				brain_set[i][3] = copy.deepcopy(most_fitted_individual[3])

			counter += 1

				

		for j in range(HIDDEN_NEURON1):
			for k in range (HIDDEN_NEURON2):
				prob = random.uniform(0, 100)


				if prob < MUTATION_PROBABILITY:
					brain_set[i][1][j][k] += np.random.normal(0, 1/6)
					#brain_set[i][1][j][k] = random.uniform(-1,1)

					if brain_set[i][1][j][k] > 1:
						brain_set[i][1][j][k] = 1
					if brain_set[i][1][j][k] < -1:
						brain_set[i][1][j][k] = -1	

				else:
					if counter > crossoverPoint:
						brain_set[i][1][j][k] = copy.deepcopy(most_fitted_individual2[1][j][k])
					else:
						brain_set[i][1][j][k] = copy.deepcopy(most_fitted_individual[1][j][k])

				counter += 1

			# Crossover the bias
			if counter > crossoverPoint:
				brain_set[i][4] = copy.deepcopy(most_fitted_individual2[4])
			else:
				brain_set[i][4] = copy.deepcopy(most_fitted_individual[4])

			counter += 1
				

		for j in range(HIDDEN_NEURON2):
			for k in range (OUTPUT_NEURON):
				
				prob = random.uniform(0, 100)

				if prob < MUTATION_PROBABILITY:
					brain_set[i][2][j][k] += np.random.normal(0, 1/6)
					#brain_set[i][2][j][k] = random.uniform(-1,1)

					if brain_set[i][2][j][k] > 1:
						brain_set[i][2][j][k] = 1
					if brain_set[i][2][j][k] < -1:
						brain_set[i][2][j][k] = -1	

				else:
					if counter > crossoverPoint:
						brain_set[i][2][j][k] = copy.deepcopy(most_fitted_individual2[2][j][k])
					else:
						brain_set[i][2][j][k] = copy.deepcopy(most_fitted_individual[2][j][k])

				counter += 1

			# Crossover the bias
			if counter > crossoverPoint:
				brain_set[i][5] = copy.deepcopy(most_fitted_individual2[5])
			else:
				brain_set[i][5] = copy.deepcopy(most_fitted_individual[5])


		prob = random.uniform(0, 100)
		if prob < MUTATION_PROBABILITY:
			brain_set[i][3] += np.random.normal(0, 1/6)
			#brain_set[i][3] = random.uniform(-1,1)

			if brain_set[i][3] > 1:
				brain_set[i][3] = 1
			if brain_set[i][3] < -1:
				brain_set[i][3] = -1				
		else:
			brain_set[i][3] = copy.deepcopy(most_fitted_individual[3])
		
		prob = random.uniform(0, 100)
		if prob < MUTATION_PROBABILITY:
			brain_set[i][4] += np.random.normal(0, 1/6)
			#brain_set[i][4] = random.uniform(-1,1)

			if brain_set[i][4] > 1:
				brain_set[i][4] = 1
			if brain_set[i][4] < -1:
				brain_set[i][4] = -1	

		else:
			brain_set[i][4] = copy.deepcopy(most_fitted_individual[4])

		prob = random.uniform(0, 100)		
		if prob < MUTATION_PROBABILITY:
			brain_set[i][5] += np.random.normal(0, 1/6)
			#brain_set[i][5] = random.uniform(-1,1)

			if brain_set[i][5] > 1:
				brain_set[i][5] = 1
			if brain_set[i][5] < -1:
				brain_set[i][5] = -1	

		else:
			brain_set[i][5] = copy.deepcopy(most_fitted_individual[5])



####### End funcitions #########



# Initialize pygame
pygame.init()

individuals = 10
current_individual = 0
currentGeneration = 0

# Define constants for the screen width and height
SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 600
PIXEL_DIM = 50

INPUT_NEURON = 24
HIDDEN_NEURON1 = 18
HIDDEN_NEURON2 = 18
OUTPUT_NEURON = 4
MUTATION_PROBABILITY = 4

worm_set = []
brain_set = []
initial_food_position = []	# Save initial food position to replay the exacly same game after
initial_snake_position = [] # Save initial snake position to replay the exacly same game after

movement = 'left'	# Actual worm movement
last_position = []
score_set = []
checkpointTime = time.time()

# Replay the best snake in the end of each generation
best_snake_brain = []
best_snake_head = []
best_snake_food = []
best_snake_score = float('-inf')
current_snake_brain = []
current_snake_head = []
current_snake_food = []
current_snake_score = 0
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255, 128))

try:
	os.mkdir('checkpoints/'+str(currentGeneration))
except FileExistsError:
	pass

# Init NN
neural_network()
newGame()
food = getRandomVector()
"""
# Sem dar load
"""
seed = initial_food_position[current_individual]


"""
 Carregando
"""

# If we want replay a snake, we must rewrite the position food with the same random state of previously snake
brain_set[0] = np.load('checkpoints/616/brain_64926.npy', allow_pickle=True).tolist()

foods = np.load('checkpoints/616/food.npy').tolist()
#foods = 0
worm_set[0] = [np.load('checkpoints/616/head.npy', allow_pickle=True).tolist(), 'alive']
replay = 1
currentFood = 1
food = foods[0]
#food = 0
"""
a
"""

#print(foods)
#print(worm_set[0])
#print(current_individual)

#random.seed(seed)
#newFoodPosition(current_individual)

current_snake_food.append(copy.deepcopy(food))
current_snake_head = copy.deepcopy(worm_set[current_individual][0])

network = DrawNN([24, 8, 8, 4 ], brain_set[current_individual], screen)

# Avoid worm in looping
wormLoop = 0
# Variable to keep the main loop running
running = True

#worm_set = [[[250, 250], [300, 250], [350, 250], [400, 250], [450, 250], [500, 250], [550, 250], [600, 250], [650, 250], [700, 250], [750, 250], [800, 250], [850, 250], [900, 250], [950, 250], [1000, 250], [1000, 200], 'alive']]

oi = 0

frame_count = 0
# Main loop
while running:

	# Look at every event in the queue
	for event in pygame.event.get():

		# Did the user hit a key?
		if event.type == KEYDOWN:
			# Was it the Escape key? If so, stop the loop.
			if event.key == K_ESCAPE:
				running = False

			if event.key == pygame.K_w:
				movement = 'up'

			if event.key == pygame.K_d:
				movement = 'right'

			if event.key == pygame.K_s:
				movement = 'down'

			if event.key == pygame.K_a:
				movement = 'left'

			if event.key == pygame.K_q:
				worm_set[current_individual][len(worm_set[current_individual])-1] = 'dead'
				current_individual += 1
				continue
	            

		# Did the user click the window close button? If so, stop the loop.
		elif event.type == QUIT:
			running = False


	# Refresh the screen
	ts = time.time()*1000
	if (checkpointTime - ts ) < 0:
	#if True:


		input = [p1(worm_set[current_individual][0], food),
		p2(worm_set[current_individual][0], food),
		p3(worm_set[current_individual][0], food),
		p4(worm_set[current_individual][0], food),
		p5(worm_set[current_individual][0], food),
		p6(worm_set[current_individual][0], food),
		p7(worm_set[current_individual][0], food),
		p8(worm_set[current_individual][0], food),
		border1(worm_set[current_individual][0]),
		border2(worm_set[current_individual][0]),
		border3(worm_set[current_individual][0]),
		border4(worm_set[current_individual][0]),
		border5(worm_set[current_individual][0]),
		border6(worm_set[current_individual][0]),
		border7(worm_set[current_individual][0]),
		border8(worm_set[current_individual][0]),
		border1_body(worm_set[current_individual]),
		border2_body(worm_set[current_individual]),
		border3_body(worm_set[current_individual]),
		border4_body(worm_set[current_individual]),
		border5_body(worm_set[current_individual]),
		border6_body(worm_set[current_individual]),
		border7_body(worm_set[current_individual]),
		border8_body(worm_set[current_individual]),
		]

		
		output = neural_network_inference(input, current_individual)
		movement = np.argmax(output)

		if movement == 0:
			movement = 'left'
		elif movement == 1:
			movement = 'up'
		elif movement == 2:
			movement = 'right'
		else:
			movement = 'down'
		

		worm_status = update(movement, current_individual)		

		# If alread passes some time in the same worm, this means a worm looping
		if wormLoop >= 200:
			#print("matando por looping")
			worm_status = 'dead'

		if worm_status == 'dead':

			print("Geração " + str(currentGeneration) + ' individuo ' + str(current_individual))
			print(current_snake_head)
			print(current_snake_food)
			print(brain_set[current_individual])
			print("\n\n")

			if score_set[current_individual] > best_snake_score:
				print("Atualizando melhor snake")
				best_snake_brain = copy.deepcopy(brain_set[current_individual])
				best_snake_head = copy.deepcopy(current_snake_head)
				best_snake_food = copy.deepcopy(current_snake_food)
				best_snake_score = score_set[current_individual]




			current_individual += 1
			wormLoop = 0


			exit()
			if current_individual == individuals:

				replicate()

				try:
					os.mkdir('checkpoints/'+str(currentGeneration))
				except FileExistsError:
					pass			

				newGame()
				newFoodPosition(current_individual)

				best_snake_head = []
				best_snake_food = []
				best_snake_score = float('-inf')

				current_snake_score = 0
				current_snake_head = copy.deepcopy(worm_set[current_individual][0])

				current_snake_food = []		
				current_snake_food.append(copy.deepcopy(food))	

				if oi == 30:
					exit()						
				oi += 1


				continue

			# If new individual begins
			newFoodPosition(current_individual)




			current_snake_head = copy.deepcopy(worm_set[current_individual][0])				

			current_snake_food = []		
			current_snake_food.append(copy.deepcopy(food))				


			continue

		# Update the score for staing alive
		updateScoreAlive(current_individual)
		wormLoop += 1
		
		#pygame.image.save(screen, "record/worms/visualizacao_linhas_new/"+str(frame_count)+".png")		

		draw(current_individual)

		checkpointTime = time.time()*1000# +1000

		
		
		frame_count += 1
