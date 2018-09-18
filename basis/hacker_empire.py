import sys
import pygame
from pygame.locals import *
from random import randint

# define some datas
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 728
LOW_SPEED = 30
HIGH_SPEED = 70
LOW_SIZE = 5
HIGH_SIZE = 30
FONT_SIZE = 40
FONT_NAME = None
FREQUENCE = 50
times = 0


def randomcolor():
	return (randint(0, 255), randint(0, 255), randint(0, 255))


def randomspeed():
	return randint(LOW_SPEED, HIGH_SPEED)


def randomposition():
	return (randint(0, SCREEN_WIDTH), RANDINT(0, SCREEN_HEIGHT))


def randomsize():
	return randint(LOW_SIZE, HIGH_SIZE)


def randomname():
	return randint(0, 100000)


def randomvalue():
	return randint(0, 9)



# class of sprite
class Word(pygame.sprite.Sprite):

	def __init__(self, bornposition):
		pygame.sprite.Sprite.__init__(self)
		self.value = randomvalue()
		self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
		self.image = self.font.render(str(self.value), True, randomcolor())
		self.speed = randomspeed()
		self.rect = self.image.get_rect()
		self.rect.topleft = bornposition

	def update(self):
		self.rect = self.rect.move(0, self.speed)
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()
			# init the available modules


def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("HACKER EMPIRE CAPTION RAIN")
	clock = pygame.time.Clock()
	group = pygame.sprite.Group()
	group_count = SCREEN_WIDTH / FONT_SIZE

	# mainloop
	while True:
		time = clock.tick(FREQUENCE)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
		screen.fill((0, 0, 0))
		for i in range(0, int(group_count)):
			group.add(Word((i * FONT_SIZE, FONT_SIZE)))
		group.update()
		group.draw(screen)

		pygame.display.update()

		# save pictures
		# global times
		# times += time
		# if times > 5000:
		# 	pygame.image.save(screen, str(randomname())+".png")


if __name__ == '__main__':
	main()		




