"""
	Murmur
	~~~~~~

	Client
"""
import socket
import logging

from threading import Thread

from message_receiver import MessageReceiver, Message

logger = logging.getLogger(__name__)

class Client:
	"""
	Processes received messages from a server and sends messages to the server.
	"""
	def __init__(self, client_ip, server_ip, process, port=None):
		"""
		Initializes the client.

		server_ip - the server's ip address.
		port - the reception port of the server and the clients on the channel.
		process - properly received messages are passed to this function.
		"""
		logger.info("Client initialized.")
		self.process = process
		self.receiver = MessageReceiver(client_ip, port)

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
		logger.info("Starting to process messages.")
		for received_message in self.receiver:
			logger.info("Message received.")
			
			if received_message.sender == self.server_ip or received_message.sender == 'local':
				self.process(received_message.body)

	def connect(self, username):
		"""
		Registers the client to the server. 

		username - this client's username
		"""
		logger.info("Trying to connect to the server.")
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((self.server_ip, self.channel_port))
			sock.send("/regi {}".format(username).encode())

	def send(self, message):
		"""
		Sends a message to the server.

		message - some string to send to the server.
		"""
		logger.info("Sending a message.")
		logger.debug("Message: " + message)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((self.server_ip, self.channel_port))

			sock.send(message.encode())
			logger.debug("Message successfully sent.")
