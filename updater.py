# updater.py

from twisted.web import client
from functools import partial

import pins
from database import db

from config import PINS_TTL, \
				   AUTORELOAD_AFTER, \
				   IGNORE_AFTER

class Updater (object):
	def __init__(self):
		pass

	def is_up_to_date (self, user, board=None, ttl=PINS_TTL):
		return db.did_update_within (PINS_TTL, user, board)	

	def update_now (self, user, board=None, cb=None):
		if board is None:
			FeedUpdater (user).load_feed (cb)
		else:
			FeedUpdater (user, board).load_feed (
				partial (self.update_if_necessary, user, None, cb))

	def update_if_necessary (self, user, board=None, cb=None):
		if self.is_up_to_date (user, board):
			if cb is not None:
				cb ()
		else:
			self.update_now (user, board, cb)


class FeedUpdater (object):
	_active_updaters = {}

	def __init__ (self, user, board=None):
		if board is None:
			self.source_url = 'http://pinterest.com/{0}/feed.rss'.format (user)
		else:
			self.source_url = 'http://pinterest.com/{0}/{1}/rss'.format (user, board)
		self.user = user
		self.board = board

	def load_feed (self, cb):
		if self.source_url in self._active_updaters:
			self._active_updaters[self.source_url]._callbacks.append (cb)
		else:
			self._callbacks = [cb]
			self._active_updaters[self.source_url] = self
			client.getPage (self.source_url).addCallback (self._load_rss)

	def _load_rss (self, rss):
		self._pin_wait_count = 0
		mypins = []

		# get count first
		for pin in pins.get_pins_from_rss (rss):
			self._pin_wait_count += 1
			mypins.append (pin)

		# then go out and load stuff.
		for pin in mypins:
			pin.load (self._pin_loaded)

	def _pin_loaded (self, pin):
		self._pin_wait_count -= 1

		if self._pin_wait_count == 0:
			# DONE !!
			for cb in self._callbacks:
				if cb is not None:
					cb ()
			# inform the troops
			db.register_update (self.user, self.board)


updater = Updater ()
