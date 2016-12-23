from Tkinter import *
import Image
import time
from threading import Thread
from random import randint

class unit(object):
	def __init__(self, master,coord,unit_type, unit_counter):
		self.master = master
		self.coord = coord
		self.unit_type = unit_type
		self.start_fire_coord = (0,0)
		# keep counter to delete when killed
		self.unit_counter = unit_counter
		self.show_health = False
		# health lines
		self.g_l = 0
		self.r_l = 0
		if unit_type == "scout":
			self.unit_animation = self.load("images/scout.gif",sub = 1)
			self.max_health = 200
		if unit_type == "soldier":
			self.unit_animation = self.load("images/soldier.gif",sub = 2)
			self.max_health = 100
		if unit_type == "tank":
			self.unit_animation = self.load("images/tank.gif",sub = 2)
			self.max_health = 100

		self.health = self.max_health
		self.unit_image_on_canvas = self.master.player_canvas.create_image(self.coord, image=self.unit_animation[0], tags = "token")
		self.unit_animation_image_number = 0
		self.run_gif(self.unit_animation)



	def run_gif(self, gif):
		#print >>sys.stderr, my_image_number
	        # return to first image
	        if self.unit_animation_image_number >= len(gif):
		        self.unit_animation_image_number = 0
		self.master.player_canvas.itemconfig(self.unit_image_on_canvas, image = gif[self.unit_animation_image_number])
		# show health bar
		if self.show_health and not self.g_l:
			# c1 - health bar begin
			# c2 - current health
			# c3 - end
			c1 = self.coord[0]
			c2 = c1 + float(self.health)/float(self.max_health) * 100.0
			c3 = c1 + 100
			# green line
			self.g_l = self.master.player_canvas.create_line(c1, self.coord[1], c2, self.coord[1], fill="green", width = 4)
			# red line
			self.r_l = self.master.player_canvas.create_line(c2, self.coord[1], c3, self.coord[1], fill="red", width = 4)
		elif not self.show_health:
			if self.g_l:
				self.master.player_canvas.delete(self.g_l)
				self.master.player_canvas.delete(self.r_l)
				self.g_l = 0
				self.r_l = 0
	        self.unit_animation_image_number += 1
		self.master.after(100, lambda: self.run_gif(gif))

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

	def fire(self):
		#print >>sys.stderr, self.unit_type
		if self.unit_type == "scout":
			self.fire_animation = self.load("images/hot_fireball.gif",sub = 2)
		if self.unit_type == "tank":
			self.fire_animation = self.load("images/cold_fireball1.gif",sub = 2)
		if self.unit_type == "soldier":
			self.fire_animation = self.load("images/cold_fireball2.gif",sub = 2)

		self.fire_image_on_canvas = self.master.player_canvas.create_image(self.start_fire_coord, image=self.fire_animation[0])
		self.fire_animation_image_number = 0
		#print >>sys.stderr, my_image_number
		t1 = Thread(target=self.shoot_animation)
		t1.start()

	def shoot_animation(self):
		border_reached = 0
		# block movements
		self.master.movable_units = 0
		while not border_reached:
	        # return to first image
		        if self.fire_animation_image_number >= len(self.fire_animation):
			        self.fire_animation_image_number = 0
			self.master.player_canvas.itemconfig(self.fire_image_on_canvas, image = self.fire_animation[self.fire_animation_image_number])
			self.master.player_canvas.move(self.fire_image_on_canvas, 10, 0)
			coords = self.master.player_canvas.coords(self.fire_image_on_canvas)
			# if side reached
			if coords:
				if coords[0] >= self.master.player_canvas.winfo_width():
					self.master.player_canvas.delete(self.fire_image_on_canvas)
					border_reached = 1
			#print >>sys.stderr, coords
	        	self.fire_animation_image_number += 1
			time.sleep(0.05)
	
	def update_health(self):
		print >>sys.stderr, self.health/self.max_health
		if self.health <= 0:
			self.master.player_canvas.delete(self.unit_image_on_canvas)
			# delete unit from list
			j = 0
			for i in self.master.units:
				if i.unit_counter == self.unit_counter:
					del self.master.units[j]
					break
				j += 1
		else:
			# soldier teloporting
			if self.unit_type == "soldier":
				new_coord = (randint(100,self.master.player_canvas.winfo_width()-100),randint(100,self.master.player_canvas.winfo_height()-100))
				self.master.player_canvas.move(self.unit_image_on_canvas, new_coord[0] - self.coord[0],new_coord[1] - self.coord[1])
				# update coordinates
				self.coord = new_coord
			# stop moving if damaged except for scouts
			if self.unit_type != "scout":
				self.master.player_canvas.itemconfig(self.unit_image_on_canvas, tags = "damaged")

	def identify(self,num):
		if self.unit_image_on_canvas == num:
			return self
		else:
			return 0








