"""
	Murmur
	~~~~~~

	User Registry
"""

class UserRegistry:
	"""
	Bi-directional dictionary for lookup between usernames and ips.
	"""
	user = {} # user -> ip
	ip = {}   # ip -> user

	def register(self, new_user, new_ip):
		"""
		Add a new user to the registry.

		new_user - username of the new user
		new_ip - ip of the new user
		"""
		self.user[new_user] = new_ip
		self.ip[new_ip] = new_user

	def delete_user(self, key):
		"""
		Delete an element in the registry based on the key in user dict.

		key - a username to delete
		"""
		ip_to_del = self.user[key]
		del self.user[key]
		del self.ip[ip_to_del]

	def delete_ip(self, key):
		"""
		Delete an element in the registry based on the key in ip dict.

		key - a ip to delete.
		"""
		user_to_del = self.ip[key]
		del self.ip[key]
		del self.user[user_to_del]

	def rename_user(self, ip_addr, new_user):
		"""
		Renames a user already in the registry.

		ip_addr - ip of the user
		new_user - the user's new name
		"""
		old_user = self.ip[ip_addr]
		self.ip[ip_addr] = new_user

		del self.user[old_user]
		self.user[new_user] = ip_addr
