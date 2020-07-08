
class Pos():
	X = None
	def __init__(self, space, time):
		self.space = space
		self.time = time

	def __getattr__(self, x):
		if x == 'i':
			return self.X*self.time + self.space
		return super()

	def copy(self, dspace, dtime):
		return Pos(self.space + dspace, self.time + dtime)

	def move(self, dspace, dtime):
		self.space += dspace
		self.time += dtime

	def __str__(self):
		return f'<{self.space}, {self.time}>'

class Edge():
	def __init__(self, prev, next, strength, dspace, dtime=1):
		self.prev = prev
		self.next = next
		self.strength = strength
		self.dspace = dspace
		self.dtime = dtime

		if self.prev is not None:
			self.prev.next = self
		if self.next is not None:
			self.next.prev = self

class Vertex():
	def __init__(self, pos, player=False):
		self.pos = pos
		self.player = player

#class Player():
#	def __init__(self, pos):
		self.pos = pos



class State1D():
	def __init__(self, x, time, ptime):
		Pos.X = x

		self.grid = [[None for _ in range(x*time)] for _ in range(ptime)]
		self.starts = [None for _ in range(ptime)]
		self.drawables = [[] for _ in range(ptime)]
		self.fire_forward = [None for _ in range(ptime)]
		self.fire_backward = [None for _ in range(ptime)]
		self.x = x
		self.time = time
		self.ptime = ptime
		self.pt = 0

		g = self.grid[self.pt]
		s = Vertex(Pos(4, 0))
		p = Vertex(Pos(4, 1), True)
		e = Edge(s, p, self.pt, 0)
		#s.next = e
		#p.prev = e
		g[s.pos.i] = s
		g[p.pos.i] = p
		self.starts[self.pt] = s
		self.drawables[self.pt].append(s)
		self.fire_backward[self.pt] = set()
		self.fire_forward[self.pt] = set()

	def tick(self, dspace, dtime=1):



		g_old = self.grid[self.pt]
		s_old = self.starts[self.pt]
		fb_old = self.fire_backward[self.pt]
		ff_old = self.fire_forward[self.pt]
		drawables_old = self.drawables[self.pt]


		self.pt += 1
		# TODO grid should be initialied fresh I think
		g = self.grid[self.pt]
		self.fire_backward[self.pt] = set()
		self.fire_forward[self.pt] = set()
		self.drawables[self.pt] = set()
		fb = self.fire_backward[self.pt]
		ff = self.fire_forward[self.pt]
		drawables = self.drawables[self.pt]



		def push(v, dir, strength):
			# vertex v is feeling a push
			assert dir == -1 or dir == 1

			# does v resist?
			if v.prev.strength > strength:
				return False

			# does v have a neighbor who can resist?
			n = g[v.pos.copy(dir, 0).i]
			if n is not None:
				if not push(n, dir, strength):
					return False

			# if we had a neighbor, they have vacated
			assert g[v.pos.copy(dir, 0).i] == None

			# we have been pushed
			g[v.pos.i] = None
			v.pos.move(dir, 0)
			g[v.pos.i] = v
			return True

		# copy all non-portal things into the same spot, next time

		vs_by_time = [[] for _ in range(self.time)]

		# v_prev -> e -> v
		# In the end, we expect v.pos = v_prev_old.pos + e_old
		# TODO other drawables?
		
		s = Vertex(s_old.pos)
		g[s.pos.i] = s
		self.starts[self.pt] = s
		self.drawables[self.pt].append(s)
		v_prev = s
		v_prev_old = s_old
		e_old = v_prev_old.next

		while True:
			v = Vertex(v_prev_old.pos.copy(0, e_old.dtime))
			vs_by_time[v.pos.time].append(v)
			e = Edge(v_prev, v, e_old.strength, e_old.dspace, e_old.dtime)
			#v_prev.next = e
			#v.prev = e

			if e.dtime == 1:
				assert g[v.pos.i] == None
				g[v.pos.i] = v

			v_prev = v
			v_prev_old = e_old.next
			if v_prev_old.player:
				# TODO this is duplicated code
				v = Vertex(v_prev_old.pos.copy(0, dtime), True)
				vs_by_time[v.pos.time].append(v)
				e = Edge(v_prev, v, self.pt, dspace, dtime)
				if dtime == 1:
					g[v.pos.i] = v
				break

			e_old = v_prev_old.next
		

		for x in self.drawables[self.pt]:
			print('drawable', x)

		'''
		# propagate fire
		for e in self.fire_backward[self.pt - 1]:
			v_dead = e.prev
			e_ignite = v_dead.prev
			e_ignite.next = None

			v_dead.
		'''




		# let all movement happen
		portal_arrivals = [[] for _ in range(self.time)]
		for t in range(self.time):
			vs = vs_by_time[t]
			# go through all the vs at this time and push them
			# note we MUST do these high to low strength; we never want a high
			# strength that hasn't moved yet blocking a low strength
			def sort_key(v):
				if v.prev is None:
					# should only happen for start node
					assert self.starts[self.pt] == v
					return 0
				return -1 * v.prev.strength

			vs.sort(key=sort_key)
			for v in vs:
				# start node can't be moved
				if v == s:
					continue
				e = v.prev

				# don't bother with portal arrivals right now
				if e.dtime != 1:
					portal_arrivals[t].append(v)
					continue

				if v.pos.time == 5:
					print('looking at time 5')
					print(v, v.pos, v.prev.strength)

				dir = e.dspace
				if dir == 0:
					# if we've been pushed, it was necessarily by a higher strength
					continue
				n = g[v.pos.copy(dir, 0).i]

				if n is None or push(n, dir, e.strength):
					assert g[v.pos.copy(dir, 0).i] is None
					g[v.pos.i] = None
					v.pos.move(dir, 0)
					g[v.pos.i] = v

		# do portal stuff
		for t in range(self.time):
			for v in portal_arrivals[t]:
				assert v.prev.dspace == 0

				print('Infor for portal stuff:')
				print(v.prev.prev.pos, v.pos)
				print(v.prev.dspace, v.prev.dtime)
				print(v)

				assert v.prev.dtime != 1

				if g[v.pos.i] != None:
					print('FAILED PORTAL!')
					# portal arrival vertex is destroyed,
					# edges on either side catch fire
					e_prev = v.prev
					e_next = v.next
					e_prev.next = None
					fire_backward.add(e_prev)
					e_next.prev = None
					fire_forward.add(e_next)
					# we shold be good to garbage collect v now

				else:
					g[v.pos.i] = v




		self.check()


	def check(self):
		# run through grid and check all
		for pt in range(self.ptime):
			#print('Checking pt', pt)
			g = self.grid[pt]

			for i in range(len(g)):
				if g[i] is None:
					continue
				v = g[i]

				assert v.pos.space >= 0
				assert v.pos.i == i
				assert (v == self.starts[pt]) or (v.prev.next == v)
				assert v.player or (v.next.prev == v)

			# run through drawables and check all
			for base in self.drawables[pt]:
				n = base
				while True:
					if type(n) == Vertex:
						#print('about to check grid for ', n, 'at', n.pos, 'find', g[n.pos.i].pos)
						assert (g[n.pos.i] == n)
						assert n.player or (n.next.prev == n)
					else:
						assert n.next.prev == n
						assert n.prev.pos.time + n.dtime == n.next.pos.time
						#assert n.prev.pos.space + n.move == n.next.pos.space

					if getattr(n, 'player', False) or (n.next == base):
						break
					n = n.next
