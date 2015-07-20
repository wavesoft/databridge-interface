#!/usr/bin/env python
import json
from dirq.QueueSimple import QueueSimple

message = None

# Read message from disk
message_directory = '/var/messages/jobs'
dirq = QueueSimple(message_directory)

# Return queue details
print "Content-Type: application/json"
print
print "size=%i" % dirq.count()
