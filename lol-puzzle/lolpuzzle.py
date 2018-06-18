import pygame, sys, random
from pygame.locals import *

allchampion = ['aatrox','ahri','akali','blitzcrank','camille','darius','ekko','ezreal','galio','illaoi','jhin','kennen','kled','leesin','missfortune','nasus','pantheon','poppy','rammus','rengar','sion','varus','vayne','veigar','wukong','zoe','alistar','amumu','anivia','ashe','azir','bard','braum','caitlyn','heimerdinger','janna','jayce','jinx','karma','kindred','lucian','masteryi','morgana','ornn','quinn','rakan','skarner','soraka','thresh','tristana','urgot','xerath','yasuo','zed']

WINDOWWIDTH = 1200
WINDOWHEIGHT = 700
GAPSIZE = 27
BOXSIZE = 48
ROWNUM = 3
COLNUM = 6
SCOREBOXWIDTH = 150
SCOREBOXHEIGHT = 50
FONT = 'puzzlefont.ttf'

FINALBLOCKWIDTH = int(WINDOWWIDTH / 2)
FINALBLOCKHEIGHT = int(WINDOWHEIGHT / 2)

BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
SILVER = (193,205,205)
DARKRED = (205,51,51)

XMARGIN = int((WINDOWWIDTH - ((GAPSIZE + BOXSIZE) * COLNUM + GAPSIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - ((GAPSIZE + BOXSIZE) * ROWNUM + GAPSIZE)) / 2)

def main():
	global DISPLAY
	pygame.init()
	DISPLAY = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), pygame.FULLSCREEN)

	pygame.display.set_caption("LOL Puzzle")

	mousex = 0
	mousey = 0

	DISPLAY.fill(SILVER)

	championlist = createChampionList()
	championimgs = dict.fromkeys(championlist, None)
	board = buildBoard(championlist, championimgs)
	
	firstXY = None
	checkWon = ROWNUM * COLNUM
	score = int((len(championlist) + (len(championlist) / 2)) / 2)
	checkHighlight = (None, None)
	while True:
		mouseClicked = False

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

		buildScoreBox(score)

		col, row = getChampionAtPixel(mousex, mousey)

		if (col, row) != (None, None):
			if checkHighlight == (None, None):
				setHighlightBox(col, row, "draw")
				checkHighlight = (col, row)
			elif checkHighlight != (col, row) and checkHighlight != None:
				setHighlightBox(checkHighlight[0], checkHighlight[1], "erase")
				setHighlightBox(col, row, "draw")
				checkHighlight = (col, row)
			pygame.display.update()

			checkHighlight = (col, row)
			if mouseClicked == True and firstXY == None:
				firstXY = (col, row)
				uncoverChampionBox(col, row, board, championimgs)
			elif mouseClicked == True and firstXY != (col, row):
				uncoverChampionBox(col, row, board, championimgs)
				pygame.display.update()
				if board[row][col] != board[firstXY[1]][firstXY[0]]:
					pygame.time.wait(1000)
					coverChampionBox(col, row)
					coverChampionBox(firstXY[0], firstXY[1])
					score -= 1
				else:
					checkWon -= 2
					if checkWon == 0:
						finalState("VICTORY")
						championlist = createChampionList()
						championimgs = dict.fromkeys(championlist, None)
						board = buildBoard(championlist, championimgs)
						checkWon = ROWNUM * COLNUM
						score = int((len(championlist) + (len(championlist) / 2)) / 2)
				firstXY = None
		elif checkHighlight != (None, None):
			setHighlightBox(checkHighlight[0], checkHighlight[1], "erase")
			checkHighlight = (None, None)

		pygame.display.update()

		if score == 0:
			finalState("FOOL")
			championlist = createChampionList()
			championimgs = dict.fromkeys(championlist, None)
			board = buildBoard(championlist, championimgs)
			checkWon = ROWNUM * COLNUM
			score = int((len(championlist) + (len(championlist) / 2)) / 2)


def createChampionList():
	championnum = int((ROWNUM * COLNUM) / 2)
	random.shuffle(allchampion)
	championlist = allchampion[:championnum] * 2
	random.shuffle(championlist)
	return championlist

def buildBoard(championlist, championimgs):
	for i in range(len(championlist)):
		championimgs[championlist[i]] = pygame.image.load('champion_imgs/' + championlist[i] + '.png')
	k = 0
	board = []
	for i in range(ROWNUM):
		column = []
		for j in range(COLNUM):
			x, y = convertToPixel(j, i)
			pygame.draw.rect(DISPLAY, BLACK,(x, y, BOXSIZE, BOXSIZE))
			column.append(championlist[k])
			k+=1
		board.append(column)
	return board

def buildScoreBox(score):
	pygame.draw.rect(DISPLAY, DARKRED, (5, 5, SCOREBOXWIDTH, SCOREBOXHEIGHT))
	fontObj = pygame.font.Font(FONT, 24)
	textSurfaceObj = fontObj.render('Score: ' + str(score), True, WHITE)
	textRectObj = textSurfaceObj.get_rect(topleft = (15 ,15))
	DISPLAY.blit(textSurfaceObj, textRectObj)

def convertToPixel(col, row):
	x = col * (BOXSIZE + GAPSIZE) + GAPSIZE + XMARGIN
	y = row * (BOXSIZE + GAPSIZE) + GAPSIZE + YMARGIN
	return (x,y)
	
def getChampionAtPixel(mousex, mousey):
	for col in range(COLNUM):
		for row in range(ROWNUM):
			x, y = convertToPixel(col,row)
			boxRect = pygame.Rect(x,y,BOXSIZE,BOXSIZE)
			if boxRect.collidepoint(mousex,mousey):
				return (col,row)
	return (None, None)

def coverChampionBox(col, row):
	x, y = convertToPixel(col, row)
	pygame.draw.rect(DISPLAY, BLACK, (x, y, BOXSIZE, BOXSIZE))

def uncoverChampionBox(col, row, board, championimgs):
	x, y = convertToPixel(col, row)
	DISPLAY.blit(championimgs.get(board[row][col]),(col * (BOXSIZE + GAPSIZE) + XMARGIN + GAPSIZE, row * (BOXSIZE + GAPSIZE) + GAPSIZE + YMARGIN))

def winAnimation():
	DISPLAY.fill(SILVER)
	pygame.draw.rect(DISPLAY, DARKRED, (int((WINDOWWIDTH - FINALBLOCKWIDTH) / 2), int((WINDOWHEIGHT - FINALBLOCKHEIGHT) / 2), FINALBLOCKWIDTH, FINALBLOCKHEIGHT))
	fontObj = pygame.font.Font(FONT,75)
	textObj = fontObj.render('VICTORY',True,WHITE)
	textRectObj = textObj.get_rect(center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)))
	DISPLAY.blit(textObj, textRectObj)

def setHighlightBox(col, row, option):
	if option == "draw":
		color = DARKRED
	else:
		color = SILVER

	x, y = convertToPixel(col, row)
	pygame.draw.rect(DISPLAY, color, (x - 5, y - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def finalState(result):
	DISPLAY.fill(SILVER)
	pygame.draw.rect(DISPLAY, DARKRED, (int((WINDOWWIDTH - FINALBLOCKWIDTH) / 2), int((WINDOWHEIGHT - FINALBLOCKHEIGHT) / 2), FINALBLOCKWIDTH, FINALBLOCKHEIGHT))
	fontObj = pygame.font.Font(FONT,100)
	textObj = fontObj.render(result,True,WHITE)
	textRectObj = textObj.get_rect(center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2)))
	DISPLAY.blit(textObj, textRectObj)
	pygame.display.update()
	pygame.time.wait(5000)
	DISPLAY.fill(SILVER)


if __name__ == '__main__':
    main()