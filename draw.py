import pygame
from pygame.locals import *
import state as state1d
import time
import sys


def draw(surface, state):
	def conv(y, x):
		return (160-10*y, 50+10*x)

	def rect(y, x, c):
		#print('\trect', y, x)
		y, x = conv(y, x)
		pygame.draw.rect(surface, c, (x+1, y-1, 8, 8))

	def line(y0, x0, y1, x1, c):
		y0, x0 = conv(y0, x0)
		y1, x1 = conv(y1, x1)
		pygame.draw.line(surface, c, (x0+5, y0+5), (x1+5, y1+5), 4)

	for n in state.drawable:
		pos = n.pos
		y, x = pos.time, pos.space
		current = n
		while True:
			if isinstance(current, state1d.Vertex):
				if current.t == state1d.PLAYER:
					c = (0, 255, 0) 
				elif current.t == state1d.START:
					c = (0, 255, 255)
				else:
					c = (0, 0, 255)
				rect(y, x, c)
			else:
				y_old, x_old = y, x
				x += current.move
				y += current.dtime
				c = (127, 127, 127) if current.warp is None else (127, 0, 255)
				if any(current==s[0][0] for s in state.shifts):
					c = (255, 0, 0)
				line(y_old, x_old, y, x, c)

			if current.next is None:
				break
			current = current.next


if __name__ == '__main__':
	pygame.init()
	# Assign FPS a value
	FPS = 2
	FramePerSec = pygame.time.Clock()

	screen = pygame.display.set_mode((240,180))
	time.sleep(.3)

	WHITE = (255, 255, 255)
	BLUE = (0, 0, 255)

	#pygame.draw.line(screen, BLUE, (50, 60), (100, 110))
	#pygame.draw.line(screen, BLUE, (60, 60), (110, 110))
	posy = 100
	posx = 100

	state = state1d.State1D(10, 20)
	#moves = [0, 0, 1, 0, 1, 0, -1, -1, 1, 10, 1, 0, 0, 0, 0, 0, 0, 0, 0]
	moves = [0, 1, 0, 1, 0, 0, 0, 10, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
	count = 0

	# Beginning Game Loop
	while True:
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_UP]:
			posy -= 5
		if pressed_keys[K_DOWN]:
			posy += 5

		screen.fill(WHITE)
		if not pressed_keys[K_DOWN]:
			if count == 7:
				state.tick(0, warp=-7)
			elif count < len(moves):
				state.tick(moves[count])
			count += 1
		draw(screen, state)

		#pygame.draw.rect(screen, BLUE, (posx, posy, 15, 15))
	   
		FramePerSec.tick(FPS)