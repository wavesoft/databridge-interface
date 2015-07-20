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

from __future__ import absolute_import

import redis
from dbqueue.store import StoreBase

class REDISStore(StoreBase):
	"""
	REDIS Implementation of the databridge back-end store
	"""

	def __init__(self, **config):
		"""
		Configure REDIS Store
		"""

		# Open a strict REDIS connector
		self.redis = redis.StrictRedis(
			host=config.get("host", "localhost"),
			port=config.get("port", 6379),
			db=config.get("db", 0),
			password=config.get("password", None),
			connection_pool=config.get("connection_pool", None)
		)

		# Check for a key perfix
		self.prefix = config.get("prefix","")

	def get(self, key):
		"""
		Return the value of the specified key
		"""
		return self.redis.get(self.prefix+key)

	def set(self, key, value):
		"""
		Update the value of the specified key
		"""
		return self.redis.set(self.prefix+key, value)

	def remove(self, key):
		"""
		Remove a specified key from the database
		"""
		return self.redis.delete(self.prefix+key)

	def set_add(self, key, value):
		"""
		Add an item in a set of unique items
		"""
		return self.redis.sadd(self.prefix+key, value)

	def set_remove(self, key, value):
		"""
		Remove an item in a set of unique items
		"""
		return self.redis.srem(self.prefix+key, value)

	def set_members(self, key):
		"""
		Return the items of a unique set of items
		"""
		return self.redis.smembers(self.prefix+key)

	def list_push(self, key, value, priority=0):
		"""
		Set a value to the specified key

		We can use sorted sets in REDIS to implement priorities
		as it's meant to be, however for now just treat each
		priority request as the 'highest'.
		"""

		if not priority:
			return self.redis.rpush(self.prefix+key, value)
		else:
			return self.redis.lpush(self.prefix+key, value)

	def list_pop(self, key):
		"""
		Pop a value from the FIFO list under the specified key
		"""
		return self.redis.lpop(self.prefix+key)
