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

import json
import cPickle as pickle

from dbqueue.features import FeatureOffer, FeatureRequirement, FeatureMatcher, FeatureFormatError
from dbqueue.errors import QueueError

class DataBridgeQueue:
	"""
	Core class that implements the DataBridge queue
	"""

	def __init__(self, queueName, storeBackend, featureFactory=None):
		"""
		Initialize a DataBridge Queue interface
		"""

		# Keep local of properties
		self.queue = queueName
		self.backend = storeBackend
		self.featureFactory = featureFactory

		# Load persistent configuration
		self.config = storeBackend.get("config")
		if not self.config:
			self.config = {}
		else:
			self.config = json.loads(self.config)

	def config(self, parm, value=None):
		"""
		Set or Get a persistent configuration parameter
		"""

		# If value is not specified, return property
		if value is None:
			if not parm in self.config:
				return None
			return self.config[parm]

		# Update configuration property
		self.config[parm] = value
		self.backend.set("config", json.dumps(self.config))

	def push(self, jobid, feats=None):
		"""
		Push a job in the queue, optionally specifying
		additional run-time specifications such as JDL
		"""

		# Default queue id
		qid = "default"

		# If we have job feature specifications handle them now
		if (not feats is None) and (not self.featureFactory is None):

			# Create a feature requirement object from the request
			try:
				f_req = self.featureFactory.createRequirement(feats)
			except FeatureFormatError as e:
				raise QueueError("Could not add item on queue: %s" % str(e))

			# Get the feature domain, effectively meaning a unique string
			# that identifies the specified category
			qid = f_req.getID()

			# Store feature requirement in the store
			self.backend.set( "%s/feats/%s" % (self.queue, qid), pickle.dumps(f_req) )

			# Update the set of features
			self.backend.set_add( "%s/feats" % (self.queue,), qid )

		# According to feature priority add
		# in the head or in the tail of the queue
		self.backend.list_push( "%s/queue/%s" % (self.queue, qid), jobid )

	def pop(self, feats=None):
		"""
		Pop a job from the queue, that satisfies the features received
		by the worker node.
		"""

		# Default queue id
		qid = "default"

		# If we don't have feature specifications just get next item from default
		if (feats is None) or (self.featureFactory is None):

			# Get next item
			item = self.backend.list_pop( "%s/queue/%s" % (self.queue, qid) )
			if not item:
				return None

			# Return item
			return item

		# If we have client feature specifications handle them now
		else:

			# Create a feature offer object from the request
			try:
				f_offer = self.featureFactory.createOffer(feats)
			except FeatureFormatError as e:
				raise QueueError("Could not receive item on queue: %s" % str(e))

			# Create a feature matcher
			matcher = self.featureFactory.createMatcher( f_offer )

			# Load list of registered feature IDs
			feat_ids = self.backend.set_members( "%s/feats" % (self.queue,) )
			if feat_ids:

				# Iterate over all the registered feature requests				
				for qid in feat_ids:

					# Load FeatureRequirement object from store
					try:
						f_req = pickle.loads( self.backend.get( "%s/feats/%s" % (self.queue, qid) ) )
					except pickle.UnpicklingError:
						# Skip this problematic feature
						continue

					# Add a feature to cmpare against
					matcher.addRequirement( f_req )

			# Start fetching items from queue and if that
			# queue is emptied, cleanup and continue
			best = matcher.nextBestOffer()
			while best:

				# Get matcher ID
				qid = best.getID()

				# Get next item
				item = self.backend.list_pop( "%s/queue/%s" % (self.queue, qid) )
				if not item:

					# If there are no items, cleanup feature specifications
					# and ask for next best offer
					self.backend.remove( "%s/feats/%s" % (self.queue, qid) )
					self.backend.set_remove( "%s/feats" % (self.queue,), qid )

					# Get next offer
					best = matcher.nextBestOffer()
					continue

				# We got an item, return
				return item
