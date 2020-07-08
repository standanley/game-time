import pygame
from pygame.locals import *
import state_v2 as state1d
import time
import sys


def draw(surface, state):
	def conv(y, x):
		return (340-10*y, 50+10*x)

	def rect(y, x, c):
		#print('\trect', y, x)
		y, x = conv(y, x)
		pygame.draw.rect(surface, c, (x+1, y-1, 8, 8))

	def line(y0, x0, y1, x1, c):
		y0, x0 = conv(y0, x0)
		y1, x1 = conv(y1, x1)
		pygame.draw.line(surface, c, (x0+5, y0+5-2), (x1+5, y1+5-2), 4)

	print('\nGonna draw')
	for n in state.drawables[state.pt]:
		print('starting with', n, n.pos)
		pos = n.pos
		#y, x = pos.time, pos.space
		current = n
		while True:

			if isinstance(current, state1d.Vertex):
				y, x = current.pos.time, current.pos.space
				if current.player:
					c = (0, 255, 0) 
				elif current == state.starts[state.pt]:
					c = (0, 255, 255)
				else:
					c = (0, 0, 255)
				rect(y, x, c)
			else:
				y_old, x_old = y, x
				x += current.dspace
				y += current.dtime
				c = (127, 127, 127) if current.dtime == 1 else (127, 0, 255)
				if current.prev.pos.space + current.dspace != current.next.pos.space:
					c = (255, 0, 0)
				line(y_old, x_old, y, x, c)

			if not hasattr(current, 'next'):
				break
			current = current.next


if __name__ == '__main__':
	pygame.init()
	# Assign FPS a value
	FPS = 5
	FramePerSec = pygame.time.Clock()

	screen = pygame.display.set_mode((480,360))
	time.sleep(.3)

	WHITE = (255, 255, 255)
	BLUE = (0, 0, 255)

	#pygame.draw.line(screen, BLUE, (50, 60), (100, 110))
	#pygame.draw.line(screen, BLUE, (60, 60), (110, 110))
	posy = 100
	posx = 100

	state = state1d.State1D(10, 40, 100)
	#moves = [0, 1, 0, 1, 0, 0, 0, -7, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, -7, 0, 0, 0, 0, 0]
	moves = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, -16, -1, 1, 1, 15, -1, -1, -1, -1, -12, 0, 1, -1, -1, 0, 0, 0, 0]
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
			if abs(moves[count]) > 1:
				state.tick(0, dtime=moves[count])
			elif count < len(moves):
				state.tick(moves[count])
			count += 1
		draw(screen, state)

		#pygame.draw.rect(screen, BLUE, (posx, posy, 15, 15))
	   
		FramePerSec.tick(FPS)