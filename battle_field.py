from Tkinter import *
#import spritesheet
from random import randint
from unit import unit
import time
from threading import Thread

class battle_field(Frame):
	def __init__(self, master):
		Frame.__init__(self,master)
		self.top=top=Toplevel(master,width = 400,height = 800, background="white")
		self.init_field()

	def init_field(self):
		#self.field = Toplevel(Frame,width = 400,height = 800, background="white")
		#field.wm_title("Battle field")
		self.unit_counter = 0
		# free mode
		self.free_mode = 1
		# battle_mode
		self.battle = 0
		# allow units to move
		self.movable_units = 1
		# save current coords for hit/kill message
		self.cur_coord = (0,0)	
		
		self.units_label = LabelFrame(self.top, text="Units", padx=5, pady=5, background="white")
		self.units_label.pack(fill = Y, side=RIGHT ,padx=10, pady=10)

		self.player_label = LabelFrame(self.top, text="Battle Field", padx=5, pady=5, background="white")
		self.player_label.pack(fill = BOTH, padx=10, pady=10)

	        # create units canvas
	        #self.units_canvas = Canvas(self.units_label,width=200, height=800, background="white")
	        #self.units_canvas.pack(fill=Y, expand=True)

	        # create player canvas
	        self.player_canvas = Canvas(self.player_label,width=400, height=800, background="white")
	        self.player_canvas.pack(fill="both", expand=True)

		# create unit buttons
		""" create scout button """
		self.button_scout = Button(self.units_label)
		self.scout_image = PhotoImage(file="images/scout.gif").subsample(1)
		self.button_scout["image"] = self.scout_image
		self.button_scout.pack(pady=5, fill=X)
		self.button_scout["command"] = lambda: self._create_unit((randint(50,self.player_label.winfo_width()-50),randint(100,self.player_label.winfo_height())-100),"scout")
		""" create soldier button """
		self.button_soldier = Button(self.units_label)
		self.soldier_image = PhotoImage(file="images/soldier.gif").subsample(2)
		self.button_soldier["image"] = self.soldier_image
		self.button_soldier.pack(pady=5, fill=X)
		self.button_soldier["command"] = lambda: self._create_unit((randint(50,self.player_label.winfo_width()-50),randint(100,self.player_label.winfo_height())-100),"soldier")
		""" create tank button """
		self.button_tank = Button(self.units_label)
		self.tank_image = PhotoImage(file="images/tank.gif").subsample(2)
		self.button_tank["image"] = self.tank_image
		self.button_tank.pack(pady=5, fill=X)
		self.button_tank["command"] = lambda: self._create_unit((randint(50,self.player_label.winfo_width()-50),randint(100,self.player_label.winfo_height())-100),"tank")
		


	        # this data is used to keep track of an 
	        # item being dragged
	        self._drag_data = {"x": 0, "y": 0, "item": None}
		# to keep images
		self.images = []
		self.units = []

	        # add bindings for clicking, dragging and releasing over
	        # any object with the "token" tag
	        self.player_canvas.tag_bind("token", "<ButtonPress-3>", self.OnTokenButtonPress3)
	        self.player_canvas.tag_bind("token", "<ButtonRelease-3>", self.OnTokenButtonRelease3)
	        self.player_canvas.tag_bind("token", "<B3-Motion>", self.OnTokenMotion3)
		# left click to shoot
	        self.player_canvas.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress1)
	        self.player_canvas.tag_bind("damaged", "<ButtonPress-1>", self.OnTokenButtonPress1)

		# decide which turn
		if self.master.Im_server:
			self.take_turn()
		else:
			self.next_turn()


		self.top.bind('<KeyPress>', self.onKeyPress)
		self.top.bind('<KeyRelease>', self.onKeyRelease)
	
	def onKeyPress(self,event):
		if event.keysym == "Shift_L":
			for u in self.units:
				u.show_health = True
	def onKeyRelease(self,event):
		if event.keysym == "Shift_L":
			for u in self.units:
				u.show_health = False

	def _create_unit(self, coord, unit_type):
	        '''Create a token at the given coordinate in the given color'''
		self.unit_counter += 1
		self.units.append(unit(self,coord,unit_type, self.unit_counter))
		if self.unit_counter >= 5:
			self.free_mode = 0
			self.battle = 1
			# hide units panel
			self.units_label.pack_forget()
		#print >>sys.stderr, self.units[-1].health

	def OnTokenButtonPress3(self, event):
	        '''Being drag of an object'''
		if self.movable_units:
			self.being_drag = 1
		        # record the item and its location
			self._drag_data["item"] = self.player_canvas.find_closest(event.x, event.y)[0]
		        self._drag_data["x"] = event.x
		        self._drag_data["y"] = event.y


	def OnTokenButtonRelease3(self, event):
	        '''End drag of an object'''
		if self.movable_units and self.being_drag:
		        # reset the drag information
		        self._drag_data["item"] = None
		        self._drag_data["x"] = 0
		        self._drag_data["y"] = 0
			idf = self.player_canvas.find_closest(event.x, event.y)[0]
			# identify the clicked object
			for i in self.units:
				unit = i.identify(idf)
				if unit:
					break
			# if unit found
			if unit:
				# update unit coordinates
				unit.coord = (event.x, event.y)
			self.being_drag = 0


	def OnTokenMotion3(self, event):
	        '''Handle dragging of an object'''
		if self.movable_units and self.being_drag:
		        # compute how much this object has moved
		        delta_x = event.x - self._drag_data["x"]
		        delta_y = event.y - self._drag_data["y"]
		        # move the object the appropriate amount
		        self.player_canvas.move(self._drag_data["item"], delta_x, delta_y)
		        # record the new position
		        self._drag_data["x"] = event.x
		        self._drag_data["y"] = event.y

	def OnTokenButtonPress1(self, event):
		#print >>sys.stderr, self.player_canvas.find_closest(event.x, event.y)[0]  
		if not self.battle:
			self.free_mode = 0
			self.battle = 1
			# hide units panel
			self.units_label.pack_forget()
		if self.my_turn:
			unit = 0			
			idf = self.player_canvas.find_closest(event.x, event.y)[0]
			# identify the clicked object
			tag = self.player_canvas.gettags(idf)[0]
			if tag == "token" or tag == "damaged":
				for i in self.units:
					unit = i.identify(idf)
					if unit:
						break
			# if unit found
			if unit:
				# save coord for hit/fill message
				self.cur_coord = (event.x,event.y)
				# start fure animation
				unit.start_fire_coord = (event.x,event.y)
				t1 = Thread(target=unit.fire())
				t1.start()
				t1.join()
				# path coord for starting fire from this location
				self.master.send_message(str(event.x)+"_"+str(event.y)+"X"+str(unit.unit_type));		
			else:
				print >>sys.stderr, "bad unit"
			# next turn
			self.next_turn()

	def take_turn(self):
		self.my_turn = True
		self.player_label["background"] = "green"

	def next_turn(self):
		self.my_turn = False
		self.player_label["background"] = "red"

	def hit(self,message):
		msg = self.player_canvas.create_text(self.cur_coord[0],self.cur_coord[1],fill="red",font="Times 40 bold",
                        text=message)
		time.sleep(1)
		self.player_canvas.delete(msg)



