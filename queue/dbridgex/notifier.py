
import socket
import json

class UDPNotifier:
	"""
	A class that is used to broadcast UDP notifications to
	listening entities.
	"""

	def __init__(self):
		"""
		Initialize the UDP notifier class
		"""
		self.targets = []

		# Create a socket to use for sending the messages
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def removeAllTargets(self):
		"""
		Remove all targes
		"""
		self.targets = []

	def addTarget(self, machine):
		"""
		Include machine in the targets
		"""

		# Split machine to ip:port
		parts = machine.split(":")
		h_machine = parts[0]
		h_port = 19561

		# Get port
		if len(parts) > 1:
			h_port = int(parts[1])

		# Include machine/ip pair
		self.targets.append( (h_machine, h_port) )

	def notify(self, name, parameters={}):
		"""
		Send a notification to all targets
		"""

		# If we have no targets, exit
		if not self.targets:
			return

		# Calculate the mesage payload
		parameters['event'] = name
		message = json.dumps(parameters) + "\n"

		# Send message to all targets
		for t in self.targets:

			# Send message to target
			self.sock.sendto(message, t)

