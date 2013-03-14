# runserver.py

from twisted.web import server
from twisted.internet import reactor

from responder import TopLevel

from config import PORT


reactor.listenTCP (PORT, server.Site(TopLevel ()))

reactor.run()
