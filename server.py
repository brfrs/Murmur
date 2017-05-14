"""
	Murmur
	~~~~~~

	Server
"""
import socket
import re
import logging

from queue import Queue
from threading import Thread

from user_registry import UserRegistry
from message_receiver import MessageReceiver, Message

COMMAND_FLAG_CHAR = '/'

logger = logging.getLogger(__name__)

class Server:
	"""
	Murmur server.
	"""
	registry = UserRegistry()

	def __init__(self, port, ip, client_process):
		self.channel_port = port
		self.ip = ip

		self.client_process = client_process
		self.receiver = MessageReceiver(self.ip, self.channel_port)
		logger.info("Server initialized.")

	def start_processing(self):
		"""
		Starts the server for actual processing.
		"""
		logger.info("Server processing started.")
		Thread(name='Server Processing Thread', target=self.__process_requests,
			daemon=True).start()

	def __process_requests(self):
		"""
		Processes local and network messages. If it originates from a known
		client, it will try to parse the command or send it to everyone if it
		is not a command. If it originated from an unknown client it will try 
		to register them. 
		"""
		for received_message in self.receiver:
			if received_message.sender in self.registry.ip:
				logger.info("Message received from registered client.")
				if received_message.body.startswith(COMMAND_FLAG_CHAR):
					logger.debug("Message was a command.")
					self.parse(received_message.body)
				else:
					logger.debug("Message was generic.")
					self.send_to_all(received_message)
			else:
				logger.info("Message received from an unregistered client.")
				self.attempt_to_register(received_message)

	def parse(self, message: Message):
		"""
		Try to make sense out of a command sent to the server from a registered
		client.

		message - a message object
		"""
		pass

	def register_hosting_client(self, username: str):
		"""
		Registers the hosting client's username with the registry.

		username - a client's username
		"""
		if self.validate_name(username):
			self.registry.register(username, 'local')

	def attempt_to_register(self, message: Message):
		"""
		Called when a message is received from an unregistered client. Tries to
		match the sent message with the proper registration format.

		message - a Message object to parse.
		"""
		logger.info("Attempting to register client.")

		successful_parse = re.match(r'\/regi (.{1,30})', message.body)

		if successful_parse and self.validate_name(successful_parse.group(1)):
			logger.info("Client successfully registered.")
			self.registry.register(successful_parse.group(1), message.sender)
		else:
			logger.info("Client not registered") # Ignore the message

	def validate_name(self, username: str) -> bool:
		"""
		Checks to see if the username is valid.

		username - a string for the registering client's username
		"""
		return True

	def send(self, message_body: str, target: str):
		"""
		Sends a message to a client. If the message fails to send, the target
		is removed from the registry and presumed to be disconnected.

		target - the ip of the message recipient.
		message_body - a string to send the target.
		"""
		if target == 'local':
			self.client_process(message_body)
		else:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				try:
					sock.settimeout(1)
					sock.connect((target, self.channel_port))
					sock.send(message_body.encode())
				except socket.timeout:
					self.registry.delete_ip(target)

	def send_to_all(self, message: Message):
		"""
		Sends a message to all ips in the registry. Appends the username before
		sending the message.

		message - a message object
		"""
		to_send = self.registry.ip[message.sender] + ": " + message.body

		for ip in self.registry.ip:
			self.send(to_send, ip)

	def send_as_hosting_user(self, message_body: str):
		"""
		Sends a message under the server's registered user name.

		message_body - a string to send
		"""
		self.receiver.receive(Message(message_body, 'local'))
		