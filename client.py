"""
	Murmur
	~~~~~~

	Client
"""
import socket

from threading import Thread

from message_receiver import MessageReceiver, Message

class Client:
	"""
	Processes received messages from a server and sends messages to the server.
	"""
	def __init__(self, server_ip, process=print, port=None):
		"""
		Initializes the client.

		server_ip - the server's ip address.
		port - the reception port of the server and the clients on the channel.
		process - properly received messages are passed to this function.
		"""
		self.process = process
		self.receiver = MessageReceiver(port)
		self.server_ip = server_ip
		self.channel_port = port

		Thread(name="Client Listening Thread", 
			target=self.__process_messages, daemon=True).start()

	def __process_messages(self):
		"""
		Retrieves messages from a MessageReceiver object and passes it to the
		process function. Should be used in a daemon thread as it loops 
		forever.
		"""
		for received_message in self.receiver:
			if received_message.sender == self.server_ip or received_message.sender == 'local':
				self.process(received_message.body)

	def connect(self, username):
		"""
		Registers the client to the server. 

		username - this client's username
		"""
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((self.server_ip, self.channel_port))
			sock.send("/regi {}".format(username).encode())

	def send(self, message):
		"""
		Sends a message to the server.

		message - some string to send to the server.
		"""
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((self.server_ip, self.channel_port))

			sock.send(message.encode())
