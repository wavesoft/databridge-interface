#!/usr/bin/env python
import json
from dirq.QueueSimple import QueueSimple

message = None

# Read message from disk
message_directory = '/var/messages/jobsout'
dirq = QueueSimple(message_directory)
for name in dirq:
    if not dirq.lock(name):
        continue
    message = dirq.get(name)
    dirq.remove(name)
    break

# Send response
if message:
    #body=json.loads(message)["body"]
    print "Content-Type: application/json"
    print
    print message
else:
    print "Status: 404 Not Found\n\n"

