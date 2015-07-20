#!/usr/bin/env python
import json
from dirq.QueueSimple import QueueSimple

# Read message from disk
message_directory = '/var/messages/jobsout'
dirq = QueueSimple(message_directory)

# Return queue details
print "Content-Type: application/x-yaml"
print
print "size: %i" % dirq.count()
