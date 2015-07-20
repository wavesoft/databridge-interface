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


class FeatureFormatError(Exception):
	"""
	The feature description was not in an understandable format
	"""
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class FeatureRequirement:
	"""
	A feature requirement exposed by the server
	"""

	def __init__(self, feats):
		"""
		Initialize a feature reqeust
		"""
		self.feats = feats

	def getID(self):
		"""
		Return the indexing ID for this feature request.
		"""
		raise NotImplementedError("Command not implemented")

class FeatureOffer:
	"""
	A feature offer received from the agent
	"""

	def __init__(self, feats):
		"""
		Initialize a feature offer
		"""
		self.feats = feats

	def getDescription(self):
		"""
		Return offer description (as a dictionary or as a string)
		that is used by the notification targets to identify the
		kind of offers that come from the clients.
		"""
		raise NotImplementedError("Command not implemented")

class FeatureMatcher:
	"""
	A feature matching class
	"""

	def __init__(self, offer):
		"""
		Initialize a feature matcher for the specified offer
		"""
		self.offer = offer

	def addRequirement(self, req):
		"""
		Add a requirement to the process
		"""
		raise NotImplementedError("Command not implemented")

	def nextBestOffer(self):
		"""
		Return the next best offer that mathes the specified requirements
		"""
		raise NotImplementedError("Command not implemented")

class FeatureFactory:
	"""
	Feature matcher factory is responsible for creating
	the appropriate feature matching class
	"""

	def createRequirement(self, reqDesc):
		"""
		Create an instance to FeatureRequirement
		"""
		raise NotImplementedError("Command not implemented")

	def createOffer(self, offerDesc):
		"""
		Create an instance to FeatureOffer
		"""
		raise NotImplementedError("Command not implemented")

	def createMatcher(self, offerDesc):
		"""
		Create an instance of FeatureMatcher
		"""
		raise NotImplementedError("Command not implemented")

