
PLAYER = 0
FIRE_UP = 4
FIRE_DOWN = 5
SHIFT_SEND = 6
SHIFT_RECEIVE = 7
START = 8
#PORTAL_LEAVE = 9
#PORTAL_ARRIVE = 10
GHOST = 11

class Pos():
	def __init__(self, space, time):
		self.space = space
		self.time = time

	def __getattr__(self, x):
		if x == 'i':
			return 10*self.time + self.space
		return super()

	def copy(self, dspace, dtime):
		return Pos(self.space + dspace, self.time + dtime)

	def move(self, dspace, dtime):
		self.space += dspace
		self.time += dtime

	def __str__(self):
		return f'<{self.space}, {self.time}>'

class Edge():
	def __init__(self, dir, prev, next, strength, warp=None):
		self.dir = dir
		self.move = dir
		self.prev = prev
		self.next = next
		self.warp = warp
		self.dtime = warp if warp else 1
		self.strength = strength

class Vertex():
	def __init__(self, pos, t):
		self.pos = pos
		self.t = t
		self.prev = None
		self.next = None
		self.contact_left = None
		self.contact_right = None

class State1D():
	def __init__(self, space, time):
		self.grid = [None for _ in range(space*time)]
		self.drawable = []
		# a "shift" is a reference to an edge that is nonsensical now;
		# it should be fixed and the weirdness propogated to the next edge
		self.next_cycle_updates = [set() for _ in range(time)]
		self.age = 0

		start = Vertex(Pos(0, 0), START, 0)
		player = Vertex(Pos(0, 1), PLAYER, None)
		edge = Edge(0, start, player, self.age)
		start.next = edge
		player.prev = edge

		self.grid[start.pos.i] = start
		self.drawable.append(start)

		self.player = player


	def tick(self, dir, warp = None):
		def push(v, dir, strength, pusher):
			# vertex v is feeling a push
			assert dir == -1 or dir == 1
			if dir == -1:
				v.contact_right = pusher
				pusher.contact_left = v
			elif dir == 1:
				v.contact_left = pusher
				pusher.contact_right = v

			# does v resist?
			if v.prev.strength > strength:
				# I work out
				v.prev.pushing = pusher.prev
				return False

			# does v have a neighbor who can resist?
			n = self.grid[v.pos.copy(dir, 0).i]
			if n is not None:
				if push(n, dir, strength):
					v.pushing = n # I think this is redundant
					pusher.pushing = v
				else:
					v.pushing = v
					v.pushng = pusher
					return False

			# if we had a neighbor, they have vacated
			assert self.grid[v.pos.copy(dir, 0).i] == None

			# we have been pushed
			self.grid[v.pos.i] = None
			v.pos.move(dir, 0)
			self.grid[v.pos.i] = v
			v.prev.move += dir
			v.next.move -= dir
			# I don't think it's our job to update next_cycle_updates ?
			#self.next_cycle_updates.add([v.next])
			return True

	TODO things can walk through each other
	# can we go easily?
	# if we are trying to cross another
	#	?
	# 


	# TODO: I don't think I need this method at all!
	# difficult physics case: everybody is pushing for the middle spot:
	# __97532468_
	# _9753_2468_
	# we see left will win and take the spot, while right stays put
	# but now imagine a new player with strength 1 appears in that spot going right
	# we have to reevaluate everyone!
	# Solution: maybe give edges an effective strength, where that 3 has E.S. of 9?
	# effective strength should get reset when pusher does
	def place_vertex(v):
		# looks at previous move and places this vertex accordingly
		# assumes there is no entry for this vertex in the grid
		# will push things out of the way to make room if possible
		# does not touch v.next

		v.contact_left = None
		v.contact_right = None

		edge = v.prev
		goal_spot = edge.prev.pos.copy(edge.dir, edge.dtime)
		n = self.grid[goal_spot.i]

		if n is not None and n.prev.warp is not None:
			print('BAD WARP to', goal_spot)
			# TODO: remove it from grid

		if n is None:
			# check for crossing
			if crossing:
				pass
			else:
				# plain sailing
				v.pos = goal_spot
		else:
			# somebody is in our spot
			push_dir = dir if dir != 0 else -1 * n.prev.move
			if push(n, push_dir, edge.strength, v):
				# we get our way by force
				assert self.grid[goal_spot.i] is None
				v.pos = goal_spot
			else:
				# we couldn't resist, but are we pushed against something?
				new_push_dir = push_dir * -1
				new_goal_spot = goal_spot.copy(new_push_dir, 0)
				new_n = self.grid[new_goal_spot.i]
				if new_n is None:
					# not pushed against anything
					v.pos = new_goal_spot
				else:
					# more pushing!
					# we are pushing against new_n, but with the strength of n
					if push(new_n, new_push_dir, n.prev.strength, v):
						# our original neighbor wins!
						v.pos = new_goal_spot
					else:
						# all things considered, our neighbor should not have won the push
						# we should push it back with our new_neighbor's strength
						WAIT!





		if edge.dir == 0:

			if n is None:
				# plain sailing
				v.pos = goal_spot
			else:
				# somebody moved into our spot!
				if n.prev.warp is not None:
					print('BAD WARP to', goal_spot)
					# TODO what if that warp also gets moved this tick?
					# perhaps we should only flag it for now??
				else:
					# shoving contest
					if push(n, -1*n.prev.dir, edge.strength):
						# we hold against their shove
						assert self.grid[goal_spot.i] is None
						v.pos = goal_spot
					else:
						# we get shoved
						TODO are we squished between things?
						v.pos = goal_spot.shift(n.move, 0)
		else:
			# we are trying to move
			if n is None:
				# are we trying to pass though someone?

				v.pos = goal_spot


		edge.move = v.pos.space - edge.prev.pos.space
		self.grid[v.pos.i] = v





		n = self.grid(edge.prev.pos.copy(0, 1))
		if n is not None:
			# someone else would be in that spot


		# n is in the space we are about to occupy
		n = self.grid(edge.prev.pos.copy(self.dir, 1))
		if n is not None:
			if dir == 0:
				print('Someone warped into our spot!')
			if not push(n, edge.dir, edge.strength):
				# we don't get to move like we want



			'''
		TODO:
		an object can push on another object if it wants to occupy the same spot
		It passes in a strength determined by its previous edge
		The pushee then returns success or failure about being pushed with that strength
			If it does get pushed, it might hit another object and recursively call
			If not pushed, just return False
			If pushed, update the grid and your previous and next edges, probably register a shift
			'''

			'''
		def create_shift(edge, shift):
			# Introduce weirdness into this edge so it is wrong
			# by a distance of shift, and that weirdness will propogate
			assert shift != 0
			edge.move += shift
			edge.next.pos.move(shift, 0)
			edge.next.next.move -= shift

			s = [edge.next.next]
			self.shifts.append(s)
			'''

		'''
		def perform_shift(s):
			# Fix weirdness in this edge and propogate it to the next one
			edge = s[0]
			self.grid[edge.next.i] = None
			place_vertex(edge.next)
			next_edge = edge.next.next
			next_edge.move = next_edge.next.pos.space - next_edge.prev.pos.space
			self.next_cycle_updates.add(next_edge)


			TODO check over the rest of this functino
			shift = edge.dir - edge.move
			edge.move += shift
			self.grid[edge.next.pos.i] = None
			edge.next.pos.move(shift, 0)

			self.grid[edge.next.pos.i] = edge.next
			edge.next.next.move -= shift
			s[0][0] = edge.next.next
		'''

		def mark_next_update(e):
			TODO e.prev or e.next? think about warps
			us = next_cycle_updates[e.prev.pos.time]
			if v in us:
				return
			else:
				next_cycle_updates[e.prev.pos.time].add(v)
				for v in 

		def apply_move(e):
			# Assuming this vertex is in place and hasn't tried moving,
			# try moving
			# Update grid and abc
			v = e.next
			goal_pos = v.dir.copy(e.dir, 0)
			n = self.grid[goal_pos.i]
			if n is None:
				e.move = e.dir


			push()


		update = self.next_cycle_updates
		self.next_cycle_updates = [set() for _ in self.next_cycle_updates]
		for time, u in reversed(enumerate(update)):
			# remove old version of placed vertex

			for e in u:
				self.grid[e.next.pos.i] = None

			# place vertices with no movement
			for e in u:
				self.grid[e.prev.pos.copy(0, 1)]
				e.move = 0

			# vertices try to move and can push each other
			# TODO sort by strength high to low I think
			for e in u:
				place(e.next)
				next_edge = e.next.next
				TODO next few lines
				next_edge.move = next_edge.next.pos.space - next_edge.prev.pos.space
				if next_edge.move != next_edge.dir:
					mark_next_update(next_edge)
		
		# player
		p = self.player
		g = Vertex(p.pos.copy(0, 0), GHOST, self.age)
		e = Edge(dir, g, p, warp)
		p.prev.next = g
		g.prev = p.prev
		g.next = e
		p.prev = e
		p.pos.move(dir, e.dtime)

		c = self.grid[p.pos.i]
		if c:
			# collision!
			if dir == 0:
				# they crashed into us
				create_shift(c.prev, -1)
			else:
				assert False

		self.grid[g.pos.i] = g

		self.age += 1
		self.check()
		print('Player pos:', p.pos)


	def draw(self, surface):
		pass

	def check(self):
		# run through grid and check all
		for i in range(len(self.grid)):
			if self.grid[i] is None:
				continue
			v = self.grid[i]

			assert v.pos.i == i
			assert (v.t == START) or (v.prev.next == v)
			assert (v.t == PLAYER) or (v.next.prev == v)

		# run through drawables and check all
		for base in self.drawable:
			n = base
			while True:
				if type(n) == Vertex:
					print('about to check grid for ', n.t, 'at', n.pos)
					assert (n.t == PLAYER) or (self.grid[n.pos.i] == n)
					assert(n.t == PLAYER) or (n.next.prev == n)
				else:
					assert n.next.prev == n
					assert n.prev.pos.time + n.dtime == n.next.pos.time
					assert n.prev.pos.space + n.move == n.next.pos.space

				if (n.next == None) or (n.next == base):
					break
				n = n.next


if __name__ == '__main__':
	state = State1D(10, 15)
	state.check()

	state.tick(0)



