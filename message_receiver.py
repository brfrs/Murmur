"""
	Murmur
	~~~~~~

	Message Receiver
"""

import socket
import logging

from threading import Thread
from queue import Queue
from collections import namedtuple

SHORT_TIME_OUT = 3.0
MAX_BUFFER_SIZE = 4096

Message = namedtuple("Message", "body sender")

logger = logging.getLogger(__name__)

class MessageReceiver:
	"""
	A object to manage messages sent to a Murmer client or server. Messages
	should be retrieved by using this object as a generator expression
	"""
	message_queue = Queue()

	def __init__(self, ip: str, port=None):
		"""
		Sets up and starts the receiver for listening. Takes the port as
		a parameter. The port should be the same for all clients and servers.

		port - the receiving port for the listening socket.
		"""
		logger.info("Starting a message receiver")

		self.ip = ip
		
		if port is not None:
			logger.info("Message receiver is connected to the network.")
			self.channel_port = port

			Thread(name="Listening Thread", target=self.__receive_messages, 
				daemon=True).start()

	def __iter__(self) -> Message:
		"""
		Generator that produces messages from the message queue.

		returns a Message tuple
		"""
		while True:
			yield self.message_queue.get()

	def receive(self, new_message: Message):
		"""
		Puts a message on the message queue.

		message - a Message tuple
		"""
		if not isinstance(new_message, Message):
			logger.warn("A non-message object was passed to the receiver.")
			raise ValueError

		logger.info("A message was passed to the message receiver.")
		logger.debug("Body: '{}', Sender: {}".format(*new_message))

		self.message_queue.put(new_message)

	def __receive_messages(self):
		"""
		Take a message from a network connection and put it on the message
		queue.
		"""
		logger.info("Attempting to bind the socket to the channel port.")
		listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(SHORT_TIME_OUT)

		listening_sock.bind((self.ip, self.channel_port)) # TODO FIX THIS
		listening_sock.listen(5)

		logger.info("Socket bound successfully.")

		while True:
			try:
				client_sock, client_addr = listening_sock.accept()
				body = client_sock.recv(MAX_BUFFER_SIZE).decode()
				
				logger.info("Message received from the network.")

				self.receive(Message(body, client_addr[0]))

			except socket.timeout:
				logger.debug("Connection from remote host timed-out")
