#
# DataBridge-X Queue Implementation
# Copyright (C) 2014-2015  Ioannis Charalampidis, PH-SFT, CERN

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

class StoreBase:
	"""
	Base class for a DataBridge store back-end
	"""

	def get(self, key):
		"""
		Return the value of the specified key
		"""
		raise NotImplementedError("Command not implemented")

	def set(self, key, value):
		"""
		Set a value to the specified key
		"""
		raise NotImplementedError("Command not implemented")

	def remove(self, key):
		"""
		Remove a specified key from the database
		"""
		raise NotImplementedError("Command not implemented")

	def list_push(self, key, value, priority=0):
		"""
		Push a value in the FIFO list under the specified key

		Optionally, if the underlaying store supports it, the
		items in the queue must be sorted according to priority.
		Higher priority items have more changes to be pop'ed.
		"""
		raise NotImplementedError("Command not implemented")

	def list_pop(self, key):
		"""
		Pop a value from the FIFO list under the specified key
		"""
		raise NotImplementedError("Command not implemented")

	def set_add(self, key, value):
		"""
		Add an item in a set of unique items
		"""
		raise NotImplementedError("Command not implemented")

	def set_remove(self, key, value):
		"""
		Remove an item in a set of unique items
		"""
		raise NotImplementedError("Command not implemented")

	def set_members(self, key):
		"""
		Return the items of a unique set of items
		"""
		raise NotImplementedError("Command not implemented")
