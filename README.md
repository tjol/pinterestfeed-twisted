Pinterest RSS feed generator
============================

**This service generates RSS feeds for Pinterest users and boards.**

Copyright (C) 2013 Thomas Jollans <t@jollybox.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

See: AGPL.txt

Requirements
------------

This program is written in Python 2 and uses Twisted and several other
useful modules:

+ **twisted.web** and dependencies by Twisted Matrix
+ **PyRSS2Gen** by Dalke Scientific
+ **feedparser** by Mark Pilgrim et al.
+ **BeautifulSoup** version 3 by Leonard Richardson
+ **MySQLdb** by Andy Dustman if you want to use MySQL

Configuration
-------------

A database needs to be set up and configured. The comments in `config.py`
should be self explanatory.

To run, start `runserver.py`.

Notes on functionality
----------------------

This service will automatically reload feeds that have recently been accessed
in the background to ensure speedy response times for most users. It relies on
the RSS feeds provided by Pinterest (hopefully, these won't be removed when the
new layout, in beta at the time of writing, goes gold) and META tags that look
like they're also parsed by the Pinterest mobile app.

As this service will generate a lot of requests when run in public, it *might*
be blocked by Pinterest, even if they have no malicious intent towards this
project.
