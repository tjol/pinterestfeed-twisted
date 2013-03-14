# runserver.py

from twisted.web import server
from twisted.internet import reactor
from twisted.internet import task

from responder import TopLevel
from updater import updater

from config import PORT, \
				   PROBE_INTERVAL

reactor.listenTCP (PORT, server.Site(TopLevel ()))

loop = task.LoopingCall (updater.update_what_needs_updating)
loop.start (PROBE_INTERVAL.total_seconds ())

reactor.run()
