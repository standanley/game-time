import pygame
import sys
from pygame.locals import *
import time



class State1D():

	# Node
	PLAYER = 0
	FIRE_UP = 4
	FIRE_DOWN = 5
	SHIFT_SEND = 6
	SHIFT_RECEIVE = 7
	START = 8
	PORTAL_LEAVE = 9
	PORTAL_ARRIVE = 10
	GHOST = 11

	# Edge
	'''
	STILL = 1	# |
	RIGHT = 2	# /
	LEFT = 3 	# \
	LEFT_FAIL = 12
	RIGHT_FAIL = 13
	'''

	class Pos():
		def __init__(self, space, time):
			self.space = space
			self.time = time

		def __getattr__(self, x):
			if x == 'i':
				return 10*self.time + self.space
			return super()

		def after(self):
			return State1D.Pos(self.space, self.time+1)

		def before(self):
			return State1D.Pos(self.space, self.time-1)

		def left(self):
			return State1D.Pos(self.space-1, self.time)

		def right(self):
			return State1D.Pos(self.space+1, self.time)

		def same(self):
			return State1D.Pos(self.space, self.time)




	class Edge():
		def __init__(self, move, p, n):
			self.move = move
			self.result = move

			assert p is not None
			assert n is not None

			self.prev = p
			self.next = n

	class Node():
		def __init__(self, t,p, n):
			self.t = t
			self.prev = p
			self.next = n


	def __init__(self, size, duration):
		self.lines = []
		self.active = []
		self.shifts = []
		self.grid = [None for _ in range(size*duration)]

		s = self.Node(self.START, None, None)
		player = self.Node(self.PLAYER, None, None)
		e = self.Edge(0, s, player)
		s.next = e
		player.prev = e

		s.pos = self.Pos(0, 0)
		player.pos = self.Pos(0, 1)

		self.lines.append(s) 
		self.active.append(player)

		self.grid[s.pos.i] = s
		#self.grid[player.pos.i] = player




	def tick(self, dir, warp = None):
		print('tick', dir)
		for a in (self.shifts + self.active):
			a.pos
			if a.t == self.PLAYER:
				# self.PLAYER moves forward in time
				if warp is not None:
					# new objects
					pl = self.Node(self.PORTAL_LEAVE, a.prev, None)
					pa = self.Node(self.PORTAL_ARRIVE, None, a)

					# fix connections
					a.prev.next = pl
					a.prev = pa
					pl.link = pa
					pa.link = pl

					# fix dicts
					pl.pos = a.pos.same()
					a.pos.time = warp
					pa.pos = a.pos.same()
					self.lines.append(pa)
					self.grid[pl.pos.i] = pl
					self.grid[pa.pos.i] = pa

				# regular movement
				current_index = a.pos.i
				a.pos.time += 1
				a.pos.space += dir

				in_space = self.grid[a.pos.i]
				if in_space is not None:
					print('COLLISION of type', in_space.t, 'in loc', a.pos.space, a.pos.time)
					# for now assume we are able to push it
					their_move = in_space.prev.move
					if dir == 0:
						# they crash into us, zero them out
						in_space.prev.result = 0
						r = self.Node(self.SHIFT_RECEIVE, in_space.next, None)
						s = self.Node(self.SHIFT_SEND, None, in_space.next.next)
						s.pos = a.pos.after()
						temp = a.pos.same()
						temp.space -= their_move
						temp.time += 2
						r.pos = temp

						s.link = r
						r.link = s
						in_space.next.next = r
						in_space.next.next.prev = s

						#self.lines.append(s)
						self.shifts.append(s)
						self.grid[r.pos.before().i] = in_space

					elif dir == 1:
						# we went right, for now assume they're to our right?
						pass

				g = self.Node(self.GHOST, a.prev, None)
				e = self.Edge(dir, g, a)
				g.next = e
				g.prev.next = g
				e.next.prev = e

				self.grid[current_index] = g

			elif a.t == self.SHIFT_SEND:
				print('PERFORMING SHIFT, sender:', a.pos.space, a.pos.time)
				s = a
				r = a.link
				g = a.next

				r.prev.next = g
				r.prev = g.next
				s.next = g.next.next
				g.next.next.prev = s

				self.grid[s.pos.i] = None
				temp = r.pos.same()
				temp.space += r.prev.result
				self.grid[temp.i] = g
				s.pos.time += 1



				#grid[]



	def draw(self, surface):
		#print('drawing')
		def conv(y, x):
			return (160-10*y, 50+10*x)
		def rect(y, x, c):
			#print('\trect', y, x)
			y, x = conv(y, x)
			pygame.draw.rect(surface, c, (x+1, y-1, 8, 8))
		def line(y0, x0, y1, x1):
			y0, x0 = conv(y0, x0)
			y1, x1 = conv(y1, x1)
			pygame.draw.line(surface, (127, 127, 127), (x0+5, y0+5), (x1+5, y1+5), 4)

		for n in self.lines:
			pos = n.pos
			y, x = pos.time, pos.space
			current = n
			while True:
				if isinstance(current, self.Node):
					rect(y, x, (0, 0, 255))
				else:
					y_old, x_old = y, x
					x += current.result
					y += 1
					line(y_old, x_old, y, x)

				if current.next is None:
					break
				current = current.next
				
			






def main():
    pygame.init()
    # Assign FPS a value
    FPS = 2
    FramePerSec = pygame.time.Clock()

    screen = pygame.display.set_mode((240,180))
    time.sleep(3)

    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    #pygame.draw.line(screen, BLUE, (50, 60), (100, 110))
    #pygame.draw.line(screen, BLUE, (60, 60), (110, 110))
    posy = 100
    posx = 100

    state = State1D(10, 20)
    #moves = [0, 0, 1, 0, 1, 0, -1, -1, 1, 10, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    moves = [0, 0, 1, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0]
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
        if count == 6:
        	state.tick(0, warp=1)
        elif count < len(moves):
        	state.tick(moves[count])
        count += 1
        state.draw(screen)

        #pygame.draw.rect(screen, BLUE, (posx, posy, 15, 15))
       
        FramePerSec.tick(FPS)


if __name__ == '__main__':
    main()