import pygame
import sys
import random
import glob
from pygame.locals import *
from os.path import join

FPS = 60
DEFAULT_CHARACTER_SIZE = (56, 36)
TUBEWIDTH = DEFAULT_CHARACTER_SIZE[0] * 1.5
TUBEHEIGHT = 350
SPACE = TUBEWIDTH * 3.5
HOLEHEIGHT = DEFAULT_CHARACTER_SIZE[1] * 3.5
CHARACTERSTAND = 40
TUBENUMBER = 3
WINDOWWIDTH = (SPACE + TUBEWIDTH) * TUBENUMBER
WINDOWHEIGHT = 500

LIB_FOLDER = 'lib'
IMAGE_FOLDER = 'image'
FONT_FOLDER = 'font'
BG_FOLDER = 'background'
OBJ_FOLDER = 'object'
CHAR_FOLDER = 'character'

LOSEFONT = join(LIB_FOLDER, FONT_FOLDER, 'losefont.ttf')
SCOREFONT = join(LIB_FOLDER, FONT_FOLDER, 'scorefont.ttf')
CHARIMAGE = join(".",LIB_FOLDER, IMAGE_FOLDER, CHAR_FOLDER, '*.png')
BACKGROUND = join(".",LIB_FOLDER, IMAGE_FOLDER, BG_FOLDER, '*.png')
TUBEUP = join(LIB_FOLDER, IMAGE_FOLDER, OBJ_FOLDER, 'tube_up.png')
TUBEDOWN = join(LIB_FOLDER, IMAGE_FOLDER, OBJ_FOLDER, 'tube_down.png')

CHARACTER_LIST = glob.glob(CHARIMAGE)
BACKGROUND_LIST = glob.glob(BACKGROUND)

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

    pygame.display.set_caption("Flappy Game")

    character, charactersize, background = get_random_images()
    characterposition = 0	
    tubelist = []
    score = 0
    characterposition, tubelist, score = start_game(characterposition, tubelist, background, score)
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
            characterposition -= 50
        else:
            characterposition += 3

        if characterposition < 0:
            characterposition = 0

        tubelist, score = move_tubes(tubelist, speed, score)
        draw_tubes(tubelist)
        draw_character(character, characterposition)
        draw_score_box(score)

        if check_lose(tubelist, characterposition, charactersize):
            draw_lose_screen()
            pygame.display.update()
            pygame.time.wait(3000)
            character, charactersize, background = get_random_images()
            characterposition, tubelist, score = start_game(characterposition, tubelist, background, score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def get_random_images():
    character = pygame.image.load(random.choice(CHARACTER_LIST))
    character = pygame.transform.scale(character, DEFAULT_CHARACTER_SIZE)
    charactersize = character.get_rect().size

    background = pygame.image.load(random.choice(BACKGROUND_LIST))
    background = pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))

    return (character, charactersize, background)

def start_game(characterposition, tubelist, background, score):
	DISPLAY.blit(background, (0, 0))
	characterposition = WINDOWHEIGHT / 2
	tubelist = create_tube_list(tubelist)
	score = 0
	return (characterposition, tubelist, score)

def draw_character(character, characterposition):
	DISPLAY.blit(character,(CHARACTERSTAND,characterposition))

def get_random_tube_height():
	number = random.randint(int(WINDOWHEIGHT / 6),int(WINDOWHEIGHT * 5 / 6) - HOLEHEIGHT)
	return number

def create_new_tube(tubelist):
	newcol = get_random_tube_height()
	tubelist.append([WINDOWWIDTH + SPACE, newcol])
	return tubelist

def create_tube_list(tubelist):
	tubelist = []
	firstposition = WINDOWWIDTH
	for i in range(TUBENUMBER + 1):
		tubelist.append([firstposition, get_random_tube_height()])
		firstposition += TUBEWIDTH + SPACE
	return tubelist

def move_tubes(tubelist, speed, score):
	for tube in tubelist:
		tube[0] -= speed
	if tubelist[0][0] <= -TUBEWIDTH:
		del tubelist[0]
		create_new_tube(tubelist)
	if tubelist[0][0] == CHARACTERSTAND - TUBEWIDTH:
		score += 1
	return (tubelist, score)

def draw_tubes(tubelist):
	for tube in tubelist:
		tubeup = pygame.image.load(TUBEUP)
		tubeup = pygame.transform.scale(tubeup, (TUBEWIDTH, TUBEHEIGHT))
		DISPLAY.blit(tubeup, (tube[0], tube[1] - TUBEHEIGHT))
		tubedown = pygame.image.load(TUBEDOWN)
		tubedown = pygame.transform.scale(tubedown, (TUBEWIDTH, TUBEHEIGHT))
		DISPLAY.blit(tubedown, (tube[0], tube[1] + HOLEHEIGHT))	

def check_hit_tube(tubelist, characterposition, charactersize):
	characterRect = pygame.Rect(CHARACTERSTAND, characterposition, charactersize[0], charactersize[1])
	for tube in tubelist:
		uptube = pygame.Rect(tube[0], 0, TUBEWIDTH, tube[1])
		downtube = pygame.Rect(tube[0], tube[1] + HOLEHEIGHT, TUBEWIDTH, WINDOWHEIGHT - tube[1] - HOLEHEIGHT)
		if characterRect.colliderect(uptube) or characterRect.colliderect(downtube):
			return True
	return False

def check_fall_down(characterposition, charactersize):
	if characterposition >= WINDOWHEIGHT - charactersize[1]:
		return True
	return False

def draw_lose_screen():
	fontObj = pygame.font.Font(LOSEFONT, 100)
	textObj = fontObj.render("YOU LOSE", True, BLACK)
	textRectObj = textObj.get_rect(center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)))
	DISPLAY.blit(textObj, textRectObj)

def check_lose(tubelist, characterposition, charactersize):
	if check_hit_tube(tubelist, characterposition, charactersize) or check_fall_down(characterposition, charactersize):
		return True
	return False

def draw_score_box(score):
	pygame.draw.rect(DISPLAY, SILVER, (10, 10, 100, 50))
	fontObj = pygame.font.Font(SCOREFONT, 25)
	textObj = fontObj.render("Score: " + str(score), True, BLACK)
	textRectObj = textObj.get_rect(center = (60, 35))
	DISPLAY.blit(textObj, textRectObj)

if __name__ == '__main__':
	main()


