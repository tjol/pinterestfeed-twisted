# config.py

from datetime import timedelta

# sqlite3:
# CREATE TABLE IF NOT EXISTS "pins"
#    (id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user TEXT NOT NULL,
#     board TEXT NOT NULL,
#     url TEXT UNIQUE,
#     caption TEXT,
#     img TEXT,
#     source TEXT,
#     date INTEGER NOT NULL);
#
# CREATE TABLE IF NOT EXISTS "updates"
#	(user TEXT NOT NULL,
#	 board TEXT,
#	 time INTEGER NOT NULL);
#
# CREATE TABLE IF NOT EXISTS "requests"
# 	(user TEXT NOT NULL,
# 	 time INTEGER NOT NULL);


DATABASE_TYPE = "sqlite3"
SQLITE3_DATABASE = "pins.db"

# TCP port to listen on
PORT = 8080

# TIMES TO LIVE
PINS_TTL = timedelta (minutes=30)
AUTORELOAD_AFTER = timedelta (minutes=20)
IGNORE_AFTER = timedelta (days=1)

# Number of items to display in a feed
FEED_LENGTH = 20
