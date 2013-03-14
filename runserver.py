# runserver.py
# 
# pinterestfeed2 - Pinterest RSS feed generator
# 
# Copyright (C) 2013 Thomas Jollans
#   This program is free software subject to the conditions of the AGPL,
#   version 3 or any later version. For details, see README.md and AGPL.txt

from twisted.web import server
from twisted.internet import reactor
from twisted.internet import task

from responder import TopLevel
from updater import updater

from config import PORT, \
				   PROBE_INTERVAL, \
				   LISTEN_ON

reactor.listenTCP (PORT, server.Site(TopLevel ()), interface=LISTEN_ON)

loop = task.LoopingCall (updater.update_what_needs_updating)
loop.start (PROBE_INTERVAL.seconds)

reactor.run()
