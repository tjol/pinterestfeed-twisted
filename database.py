# database.py

from datetime import datetime
import calendar

from config import DATABASE_TYPE, \
				   FEED_LENGTH

_QUERIES = {
	'sqlite3': {
		'get_pin':
			r'''SELECT "date", "user", "board", "img", "caption", "source" ''' +
			r'''FROM "pins" WHERE "url"=?''',
		'save_pin':
			r'''INSERT INTO "pins" ''' + 
			r'''("url", "date", "user", "board", "img", "caption", "source") ''' +
			r'''VALUES (?, ?, ?, ?, ?, ?, ?)''',
		'updates_since':
			r'''SELECT "time" FROM "updates" ''' +
			r'''WHERE "user" = ? AND "board" IS NULL AND DATETIME("time") >= DATETIME(?)''',
		'updates_board':
			r'''SELECT "time" FROM "updates" ''' +
			r'''WHERE "user" = ? AND "board" = ?''',
		'get_user_pins':
			r'''SELECT "url", "date", "user", "board", "img", "caption", "source" ''' +
			r'''FROM "pins" WHERE "user" = ? ORDER BY "date" DESC LIMIT ?''',
		'get_board_pins':
			r'''SELECT "url", "date", "user", "board", "img", "caption", "source" ''' +
			r'''FROM "pins" WHERE "user" = ? AND "board" = ? ORDER BY "date" DESC LIMIT ?''',
		'register_update':
			r'''INSERT INTO "updates" ("user", "board", "time") ''' +
			r'''VALUES (?, ?, ?)''',
		'register_request':
			r'''INSERT INTO "requests" ("user", "time") ''' +
			r'''VALUES (?, ?, ?)'''
	}
} [DATABASE_TYPE]


class Database (object):
	"""Database abstraction layer"""

	def __init__ (self):
		if "sqlite3" == DATABASE_TYPE:
			self._init_sqlite3 ()
		elif "mysql" == DATABASE_TYPE:
			self._init_mysql ()

	def _init_sqlite3 (self):
		import sqlite3
		from config import SQLITE3_DATABASE
		self._connection = sqlite3.connect (SQLITE3_DATABASE)

	def _init_mysql (self):
		pass

	def get_pin (self, url):
		curs = self._connection.cursor ()
		curs.execute (_QUERIES['get_pin'], [url])

		pin_info = dict (zip (['date', 'user', 'board', 'img', 'caption', 'source'],
							  curs.fetchone ()))
		if "sqlite3" == DATABASE_TYPE:
			# sqlite3 does not support a native date type
			pin_info["date"] = datetime.utcfromtimestamp (pin_info["date"])

		curs.close ()
		return pin_info

	def save_pin (self, url, date, user, board, img, caption, source):
		curs = self._connection.cursor ()
		if "sqlite3" == DATABASE_TYPE:
			# sqlite3 does not support a native date type
			date = calendar.timegm (date.timetuple ())

		curs.execute (_QUERIES['save_pin'], [url, date, user, board, img, caption, source])
		curs.close ()
		self._connection.commit ()

	def did_update_within (self, tdelta, user, board=None):
		"""
		Is an update of this user recorded within the timedelta? (bool)
		If a board is given, return True only if that board has been queried
		at least once.
		"""
		curs = self._connection.cursor ()
		curs.execute (_QUERIES['updates_since'], [user, datetime.now () - tdelta])

		if curs.fetchone () is None:
			curs.close ()
			return False

		if board is not None:
			curs.execute (_QUERIES['updates_board'], [user, board])
			if curs.fetchone () is None:
				curs.close ()
				return False

		curs.close ()
		return True

	def get_pins (self, user, board=None, limit=FEED_LENGTH):
		from pins import Pin

		curs = self._connection.cursor ()
		if board is None:
			curs.execute (_QUERIES['get_user_pins'], [user, limit])
		else:
			curs.execute (_QUERIES['get_board_pins'], [user, board, limit])

		for row in curs:
			p = Pin (row[0], None)
			pin_info = dict (zip (['date', 'user', 'board', 'img', 'caption', 'source'], row[1:]))
			if "sqlite3" == DATABASE_TYPE:
				# sqlite3 does not support a native date type
				pin_info["date"] = datetime.utcfromtimestamp (pin_info["date"])
			p.populate (pin_info)

			yield p

		curs.close ()

	def register_update (self, user, board=None):
		curs = self._connection.cursor ()
		curs.execute (_QUERIES['register_update'], [user, board, datetime.now ()])
		curs.close ()
		self._connection.commit ()

	def register_request (self, user):
		curs = self._connection.cursor ()
		curs.execute (_QUERIES['register_request'], [user, datetime.now ()])
		curs.close ()
		self._connection.commit ()

db = Database ()
