#!/usr/bin/env python

from edge import *
from vertex import *

class Graph:
	# attributes
	name     = None
	g        = None
	vertices = []
	edges    = []



	def __init__(self, g, name = None):
		self.name = name
		self.g = g

	def add_vertex(self, x, y):
		self.vertices.append(Vertex(self.g, x, y))

	def get_vertex(self, x, y):
		for i in range(len(self.vertices)):
			if self.vertices[i].inside(x, y):
				return self.vertices[i]

		return None

	def remove_vertex(vertex):
		self.vertices.remove(vertex)

	def link_vertices(self, src_vertex, dest_vertex):
		src_vertex.add_link(dest_vertex)
		self.edges.append(Edge(self.g, src_vertex.x, src_vertex.y, dest_vertex.x, dest_vertex.y))

	def draw(self):
		for i in range(len(self.vertices)):
			self.vertices[i].draw()

		for i in range(len(self.edges)):
			self.edges[i].draw()

	def move_edges(self, old_end, x, y):
		if old_end is None:
			return

		ox, oy = old_end

		for i in range(len(self.edges)):
			self.g.erase_segment(self.edges[i].x1, self.edges[i].y1,
					     self.edges[i].x2, self.edges[i].y2)
			if self.edges[i].x1 == ox and self.edges[i].y1 == oy:
				self.edges[i].x1 = x
				self.edges[i].y1 = y

			if self.edges[i].x2 == ox and self.edges[i].y2 == oy:
				self.edges[i].x2 = x
				self.edges[i].y2 = y

			self.edges[i].redraw()

	def save_to_file(self, filename = None):
		if filename is None:
			filename = "graph.save"

		try:
			f = open(filename, "w")
		except:
			print "Unable to open file: ", filename
			return

		nr_vert = len(self.vertices)
		f.write(str(int(nr_vert)) + "\n")

		for i in range(nr_vert):
			f.write(str(int(self.vertices[i].x)) + "\n")
			f.write(str(int(self.vertices[i].y)) + "\n")
			nr_links = len(self.vertices[i].links)
			f.write(str(int(nr_links)) + "\n")
			for j in range(nr_links):
				f.write(str(int(self.vertices[i].links[j].x)) + "\n")
				f.write(str(int(self.vertices[i].links[j].y)) + "\n")

		f.close()

	def load_from_file(self, filename = None):
		if filename is None:
			filename = "graph.save"

		try:
			f = open(filename, "r")
		except:
			print "Unable to open file: ", filename
			return

		nr_vert = int(f.readline())

		for i in range(nr_vert):
			x = int(f.readline())
			y = int(f.readline())
			self.add_vertex(x, y)
			v = self.get_vertex(x, y)
			nr_links = int(f.readline())
			for j in range(nr_links):
				lx = int(f.readline())
				ly = int(f.readline())
				t = lx, ly
				v.c_links.append(t)

		f.close()

		for i in range(nr_vert):
			for j in range(len(self.vertices[i].c_links)):
				x, y = self.vertices[i].c_links[j]
				v = self.get_vertex(x, y)
				self.link_vertices(self.vertices[i], v)

if __name__ == "__main__":
	print "Graph"
