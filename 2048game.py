# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 20:15:44 2019

@author: cameron gemmell
"""
# TODO
#=============================
# -run in python2
# -direction is now a vector please god don't break it please
#=============================

import pygame
import random

pygame.init()
random.seed()

exited = False
gameDisplay = pygame.display.set_mode((400,500))
pygame.display.set_caption("2048 Clone")
clock = pygame.time.Clock()

# Board constants
BOARD_SIDE = 360
BOARD_POS = [20,120]
NUM_CELLS = 4
CELL_SIDE = BOARD_SIDE/NUM_CELLS

# Board variables
NUM_TURNS = 0

# Board cells definition
board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] # 4 rows of 4 columns of Cells of score 0 (empty) by default

# Color definitions
color_bg = (78,191,255)
color_board = (60,128,255)
color_white = (255,255,255)
color_black = (0,0,0)
color_beige = (238,207,125)
color_yellow = (255,255,96)
color_orange = (255,140,60)
color_red = (255,0,55)

# Font definitions
gameFont = pygame.font.Font(None, 36)
uiFont = pygame.font.Font(None,48)

# Create two initial cells
def gameInit():
    createCell(1)
    createCell(1)
    global NUM_TURNS # Bring turn counter into scope
    NUM_TURNS = 0

# lowestCell = cell to create (always match lowest number)
def createCell(lowestCell):

    #print
    #print("---------------------------------------------")
    #print("Creating Cell")
    #print

    # Get the empty elements
    emptyBoard = []

    # For every cell
    for i in range (0, NUM_CELLS):
        for j in range (0, NUM_CELLS):
            if (board[i][j] == 0): # If cell is empty
               emptyBoard.append([i,j]) 

    if len(emptyBoard)>0: # If there are empty boards
        emptyCellIndex = random.randint(0,len(emptyBoard)-1)
        #print("Empty index: " + str(emptyCellIndex))
        #print("Empty co-ords: " + str(emptyBoard[emptyCellIndex]))
        #print
        board[emptyBoard[emptyCellIndex][0]][emptyBoard[emptyCellIndex][1]] = lowestCell
        #print("Cell created.")
        #print("----------------------------------------------")
    else:
        # Otherwise board is full
        return False

    return True

def getLowestCell():
    lowest = max(board) # Set lowest to highest (0 shouldn't be counted as cell)

    for x in range (0,4):
        for y in range (0,4):
            if (board[x][y]<lowest) and (board[x][y]>0):
                lowest = board[x][y]

    # If lowest is a useable number
    if (lowest>0):
        return lowest

    # Else return 1 as the lowest
    return 1

def draw():
    # Background
    gameDisplay.fill(color_bg)
    # Top UI Section
    pygame.draw.rect(gameDisplay, color_board, (20,20,360,80))
    pygame.draw.rect(gameDisplay, color_white, (20,20,360,80), 2)
    if (NUM_TURNS>0):
        scoreText = uiFont.render("Turns Survived: "+str(NUM_TURNS),True,color_white)
    else:
        scoreText = uiFont.render("Good Luck!",True,color_white)
    gameDisplay.blit(scoreText,(20+180-(scoreText.get_width()/2),20+40-(scoreText.get_height()/2)))
    # Board
    pygame.draw.rect(gameDisplay, color_board, (BOARD_POS[0],BOARD_POS[1],BOARD_SIDE,BOARD_SIDE))
    # Board cells
    counterx = 0
    for i in range(NUM_CELLS):
        countery = 0
        for j in range(NUM_CELLS):
            # Draw colour of cells
            if board[i][j]>0:
                color_cell = color_beige
                if board[i][j]>=1024:
                    color_cell = color_yellow
                if board[i][j]>=1536:
                    color_cell = color_orange
                if board[i][j]>=2048:
                    color_cell = color_red
                pygame.draw.rect(gameDisplay, color_cell, (BOARD_POS[0]+(counterx*CELL_SIDE),BOARD_POS[1]+(countery*CELL_SIDE),CELL_SIDE,CELL_SIDE))
                pygame.draw.rect(gameDisplay, color_white, (BOARD_POS[0]+(counterx*CELL_SIDE),BOARD_POS[1]+(countery*CELL_SIDE),CELL_SIDE,CELL_SIDE), 2)
            
                # Draw text on cells if cell isn't empty
                cellText = gameFont.render(str(board[i][j]),True,color_white)
                gameDisplay.blit(cellText,((BOARD_POS[0]+(counterx*CELL_SIDE)+((CELL_SIDE-cellText.get_width())/2)),((BOARD_POS[1]+(countery*CELL_SIDE)+((CELL_SIDE-cellText.get_height())/2)))))

            countery+=1
        counterx+=1

    # Board border
    pygame.draw.rect(gameDisplay, color_white, (BOARD_POS[0],BOARD_POS[1],BOARD_SIDE,BOARD_SIDE), 2)

    pygame.display.flip()

# Move every cell along in the direction until there is no whitespace remaining
def removeWhitespace(direction):
    # direction is an array with two values: x and y (vector for the cool maths nerds)
    whitespaceExists = False
    
    # Loop for as many times as could be needed
    for x in range (0,NUM_CELLS):
        # Loop over the cells in the board
        for i in range (0,NUM_CELLS):
            for j in range (0,NUM_CELLS):
                if (board[i][j] > 0): # If cell is filled in
                    newPos = [i-direction[0],j-direction[1]] # Get the new proposed position (position + direction)
                    if (0 <= newPos[0] < NUM_CELLS) and (0<= newPos[1] < NUM_CELLS):# If this isn't out of bounds
                        if (board[newPos[0]][newPos[1]] <= 0): # If this isn't filled in
                            board[newPos[0]][newPos[1]] = board[i][j]; # Set the new position
                            board[i][j] = 0 # Empty the old position

def moveGame(direction):
    # direction is an array with two values: x and y
    global NUM_TURNS # Bring turn counter into scope
    NUM_TURNS+=1 # Increment turn counter
    moved = False # Tracker for recursion
    
    removeWhitespace(direction) 
   
    # if not working, try looping by NUM_CELLS
    # for every cell
    #for i in range (NUM_CELLS):
    for x in range (NUM_CELLS):
        for y in range (NUM_CELLS):
            # Get new cell position
            newPos = [x-direction[0],y-direction[1]]
            if (0 <= newPos[0] < NUM_CELLS) and (0 <= newPos[1] < NUM_CELLS): # If the new position is in range
                if (board[x][y] == board[newPos[0]][newPos[1]]): # If the cells are the same
                    board[newPos[0]][newPos[1]] = board[x][y]*2 # Update the new position
                    board[x][y] = 0 # Clear the old one

    removeWhitespace(direction)
    
    cellCreated = createCell(getLowestCell())# Create a cell. if this has failed, user has lost the game
    return cellCreated

#==========================================================
# MAIN PROGRAM
#==========================================================
gameInit()
print("Game initialised.")
while not exited: # Game loop
    
    moveDir = [0,0] # If less than or equal to 0, don't move

    for event in pygame.event.get(): # Event handling
        
        if event.type == pygame.QUIT:
            exited = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exited = True
            if event.key == pygame.K_UP: # Up key pressed
                moveDir = [0,1]
                break
            if event.key == pygame.K_LEFT: # Left key pressed
                moveDir = [1,0]
                break
            if event.key == pygame.K_DOWN: # Down key pressed
                moveDir = [0,-1]
                break
            if event.key == pygame.K_RIGHT: # Right key pressed
                moveDir = [-1,0]
                break
    
    if (moveDir!=[0,0]):

        if (moveGame(moveDir) == False):
            exited = True 
        moveDir = [0,0]

    draw()
    
    pygame.display.update()
    clock.tick(20) # 20 Frames per second

print("Exiting game..")
pygame.quit()
quit()
