#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()
import os, sys
from dirq.QueueSimple import QueueSimple 

message_directory = '/var/messages/jobsout'

if os.environ['REQUEST_METHOD'] == 'PUT':
    form = cgi.FieldStorage()
    for param in form.keys():
        if not form[param].file:
            continue
        name = form[param].filename
        value = form[param].value
        dirq = QueueSimple(message_directory)
        name = dirq.add(value)

print "Content-Type: text/html\n"

