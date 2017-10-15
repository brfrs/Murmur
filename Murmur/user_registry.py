"""
	Murmur
	~~~~~~

	User Registry
"""

class UserRegistry:
	"""
	Bi-directional dictionary for lookup between usernames and ips.
	"""
	def __init__(self):
		self.__user = {} # user -> ip
		self.__ip = {}   # ip -> user

	def register(self, new_user: str, new_ip: str):
		"""
		Add a new user to the registry.

		new_user - username of the new user
		new_ip - ip of the new user
		"""
		self.__user[new_user] = new_ip
		self.__ip[new_ip] = new_user

	def name_taken(self, username: str) -> bool:
		"""
		Checks if a username is taken.

		username - a name to be tested
		"""
		return username in self.__user

	def ip_known(self, ip: str) -> bool:
		"""
		Checks if the ip is in the registry.abs

		ip - an ip to be checked
		"""
		return ip in self.__ip

	def get_user(self, ip: str) -> str:
		"""
		Returns the username that an ip address is registered to.

		ip - a registered ip
		"""
		return self.__ip[ip]

	def get_ip(self, user: str) -> str:
		"""
		Returns the ip that a username is registered to.

		user - a registered username
		"""
		return self.__user[user]

	def ip(self):
		"""
		A generator expression that yields the ips in the registery.
		"""
		for ip in self.__ip.keys():
			yield ip

	def delete_user(self, key: str):
		"""
		Delete an element in the registry based on the key in user dict.

		key - a username to delete
		"""
		ip_to_del = self.__user[key]
		del self.__user[key]
		del self.__ip[ip_to_del]

	def delete_ip(self, key: str):
		"""
		Delete an element in the registry based on the key in ip dict.

		key - a ip to delete.
		"""
		user_to_del = self.__ip[key]
		del self.__ip[key]
		del self.__user[user_to_del]

	def rename_user(self, ip_addr: str, new_user: str):
		"""
		Renames a user already in the registry.

		ip_addr - ip of the user
		new_user - the user's new name
		"""
		if not self.name_taken(new_user):
			old_user = self.__ip[ip_addr]
			self.__ip[ip_addr] = new_user

			del self.__user[old_user]
			self.__user[new_user] = ip_addr