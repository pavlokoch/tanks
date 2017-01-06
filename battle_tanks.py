# TODO: sometimes when press connect get error: Transport end point not connected
# cancel when waiting for connection or connecting
from Tkinter import *
import server
import client
from threading import Thread
#from multiprocessing.pool import ThreadPool
import time
import sys
import battle_field
import incoming_fire
import socket
import tkSimpleDialog

class Main_menu(Frame):
	
	def __init__(self, master):
		Frame.__init__(self,master)

		self.pack(expand=YES, fill=BOTH, pady = 20)
		self.create_widgets()
		self.data = 0
		self.sock = 0
		self.connection = 0
		self.Im_server = False

	def create_widgets(self):
		""" create server button """
		self.button_create_server = Button(self)
		self.button_create_server["text"] = "Create game"
		self.button_create_server.pack(pady=5)
		self.button_create_server.config( width = 10 )
		self.button_create_server["command"] = self.create_server
		""" connect button """
		self.button_connect = Button(self)
		self.button_connect["text"] = "Connect"
		self.button_connect.pack(pady=5)
		self.button_connect.config( width = 10 )
		self.button_connect["command"] = self.connect
		""" options button """
		self.button_options = Button(self)
		self.button_options["text"] = "Options"
		self.button_options.pack(pady=5)
		self.button_options.config( width = 10 )
		#self.button_options["command"] = self.options
		""" exit button """
		self.button_exit = Button(self)
		self.button_exit["text"] = "Exit"
		self.button_exit.pack(pady=5)
		self.button_exit.config( width = 10 )
		self.button_exit["command"] = self.exit
	
		# get to know my ip
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('gmail.com',80))
		self.my_ip = (s.getsockname()[0])
		s.close()
		""" display ip to connect to"""
		self.label = Label(self, text = self.my_ip)
		self.label.pack(pady = 5)


	def exit(self):
		# if still connected then disconnect first
		if self.sock:
			self.disconnect()
		# close programm
		sys.exit(0)

	def create_server(self):
		self.sock = server.create_server(self.my_ip)
		self.connection = server.wait_connection(self.sock)
		if self.connection:
			self.Im_server = True
			self.button_connect["text"] = "Disconnect"
			self.button_connect["command"] = self.disconnect
			self.button_create_server["text"] = "Cancel"
			self.button_create_server["command"] = self.disconnect
			#self.start_the_game
			# start main thread
			thread = Thread(target = self.start_the_game)
			thread.start()

	def kill_server(self):
		server.kill_server(self.connection)
		self.connection = 0

	def connect(self):
		ip = tkSimpleDialog.askstring("Connect to", "enter IP")
		self.sock = client.connect(ip)
		if self.sock > 0:
			self.Im_server = False
			self.button_connect["text"] = "Disconnect"
			self.button_connect["command"] = self.disconnect
			#self.start_the_game
			thread = Thread(target = self.start_the_game)
			thread.start()
			#self.button_create_server.grid_forget()
		else:
			print "No local server"
			self.exit()

	def send_message(self,message):
		if not self.Im_server and self.sock > 0:		
			client.send_message(self.sock,message)
		if self.Im_server and self.sock > 0:
			server.send_message(self.connection,message)

	def disconnect(self):
		self.send_message('disconnect')

	def re_init(self):
		self.data = 0
		self.sock = 0
		self.button_connect["text"] = "Connect"
		self.button_connect["command"] = self.connect
		self.button_create_server["text"] = "Create game"
		self.button_create_server["command"] = self.create_server

	def start_the_game(self):
		# create battle field
		self.field = battle_field.battle_field(self)
#		self.master.bind('<KeyPress>', onKeyPress)


		while self.sock:
			if self.Im_server:
				self.data = server.read_buffer(self.connection)
			else:
				self.data = client.read_buffer(self.sock)

			if self.data == 'disconnect':
				print >>sys.stderr, 'closing connection'
				# first inform opponent
				if self.Im_server:
					self.send_message('disconnect')
					# give time to client to disconnect
					time.sleep(0.6)
					server.kill_server(self.connection)
				else:
					client.disconnect(self.sock)
				# reinit 
				self.re_init()
				self.data = 0
				print >>sys.stderr, 'done'
				break
			
			if self.data == 'Hit!' or self.data == 'Kill!' or self.data == 'Miss':
				self.field.hit(self.data)
				self.data = 0
				continue

			if self.data > 0:
				print >>sys.stderr, 'received "%s"' % self.data
				x = 0
				y = 0
				try:
					x = int(self.data[0:self.data.find("_")])
					y = int(self.data[self.data.find("_")+1:self.data.find("X")])
					unit_type = self.data[self.data.find("X")+1:]
				except:
					pass
				if x and y:
					incoming_fire.incoming_fire(self.field,(x,y),unit_type)				
			time.sleep(0.5)

root = Tk()
root.title("Battle tanks")
root.geometry("200x220")
app = Main_menu(root)
root.mainloop()
