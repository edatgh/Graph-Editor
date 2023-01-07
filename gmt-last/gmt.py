#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

# Import all classes from my own modules
from graph import *



#################################################
# GGraph - Graphical Graph, wrapper for a graph #
#################################################
class GGraph:
	# Attributes
	pixmap    = None
	widget    = None
	red_gc    = None
	green_gc  = None
	white_gc  = None
	blue_gc   = None
	color_map = None
	red       = None
	green     = None
	blue      = None
	white     = None
	graph     = None
	m_down    = None
	seg_start = None
	seg_end   = None
	vertex    = None
	h_vert    = None
	s_vert    = None
	src_vert  = None
	old_end   = None

	def __init__(self, widget):
		self.widget = widget

		# Allocate all GC's, etc
		x, y, width, height = widget.get_allocation()
		self.pixmap = gtk.gdk.Pixmap(widget.window, width, height)
		self.pixmap.draw_rectangle(widget.get_style().white_gc, gtk.TRUE, 0, 0, width, height)
		self.color_map = self.pixmap.get_colormap()

		self.red   = self.color_map.alloc_color(65535, 0, 0, gtk.FALSE, gtk.TRUE)
		self.green = self.color_map.alloc_color(0, 65535, 0, gtk.FALSE, gtk.TRUE)
		self.blue  = self.color_map.alloc_color(0, 0, 65535, gtk.FALSE, gtk.TRUE)
		self.white = self.color_map.alloc_color(65535, 65535, 65535, gtk.FALSE, gtk.TRUE)

		self.red_gc = gtk.gdk.GC(self.pixmap, self.red, self.white, None, gtk.gdk.COPY,
					 gtk.gdk.SOLID, None, None, None, gtk.gdk.INCLUDE_INFERIORS,
					 0, 0, 0, 0, gtk.FALSE, 1, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND,
					 gtk.gdk.JOIN_ROUND)

		self.green_gc = gtk.gdk.GC(self.pixmap, self.green, self.white, None, gtk.gdk.COPY,
					   gtk.gdk.SOLID, None, None, None, gtk.gdk.INCLUDE_INFERIORS,
					   0, 0, 0, 0, gtk.FALSE, 1, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND,
					   gtk.gdk.JOIN_ROUND)

		self.blue_gc = gtk.gdk.GC(self.pixmap, self.blue, self.white, None, gtk.gdk.COPY,
					  gtk.gdk.SOLID, None, None, None, gtk.gdk.INCLUDE_INFERIORS,
					  0, 0, 0, 0, gtk.FALSE, 3, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND,
					  gtk.gdk.JOIN_ROUND)

		self.white_gc = gtk.gdk.GC(self.pixmap, self.white, self.white, None, gtk.gdk.COPY,
					   gtk.gdk.SOLID, None, None, None, gtk.gdk.INCLUDE_INFERIORS,
					   0, 0, 0, 0, gtk.FALSE, 3, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND,
					   gtk.gdk.JOIN_ROUND)

		self.widget.connect("expose_event", self.expose_event)
		self.widget.connect("motion_notify_event", self.motion_notify_event)
		self.widget.connect("button_press_event", self.button_press_event)
		self.widget.connect("button_release_event", self.button_release_event)

		self.graph = Graph(self)

	# Utility functions
	def draw_circle(self, x, y, r):
		self.pixmap.draw_arc(self.red_gc, gtk.FALSE, int(x - r), int(y - r), int(r * 2),
				     int(r * 2), 0, int(360 * 64))
		self.widget.queue_draw()

	def draw_h_circle(self, x, y, r):
		self.pixmap.draw_arc(self.blue_gc, gtk.FALSE, int(x - r), int(y - r), int(r * 2),
				     int(r * 2), 0, int(360 * 64))
		self.widget.queue_draw()

	def erase_circle(self, x, y, r):
		self.pixmap.draw_arc(self.white_gc, gtk.FALSE, int(x - r), int(y - r), int(r * 2),
				     int(r * 2), 0, int(360 * 64))
		self.widget.queue_draw()


	def draw_segment(self, x1, y1, x2, y2):
		self.pixmap.draw_line(self.green_gc, int(x1), int(y1), int(x2), int(y2))
		self.widget.queue_draw()

	def erase_segment(self, x1, y1, x2, y2):
		self.pixmap.draw_line(self.white_gc, int(x1), int(y1), int(x2), int(y2))
		self.widget.queue_draw()

	# Event handlers
	def expose_event(self, widget, event):
		self.graph.draw()
		x, y, width, height = event.area
		self.widget.window.draw_drawable(widget.get_style().fg_gc[gtk.STATE_NORMAL],
						 self.pixmap, x, y, x, y,
						 width, height)
		return gtk.FALSE

	def button_press_event(self, widget, event):
		if event.button == 1:
			self.m_down = event.button, event.x, event.y
			self.vertex = self.graph.get_vertex(event.x, event.y)
			if self.vertex is not None:
				self.old_end = self.vertex.x, self.vertex.y

		if event.button == 2:
			self.src_vert = self.graph.get_vertex(event.x, event.y)
			if (self.src_vert is None):
				return

			self.seg_start = event.x, event.y
			self.seg_end = None

		return gtk.TRUE

	def button_release_event(self, widget, event):
		if self.m_down is not None:
			if event.button == self.m_down[0] and event.x == self.m_down[1] and event.y == self.m_down[2]:
				self.graph.add_vertex(event.x, event.y)

		self.m_down = None

		if self.seg_start is not None and self.seg_end is not None:
			self.erase_segment(self.seg_start[0], self.seg_start[1],
					   self.seg_end[0], self.seg_end[1])
			vert = self.graph.get_vertex(self.seg_end[0], self.seg_end[1])
			if vert is not None:
				self.graph.link_vertices(self.src_vert, vert)
				vert.redraw()

		self.seg_start = None
		self.seg_end = None

		return gtk.TRUE

	def motion_notify_event(self, widget, event):
		if event.is_hint:
			x, y, state = event.window.get_pointer()
		else:
			x, y, state = event.x, event.y, event.state

		if state & gtk.gdk.BUTTON1_MASK and self.pixmap != None:
			if self.vertex is not None:
				self.vertex.move(x, y)
				self.graph.move_edges(self.old_end, x, y)
				self.old_end = x, y

		if state & gtk.gdk.BUTTON2_MASK and self.pixmap != None:
			if self.seg_end is not None and self.seg_start is not None:
				self.erase_segment(self.seg_start[0], self.seg_start[1],
						   self.seg_end[0], self.seg_end[1])
			self.seg_end = x, y

			if self.seg_start is not None:
				self.draw_segment(self.seg_start[0], self.seg_start[1],
						  x, y)

			vertex = self.graph.get_vertex(x, y)
			if vertex is None and self.h_vert is not None:
				self.h_vert.redraw()
				self.h_vert = None

			if vertex is not None and self.h_vert is not None and self.h_vert is not vertex:
				self.h_vert.redraw()
				self.h_vert = None

			if vertex is not None and vertex is not self.src_vert:
				vertex.highlight()
				self.h_vert = vertex

		return gtk.TRUE

	def on_save(self, widget, data=None):
		self.graph.save_to_file()

	def on_load(self, widget, data=None):
		self.graph.load_from_file()


#################
# main() - Main #
#################
def main():
	# Create main GMT window
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	window.set_name("Graph Manipulation Tool")

	# Create layout
	vbox = gtk.VBox(gtk.FALSE, 0)
	window.add(vbox);
	vbox.show()

	window.connect("destroy", lambda w: gtk.main_quit())

	# Create the drawing area
	drawing_area = gtk.DrawingArea()
	drawing_area.set_size_request(500, 500)
	vbox.pack_start(drawing_area, gtk.TRUE, gtk.TRUE, 0)

	drawing_area.set_events(gtk.gdk.EXPOSURE_MASK |
				gtk.gdk.LEAVE_NOTIFY_MASK |
				gtk.gdk.BUTTON_PRESS_MASK |
				gtk.gdk.BUTTON_RELEASE_MASK |
				gtk.gdk.POINTER_MOTION_MASK |
				gtk.gdk.POINTER_MOTION_HINT_MASK)

	# Quit button
	s_button = gtk.Button("Save")
	l_button = gtk.Button("Load")
	q_button = gtk.Button("Quit")

	vbox.pack_start(s_button, gtk.FALSE, gtk.FALSE, 0)
	vbox.pack_start(l_button, gtk.FALSE, gtk.FALSE, 0)
	vbox.pack_start(q_button, gtk.FALSE, gtk.FALSE, 0)

	q_button.connect_object("clicked", lambda w: w.destroy(), window)

	window.show_all()

	gg = GGraph(drawing_area)

        s_button.connect("clicked", gg.on_save)
        l_button.connect("clicked", gg.on_load)

	gtk.main()

	return 0



#######################
# Program entry point #
#######################
if __name__ == "__main__":
	main()
