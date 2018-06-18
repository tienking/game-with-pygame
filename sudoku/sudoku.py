import pygame, sys, random, copy
from pygame.locals import *

WINDOWWIDTH = 1200
WINDOWHEIGHT = 700
BOXSIZE = 70
GAPSIZE = 5
SUDOKUFONT = 'lib/sudokufont.ttf'
DATA = 'lib/data.txt'

BOARDSIZE = 9 * (BOXSIZE + GAPSIZE) + GAPSIZE
XMARGIN = int((WINDOWWIDTH - BOARDSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDSIZE) / 2)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (193, 205, 205)
DARKRED = (124, 0, 0)
RED = (168, 0, 0)
BLUE = (15, 0, 183)
DARKBLUE = (0, 28, 102)
JADEGREEN = (19, 142, 133)
LIGHTBLACK = (117, 117, 117)
GREEN = (43, 124, 0)

COVERBOXCOLOR = DARKBLUE
BOXCOLOR = WHITE
LINECOLOR = LIGHTBLACK
BACKGROUNDCOLOR = SILVER
RESETBOXCOLOR = RED
NUMBERCOLOR = BLACK
CHECKNUMBERCOLOR = DARKRED
TEXTCOLOR = WHITE
WINBOXCOLOR = RED
HIGHLIGHTCOLOR = GREEN

def main():
	global DISPLAY, data
	pygame.init()
	DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption("Sudoku")

	drawBoard()
	board = insertData()
	checkboard = copy.deepcopy(board)
	position = [0,0]
	highlightposition = (0,0)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif (event.type == KEYUP and event.key == K_UP):
				position[1] -= 1
			elif (event.type == KEYUP and event.key == K_DOWN):
				position[1] += 1
			elif (event.type == KEYUP and event.key == K_LEFT):
				position[0] -= 1
			elif (event.type == KEYUP and event.key == K_RIGHT):
				position[0] += 1

			if event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				if resetButtonClick(mousex, mousey):
					board, checkboard = resetGame(board, checkboard, position, highlightposition)

			if position[0] == 9:
				position[0] = 0
			elif position[0] == -1:
				position[0] = 8

			if position[1] == 9:
				position[1] = 0
			elif position[1] == -1:
				position[1] = 8

			col = position[0]
			row = position[1]

			if checkEmptyBox(checkboard, col, row):
				if (event.type == KEYUP and event.key == K_1):
					deleteNumber(col, row)
					insertNumber(col ,row, 1)
					board[row][col] = 1
				elif (event.type == KEYUP and event.key == K_2):
					deleteNumber(col, row)
					insertNumber(col, row, 2)
					board[row][col] = 2
				elif (event.type == KEYUP and event.key == K_3):
					deleteNumber(col, row)
					insertNumber(col, row, 3)
					board[row][col] = 3
				elif (event.type == KEYUP and event.key == K_4):
					deleteNumber(col, row)
					insertNumber(col, row, 4)
					board[row][col] = 4
				elif (event.type == KEYUP and event.key == K_5):
					deleteNumber(col, row)
					insertNumber(col, row, 5)
					board[row][col] = 5
				elif (event.type == KEYUP and event.key == K_6):
					deleteNumber(col, row)
					insertNumber(col, row, 6)
					board[row][col] = 6
				elif (event.type == KEYUP and event.key == K_7):
					deleteNumber(col, row)
					insertNumber(col, row, 7)
					board[row][col] = 7
				elif (event.type == KEYUP and event.key == K_8):
					deleteNumber(col, row)
					insertNumber(col, row, 8)
					board[row][col] = 8
				elif (event.type == KEYUP and event.key == K_9):
					deleteNumber(col, row)
					insertNumber(col, row, 9)
					board[row][col] = 9

				if (event.type == KEYUP and event.key == K_0) or (event.type == KEYUP and event.key == K_SPACE):
					deleteNumber(col, row)

		setHighlight(col, row, "draw")
		if (col, row) != highlightposition:
			setHighlight(highlightposition[0],highlightposition[1],"erase")
			setHighlight(col, row, "draw")
			highlightposition = (col, row)

		if checkWon(board):
			showWinScreen()
			pygame.display.update()
			pygame.time.wait(5000)
			board, checkboard = resetGame(board, checkboard, position, highlightposition)

		pygame.display.update()

def convertToPixel(col, row):
	x = XMARGIN + GAPSIZE + col * (GAPSIZE + BOXSIZE)
	y = YMARGIN + GAPSIZE + row * (GAPSIZE + BOXSIZE)
	return(x, y)

def readData():
	textinput = open(DATA, "r")
	datalist = textinput.readlines()
	data = []
	for line in datalist:
		row = (int(x) for x in list(line) if x != '\n')
		data.append(row)
	return data

def insertData():
	data = readData()
	numberlist = list(random.choice(data))

	board = []
	index = 0
	for i in range(9):
		col = []
		for j in range(9):
			col.append(numberlist[index])
			index += 1
		board.append(col)

	for i in range(9):
		for j in range(9):
			if board[i][j] != 0:
				x, y = convertToPixel(j, i)
				fontObj = pygame.font.Font(SUDOKUFONT,75)
				textObj = fontObj.render(str(board[i][j]),True,NUMBERCOLOR)
				textRectObj = textObj.get_rect(center = (int(x + BOXSIZE / 2), int(y + BOXSIZE / 2)))
				DISPLAY.blit(textObj, textRectObj)

	return board

def drawBoard():
	DISPLAY.fill(BACKGROUNDCOLOR)
	drawResetButton()
	pygame.draw.rect(DISPLAY,LINECOLOR, (XMARGIN, YMARGIN, BOARDSIZE, BOARDSIZE))
	for i in range(9):
		for j in range(9):
			pygame.draw.rect(DISPLAY, BOXCOLOR, (XMARGIN + j * (GAPSIZE + BOXSIZE) + GAPSIZE, YMARGIN + i * (GAPSIZE + BOXSIZE) + GAPSIZE, BOXSIZE, BOXSIZE))

	for i in range(4):
		pygame.draw.rect(DISPLAY, COVERBOXCOLOR,(XMARGIN, YMARGIN + i * 3 * (GAPSIZE + BOXSIZE), BOARDSIZE, GAPSIZE))

	for i in range(4):
		pygame.draw.rect(DISPLAY, COVERBOXCOLOR,(XMARGIN + i * 3 * (GAPSIZE + BOXSIZE), YMARGIN, GAPSIZE, BOARDSIZE))

def drawResetButton():
	pygame.draw.rect(DISPLAY, RESETBOXCOLOR, (10,10,100,50))
	fontObj = pygame.font.Font(SUDOKUFONT,35)
	textObj = fontObj.render("RESET",True,TEXTCOLOR)
	textRectObj = textObj.get_rect(center = (55, 35))
	DISPLAY.blit(textObj, textRectObj)

def resetButtonClick(mousex, mousey):
	boxRect = pygame.Rect(10,10,100,50)
	if boxRect.collidepoint(mousex, mousey):
		return True
	else:
		return False

def setHighlight(col, row, option):
	x, y = convertToPixel(col, row)
	if option == "draw":
		color = HIGHLIGHTCOLOR
	else:
		color = WHITE
	pygame.draw.rect(DISPLAY, color, (x + 3, y + 3, BOXSIZE - 6, BOXSIZE - 6), 3)

def insertNumber(col, row, number):
	x, y = convertToPixel(col, row)
	fontObj = pygame.font.Font(SUDOKUFONT,75)
	textObj = fontObj.render(str(number),True,CHECKNUMBERCOLOR)
	textRectObj = textObj.get_rect(center = (int(x + BOXSIZE / 2), int(y + BOXSIZE / 2)))
	DISPLAY.blit(textObj, textRectObj)

def deleteNumber(col, row):
	x, y = convertToPixel(col, row)
	pygame.draw.rect(DISPLAY, WHITE, (x + 2, y + 2, BOXSIZE - 4, BOXSIZE - 4))

def checkEmptyBox(checkboard, col, row):
	if checkboard[row][col] == 0:
		return True
	else: 
		return False

def checkFinish(board):
	for list in board:
		if 0 in list:
			return False
	return True

def checkCorrectNumber(numarray):
	check = True
	for list in numarray:
		num = [1,2,3,4,5,6,7,8,9]
		for number in list:
			if number in num:
				num.remove(number)
		if len(num) > 0:
			check = False
	return check

def checkWon(board):
	if checkFinish(board) == True:
		
		tempboard = [[] for x in range(3)]
		for i in range(3):
			for j in range(3):
				tempboard[i] += board[j][:]

		boxes = [[] for x in range(9)]
		index = 0
		for groupbox in tempboard:
			for i in range(3):
				for j in range(3):
					boxes[index] += groupbox[i * 3 + j * 9:i * 3 + j * 9 + 3]
				index += 1

		colboard = [[] for x in range(9)]
		for i in range(9):
			for j in range(9):
				colboard[j].append(board[i][j])

		check1 = checkCorrectNumber(board)
		check2 = checkCorrectNumber(colboard)
		check3 = checkCorrectNumber(boxes)

		if (check1 == True and check2 == True) and check3 == True:
			return True
		else:
			return False
	return False

def showWinScreen():
	DISPLAY.fill(SILVER)
	pygame.draw.rect(DISPLAY,WINBOXCOLOR, (XMARGIN, YMARGIN, BOARDSIZE, BOARDSIZE))
	fontObj = pygame.font.Font(SUDOKUFONT,150)
	textObj = fontObj.render("VICTORY", True, TEXTCOLOR)
	textRectObj = textObj.get_rect(center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)))
	DISPLAY.blit(textObj, textRectObj)

def resetGame(board, checkboard, position, highlightposition):
	drawBoard()
	board = insertData()
	checkboard = copy.deepcopy(board)
	return (board, checkboard)

if __name__ == '__main__':
	main()