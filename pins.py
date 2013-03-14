# pins.py
# 
# pinterestfeed2 - Pinterest RSS feed generator
# 
# Copyright (C) 2013 Thomas Jollans
#   This program is free software subject to the conditions of the AGPL,
#   version 3 or newer. For details, see README.md and AGPL.txt

import feedparser
from twisted.web.client import getPage
from BeautifulSoup import BeautifulSoup
import re
from email.utils import parsedate_tz, mktime_tz
from datetime import datetime

from database import db

class Pin (object):
	"""Represents a Pinterest pinned item"""

	def __init__ (self, url, date):
		self.url = url
		self.date = date
		self._loaded = False


	def load (self, callback):
		if self._loaded:
			callback (self)
		else:
			self._loaded_cb = callback
			try:
				self._load_from_db ()
			except Exception, e:
				self._load_by_scraping ()

	def _load_from_db (self):
		db_info = db.get_pin (self.url)
		self.populate (db_info)
		self._loaded_cb (self)

	def populate (self, db_info):
		self.date = db_info['date']
		self.user = db_info['user']
		self.board = db_info['board']
		self.img_url = db_info['img']
		self.caption = db_info['caption']
		self.source = db_info['source']

		self._loaded = True

	def _save_to_db (self):
		db.save_pin (self.url, self.date, self.user, self.board,
					 self.img_url, self.caption, self.source)

	def _load_by_scraping (self):
		getPage (str(self.url)).addCallback (self._load_from_html)

	def _load_from_html (self, html):
		soup = BeautifulSoup (html, convertEntities=BeautifulSoup.HTML_ENTITIES)

		self._get_image_from_soup (soup)
		self._get_caption_from_soup (soup)
		self._get_board_from_soup (soup)
		self._get_source_from_soup (soup)

		self._get_better_image ()
		self._loaded = True
		try:
			self._save_to_db ()
		except:
			pass
		self._loaded_cb (self)


	def _get_image_from_soup (self, soup):
		img_url_elem = soup.find ('meta', {'property': 'og:image'})
		if img_url_elem:
			# We have the url!
			self.img_url = img_url_elem['content']

	def _get_caption_from_soup (self, soup):
		caption_elem = soup.find ('meta', {'property': 'og:description'})
		if caption_elem:
			self.caption = caption_elem['content']

	def _get_source_from_soup (self, soup):
		source_elem = soup.find ('meta', {'property': 'pinterestapp:source'})
		if source_elem:
			self.source = source_elem['content']

	def _get_board_from_soup (self, soup):
		board_meta_elem = soup.find ('meta', {'property': 'pinterestapp:pinboard'})
		if board_meta_elem:
			board_url = board_meta_elem['content']
			m = re.match (r'^.*pinterest\.com/([^/]+)/([^/]+)/?$', board_url)
			self.user = m.group (1)
			self.board = m.group (2)


	def _get_better_image (self):
		# If Pinterest are using the URL format as of March '13, we might
		# be able to find a higher res image than previously presented.
		if self.img_url and '/550x/' in self.img_url:
			self.img_url = self.img_url.replace ('/550x/', '/736x/')

	@property
	def html (self):
		return ( u'''<p><a href="{0}"><img src="{1}" alt="{2}"></a></a>'''
				 .format (self.url, self.img_url, unicode(self.caption, 'UTF-8', 'replace')))


def get_pins_from_rss (rss):
	"""argument: RSS code"""
	orig = feedparser.parse (rss)
	for item in orig.entries:
		date = datetime.fromtimestamp (mktime_tz (parsedate_tz (item.date)))
		yield Pin (item.link, date)
