# responder.py
# 
# pinterestfeed2 - Pinterest RSS feed generator
# 
# Copyright (C) 2013 Thomas Jollans
#   This program is free software subject to the conditions of the AGPL,
#   version 3 or newer. For details, see README.md and AGPL.txt

from twisted.web.resource import Resource
from twisted.web import server
from functools import partial
import PyRSS2Gen

from updater import updater
from database import db

class TopLevel (Resource):
	def getChild (self, path, request):
		if path == 'favicon.ico':
			return None
		return UserFeed (path)

class FeedResource (Resource):

	children = []

	def render_GET (self, request):
		db.register_request (self._user)
		updater.update_if_necessary (self._user, self._board,
									 partial(self.output_feed, request))
		return server.NOT_DONE_YET

	def output_feed (self, request):
		if self._board is None:
			title = "{0} on Pinterest".format (self._user)
			link = "http://pinterest.com/{0}".format (self._user)
		else:
			title = "{0} by {1} on Pinterest".format (self._board, self._user)
			link = "http://pinterest.com/{0}/{1}".format (self._user, self._board)

		rss = PyRSS2Gen.RSS2 (
			title = title,
			link = link,
			description = "{0} (improved feed)".format(title),
			items = [
				PyRSS2Gen.RSSItem (
					title = p.caption,
					link = p.url,
					guid = p.url,
					pubDate = p.date,
					description = p.html
					)
				for p in db.get_pins (self._user, self._board)
				]
			)
		request.setHeader ('Content-Type', 'application/rss+xml')
		request.write (rss.to_xml (encoding='UTF-8'))
		request.finish ()


class UserFeed (FeedResource):
	def __init__ (self, user):
		self._user = user
		self._board = None

	def getChild (self, path, request):
		return BoardFeed (self._user, path)

class BoardFeed (FeedResource):
	isLeaf = True

	def __init__ (self, user, board):
		self._user = user
		self._board = board
