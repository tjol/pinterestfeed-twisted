# config.py
# 
# pinterestfeed2 - Pinterest RSS feed generator
# 
# Copyright (C) 2013 Thomas Jollans
#   This program is free software subject to the conditions of the AGPL,
#   version 3 or newer. For details, see README.md and AGPL.txt
#
# This file is a configuration file. System-specific modifications to this
# file are not considered part of the "Corresponding Source" as defined in
# the AGPL.

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

# mysql:
# CREATE TABLE IF NOT EXISTS pins
#    (`id` INTEGER AUTO_INCREMENT PRIMARY KEY,
#     `user` VARCHAR(255) NOT NULL,
#     `board` VARCHAR(255) NOT NULL,
#     `url` VARCHAR(255) UNIQUE,
#     `caption` TEXT,
#     `img` VARCHAR(255),
#     `source` VARCHAR(255),
#     `date` DATETIME NOT NULL);
#
# CREATE TABLE IF NOT EXISTS updates
#	(`user` VARCHAR(255) NOT NULL,
#	 `board` VARCHAR(255),
#	 `time` DATETIME NOT NULL);
#
# CREATE TABLE IF NOT EXISTS requests
# 	(`user` VARCHAR(255) NOT NULL,
# 	 `time` DATETIME NOT NULL);


# DATABASE_TYPE = "mysql"
# MYSQL_PARAMETERS = {...}

# TCP port to listen on
PORT = 8080
LISTEN_ON = "127.0.0.1"

# TIMES TO LIVE
PINS_TTL = timedelta (minutes=30)
AUTORELOAD_AFTER = timedelta (minutes=13)
IGNORE_AFTER = timedelta (days=1)
PROBE_INTERVAL = timedelta (minutes=5)

# Number of items to display in a feed
FEED_LENGTH = 20
