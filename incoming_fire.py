from Tkinter import *
import Image
import time
from threading import Thread
import math


class incoming_fire(object):
	def __init__(self, master,coord,unit_type):
		self.master = master
		# forbid moving
		if self.master.battle:
			self.master.movable_units = 0
		self.unit_type = unit_type
		self.coord = coord
		if self.master.battle:
			self.animate()
		else:
			self.master.take_turn()

	def load(self,file_name,sub):
		my_image_number = 0
		gif_animation = []
	        while True:
			try:
				frame = PhotoImage(file=file_name,format="gif -index {}".format(my_image_number)).subsample(sub)
			except TclError:
				#self.last_frame = my_image_number-1
				#self.my_image_number = 0
               			break
		        gif_animation.append(frame)
			my_image_number +=1  # number of next frame to read
		return gif_animation

	def animate(self):
		if self.unit_type == "scout":
			self.fire_animation = self.load("images/hot_fireball_flip.gif",sub = 2)
			self.damage = 30
		elif self.unit_type == "tank":
			self.fire_animation = self.load("images/cold_fireball1_flip.gif",sub = 2)
			self.damage = 50
		elif self.unit_type == "soldier":
			self.fire_animation = self.load("images/cold_fireball2_flip.gif",sub = 2)
			self.damage = 40
		else:
			self.fire_animation = self.load("images/hot_fireball_flip.gif",sub = 2)
			self.damage = 0

		self.fire_image_on_canvas = self.master.player_canvas.create_image((self.master.player_canvas.winfo_width(),self.coord[1]), image=self.fire_animation[0])
		self.fire_animation_image_number = 0
		#print >>sys.stderr, my_image_number
		t1 = Thread(target=self.shoot_animation)
		t1.start()

	def shoot_animation(self):
		border_reached = 0
		explosion = 0
		while not border_reached and not explosion:
	        # return to first image
		        if self.fire_animation_image_number >= len(self.fire_animation):
			        self.fire_animation_image_number = 0
			self.master.player_canvas.itemconfig(self.fire_image_on_canvas, image = self.fire_animation[self.fire_animation_image_number])
			self.master.player_canvas.move(self.fire_image_on_canvas, -10, 0)
			coords = self.master.player_canvas.coords(self.fire_image_on_canvas)
			# calculate distance to all units on canvas
			x1 = coords[0]
			y1 = coords[1]
			for i in self.master.units:
				x2 = i.coord[0]
				y2 = i.coord[1]
				dist = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
				#print >>sys.stderr, str(dist)
				if dist <= 50:
					explosion = 1
					self.explode((x1,y1))
					self.cause_damage(i)
			# if side reached
			if coords[0] <= 0:
				self.master.player_canvas.delete(self.fire_image_on_canvas)
				border_reached = 1
			#print >>sys.stderr, coords
	        	self.fire_animation_image_number += 1
			time.sleep(0.05)
		#allow units to move again
		self.master.movable_units = 1
		self.master.take_turn()

	def explode(self,crd):
		if self.unit_type == "scout":
			self.expl_animation = self.load("images/explosion1.gif",sub = 1)
		elif self.unit_type == "soldier":
			self.expl_animation = self.load("images/explosion2.gif",sub = 1)
		elif self.unit_type == "tank":
			self.expl_animation = self.load("images/explosion3.gif",sub = 1)
			# put explosion up
			(x,y) = crd
			crd = (x,y-80)
		else:
			self.expl_animation = self.load("images/explosion1.gif",sub = 1)
		self.expl_image_on_canvas = self.master.player_canvas.create_image(crd, image=self.expl_animation[0])
		self.expl_animation_image_number = 0
		self.run_gif(self.expl_animation)
		self.master.player_canvas.delete(self.fire_image_on_canvas)

	def run_gif(self, gif):
		#print >>sys.stderr, my_image_number
	        # return to first image
		stop = 0
	        if self.expl_animation_image_number >= len(gif)-1:
		        stop = 1
			self.expl_animation_image_number = 0
		self.master.player_canvas.itemconfig(self.expl_image_on_canvas, image = gif[self.expl_animation_image_number])
	        self.expl_animation_image_number += 1
		if not stop:		
			self.master.after(100, lambda: self.run_gif(gif,))
		else:
			self.master.player_canvas.delete(self.expl_image_on_canvas)

	def cause_damage(self, unit):
		if self.master.battle == 1:
			unit.health -= self.damage
			unit.update_health()
		


		

