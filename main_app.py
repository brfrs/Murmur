"""
	Murmur

	Main Application
"""

from tkinter import *

from interface import *

from server import Server
from client import Client

from network_functions import get_public_ip

class App:
	"""
	The main gui and logic of the program.
	"""
	def __init__(self, root=None):
		self.root = root
		self.root.resizable(False, False)
		self.root.configure(padx=10, pady=10, bg=DARK_BLUE)
		self.root.title("Murmur")
		
		self.current_frame = MainMenu(self.root, self.create_client_menu, self.create_server_menu)
		self.current_frame.grid()

	def create_server_menu(self):
		"""
		Replaces the current frame with a frame that holds a form about server
		options.
		"""
		self.replace_current_frame(CreateServerMenu(self.root, self.spawn_server))

	def create_client_menu(self):
		"""
		Replaces the current frame with a frame that holds a form about client 
		options.
		"""
		self.replace_current_frame(CreateClientMenu(self.root, self.spawn_client))

	def spawn_client(self, ip, port, username):
		"""
		Spawns a client with the given parameters. Will draw the client
		interface onto the screen as well.
		"""
		self.client_instance = Client(get_public_ip(), ip, print, port)
		self.replace_current_frame(ClientView(self.root, self.client_instance.send))
		
		self.client_instance.process = self.current_frame.write_to_screen
		self.client_instance.connect(username)

	def spawn_server(self, port, username):
		"""
		Spawns a server with the given parameters and replaces the current frame
		with a client view frame.
		"""
		self.server_instance = Server(port, get_public_ip(), print)
		
		self.replace_current_frame(ClientView(self.root, self.server_instance.send_as_hosting_user))
		self.server_instance.client_process = self.current_frame.write_to_screen
		self.server_instance.start_processing()

		self.server_instance.register_hosting_client(username)

	def replace_current_frame(self, new_frame):
		"""
		Clears the frame held in current_frame and replaces it with the
		frame in the argument.
		"""
		self.current_frame.grid_forget()
		self.current_frame.destroy()

		self.current_frame = new_frame
		self.current_frame.grid()