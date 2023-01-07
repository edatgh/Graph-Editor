#!/usr/bin/env python



class Vertex:
	RADIUS = 3

	# attributes
	g       = None # graphic facilities
	x       = None
	y       = None
	links   = []
	c_links = []

	def __init__(self, g, x, y):
		self.g = g
		self.x = x
		self.y = y

		self.draw()

	def draw(self):
		self.g.draw_circle(self.x, self.y, self.RADIUS)

	def redraw(self):
		self.g.erase_circle(self.x, self.y, self.RADIUS)
		self.g.draw_circle(self.x, self.y, self.RADIUS)

	def highlight(self):
		self.g.draw_h_circle(self.x, self.y, self.RADIUS)

	def move(self, new_x, new_y):
		self.g.erase_circle(self.x, self.y, self.RADIUS)
		self.g.draw_circle(new_x, new_y, self.RADIUS)
		self.x = new_x
		self.y = new_y

	def inside(self, x, y):
		if (x - self.x) ** 2 + (y - self.y) ** 2 <= self.RADIUS ** 2:
			return 1
		else:
			return 0

	def add_link(self, vertex):
		self.links.append(vertex)

	def remove_link(self, vertex):
		self.links.remove(vertex)

if __name__ == "__main__":
	print "Vertex"
