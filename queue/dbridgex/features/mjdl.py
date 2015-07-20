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

from dbridgex.features import FeatureRequirement, FeatureOffer, FeatureMatcher, FeatureFactory

"""
MJDL Is a *very* simplistic Job-Description-Language (micro-JDL) specification
that is used just for testing some of the features of DataBridge-X.

In principle MJDL offers only matching in the following levels:

 * `platform` 	: Platform (None matches any platform)
 * `memory` 	: Minimum memory requirements (None removes this limitation)
 * `priority` 	: The priority of this job. The higher, the more preferred.

"""

def package_in_list(packageRequirement, packageOfferList):
	"""
	Check if a versioned package requirement is found
	in the package offer list
	"""
	return packageRequirement in packageOfferList

class MJDLRequirement(FeatureRequirement):
	"""
	An MJDL Requirement specification
	"""

	def __init__(self, features):
		"""
		Initialize the requirements
		"""

		# Expose properties according to features received
		self.platform = features.get("platform", None)
		self.memory = features.get("memory", None)
		self.freeMemory = features.get("freeMemory", None)
		self.swap = features.get("swap", None)
		self.freeSwap = features.get("freeSwap", None)
		self.packages = features.get("packages", None)

		# Priority is a dimention only used by the matcher
		self.priority = features.get("priority", 0)

	def getID(self):
		"""
		Calculate a unique ID with the offer specifications that we have
		"""

		# Stringify packages
		pkgs_str = ""
		if self.packages:
			pkgs_str = "".join(self.packages)

		# Prefix with 'mjdl'
		nid = "mjdl" + \
			":%s" % str(self.platform) + \
			":%s" % str(self.memory) + \
			":%s" % str(self.freeMemory) + \
			":%s" % str(self.swap) + \
			":%s" % str(self.freeSwap) + \
			":%s" % pkgs_str + \
			":%s" % str(self.priority)

		# Return index
		return nid


class MJDLOffer(FeatureOffer):
	"""
	An MJDL Offer specification
	"""

	def __init__(self, features):
		"""
		Initialize the requirements
		"""

		# Expose properties according to features received
		self.platform = features.get("platform", None)
		self.memory = features.get("memory", None)
		self.freeMemory = features.get("freeMemory", None)
		self.swap = features.get("swap", None)
		self.freeSwap = features.get("freeSwap", None)
		self.packages = features.get("packages", None)

	def getDescription(self):
		"""
		Return offer description (as a dictionary or as a string)
		that is used by the notification targets to identify the
		kind of offers that come from the clients.
		"""

		return {
			"matcher": "mjdl",
			"platform": self.platform,
			"memory": self.memory,
			"freeMemory": self.freeMemory,
			"swap": self.swap,
			"freeSwap": self.freeSwap,
			"packages": self.packages,
		}

class MJDLMatcher(FeatureMatcher):
	"""
	An MJDL matcher
	"""

	def __init__(self, offer):
		"""
		Initialize a matcher
		"""
		self.offer = offer
		self.matchedRequirements = []

	def addRequirement(self, req):
		"""
		Add a requirement to the process
		"""

		# Check if exact parameters met
		if not (req.platform is None) and (req.platform != self.offer.platform):
			return

		# Check if minimum parameters are met
		if not (req.memory is None) and (int(self.offer.memory) < int(req.memory)):
			return
		if not (req.freeMemory is None) and (int(self.offer.freeMemory) < int(req.freeMemory)):
			return
		if not (req.swap is None) and (int(self.offer.swap) < int(req.swap)):
			return
		if not (req.freeSwap is None) and (int(self.offer.freeSwap) < int(req.freeSwap)):
			return

		# Check if all packages are in there
		if not (req.packages is None):
			# Require 'packages' in the offer
			if not self.offer.packages:
				return
			# If at least one package from offer fails, return
			for pkg in req.packages:
				if not package_in_list(pkg, self.offer.packages):
					return

		# Store item in list and sort by priority
		self.matchedRequirements.append( req )

		# Sort
		self.matchedRequirements = sorted(self.matchedRequirements, 
			key=lambda x: x.priority, reverse=True)

	def nextBestOffer(self):
		"""
		Return the next best offer that mathes the specified requirements
		"""

		# If we don't have any other item left return None
		if not self.matchedRequirements:
			return None

		# Pop next item
		return self.matchedRequirements.pop(0)


class MJDLFactory(FeatureFactory):
	"""
	Factory that creates the specifications and matcher
	class for the Micro-JDL syntax.
	"""

	def createRequirement(self, reqDesc):
		"""
		Create an instance to FeatureRequirement
		"""
		return MJDLRequirement(reqDesc)

	def createOffer(self, offerDesc):
		"""
		Create an instance to FeatureOffer
		"""
		return MJDLOffer(offerDesc)

	def createMatcher(self, offerDesc):
		"""
		Create an MJDL Feature Matcher
		"""
		return MJDLMatcher(offerDesc)
