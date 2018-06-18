import pygame, sys, random
from pygame.locals import *

FPS = 60

TUBEWIDTH = 80
TUBEHEIGHT = 350
SPACE = 300
HOLEHEIGHT = 110
BIRDSTAND = 50
TUBENUMBER = 3
WINDOWWIDTH = (SPACE + TUBEWIDTH) * TUBENUMBER
WINDOWHEIGHT = 500

LOSEFONT = 'lib/losefont.ttf'
SCOREFONT = 'lib/scorefont.ttf'
BACKGROUND = 'lib/background.png'
BIRDIMAGE = 'lib/bird.png'
TUBEUP = 'lib/tubeup.png'
TUBEDOWN = 'lib/tubedown.png'

GREEN = (36, 183, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
SILVER = (193, 205, 205)
DARKRED = (205, 51, 51)


def main():
	
	global DISPLAY, FPSCLOCK
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

	pygame.display.set_caption("Flappy Bird")

	bird = pygame.image.load(BIRDIMAGE)
	background = pygame.image.load(BACKGROUND)
	background = pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))
	
	birdsize = bird.get_rect().size
	birdposition = 0	
	tubelist = []
	score = 0
	birdposition, tubelist, score = startGame(birdposition, tubelist, background, score)
	speed = 5

	while True:
		DISPLAY.blit(background, (0, 0))
		fly = False
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == KEYUP and (event.key == K_w or event.key == K_SPACE):
				fly = True

		if fly == True:
			birdposition -= 50
		else:
			birdposition += 3

		if birdposition < 0:
			birdposition = 0

		tubelist, score = movingTubes(tubelist, speed, score)
		drawTubes(tubelist)
		drawBird(bird, birdposition)
		drawScoreBox(score)

		if checkLose(tubelist, birdposition, birdsize):
			drawLoseScreen()
			pygame.display.update()
			pygame.time.wait(3000)
			birdposition, tubelist, score = startGame(birdposition, tubelist, background, score)

		pygame.display.update()
		FPSCLOCK.tick(FPS)

def startGame(birdposition, tubelist, background, score):
	DISPLAY.blit(background, (0, 0))
	birdposition = WINDOWHEIGHT / 2
	tubelist = createTubeList(tubelist)
	score = 0
	return(birdposition, tubelist, score)

def drawBird(bird, birdposition):
	DISPLAY.blit(bird,(BIRDSTAND,birdposition))

def getRandomTubeHeight():
	number = random.randint(int(WINDOWHEIGHT / 6),int(WINDOWHEIGHT * 5 / 6) - HOLEHEIGHT)
	return number

def createNewTube(tubelist):
	newcol = getRandomTubeHeight()
	tubelist.append([WINDOWWIDTH + SPACE, newcol])
	return tubelist

def createTubeList(tubelist):
	tubelist = []
	firstposition = WINDOWWIDTH
	for i in range(TUBENUMBER + 1):
		tubelist.append([firstposition, getRandomTubeHeight()])
		firstposition += TUBEWIDTH + SPACE
	return tubelist

def movingTubes(tubelist, speed, score):
	for tube in tubelist:
		tube[0] -= speed
	if tubelist[0][0] <= -TUBEWIDTH:
		del tubelist[0]
		createNewTube(tubelist)
	if tubelist[0][0] == BIRDSTAND - TUBEWIDTH:
		score += 1
	return(tubelist, score)

def drawTubes(tubelist):
	for tube in tubelist:
		tubeup = pygame.image.load(TUBEUP)
		tubeup = pygame.transform.scale(tubeup, (TUBEWIDTH, TUBEHEIGHT))
		DISPLAY.blit(tubeup, (tube[0], tube[1] - TUBEHEIGHT))
		tubedown = pygame.image.load(TUBEDOWN)
		tubedown = pygame.transform.scale(tubedown, (TUBEWIDTH, TUBEHEIGHT))
		DISPLAY.blit(tubedown, (tube[0], tube[1] + HOLEHEIGHT))	

def checkHitTube(tubelist, birdposition, birdsize):
	birdRect = pygame.Rect(BIRDSTAND, birdposition, birdsize[0], birdsize[1])
	for tube in tubelist:
		uptube = pygame.Rect(tube[0], 0, TUBEWIDTH, tube[1])
		downtube = pygame.Rect(tube[0], tube[1] + HOLEHEIGHT, TUBEWIDTH, WINDOWHEIGHT - tube[1] - HOLEHEIGHT)
		if birdRect.colliderect(uptube) or birdRect.colliderect(downtube):
			return True
	return False

def checkFallDown(birdposition, birdsize):
	if birdposition >= WINDOWHEIGHT - birdsize[1]:
		return True
	return False

def drawLoseScreen():
	fontObj = pygame.font.Font(LOSEFONT, 100)
	textObj = fontObj.render("YOU LOSE", True, BLACK)
	textRectObj = textObj.get_rect(center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)))
	DISPLAY.blit(textObj, textRectObj)

def checkLose(tubelist, birdposition, birdsize):
	if checkHitTube(tubelist, birdposition, birdsize) or checkFallDown(birdposition, birdsize):
		return True
	return False

def drawScoreBox(score):
	pygame.draw.rect(DISPLAY, SILVER, (10, 10, 100, 50))
	fontObj = pygame.font.Font(SCOREFONT, 25)
	textObj = fontObj.render("Score: " + str(score), True, BLACK)
	textRectObj = textObj.get_rect(center = (60, 35))
	DISPLAY.blit(textObj, textRectObj)

if __name__ == '__main__':
	main()


