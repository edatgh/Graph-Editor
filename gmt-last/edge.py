#!/usr/bin/env python



class Edge:
	# Attributes
	x1 = None
	y1 = None
	x2 = None
	y2 = None
	g  = None

	def __init__(self, g, x1, y1, x2, y2):
		self.g  = g
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2



	def draw(self):
		self.g.draw_segment(self.x1, self.y1, self.x2, self.y2)

	def redraw(self):
		self.g.erase_segment(self.x1, self.y1, self.x2, self.y2)
		self.g.draw_segment(self.x1, self.y1, self.x2, self.y2)

	def move(self, x1, y1, x2, y2):
		self.g.erase_segment(self.x1, self.y1, self.x2, self.y2)
		self.g.draw_segment(self.x1, self.y1, self.x2, self.y2)
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

if __name__ == "__main__":
	print "Edge"
