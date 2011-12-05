StatusNet Stream Backup
=======================

Backs up StatusNet 1.0 streams in Activity Streams Atom format.

Installation
------------

This tool isn't very robust yet; clone the repository, install the
dependencies, and save into the folder it is run for best results.

Make sure you have Python 2.6 or 2.7 (it is 2to3 compatible but I've not
yet tested it), argparse (included with 2.7), dateutil, lxml, and requests.
On Ubuntu/Debian run:

 $ sudo aptitude install python-dateutil python-requests python-lxml

Use
---

If your username is billgates on Identi.ca, run:

 $ StatusNet-Backup.py --username billgates

to backup your entire "user timeline" (your own notices) into a directory
called "user_timeline". If you want to backup your "friends timeline"
(the notices of those you subscribe to), run:

 $ StatusNet-Backup.py --username billgates --stream friends_timeline

This tool will start at page 1, and go as far back as possible until it
encounters an entry it's seen before (e.g. you can add the above to cron
to continually add new entries to your backup).

This tool can cause a lot of server load. Please use it during off-peak
times, and use it responsibly.

Details
-------

This tool saves streams in [Activity Streams Atom format][as-atom] as is
made available from StatusNet 1.0 or later.

  [as-atom]: http://activitystrea.ms/specs/atom/1.0/

Each entry (i.e. notice, poll, etc) is saved as an individual file.

There isn't a tool to import this back into a StatusNet installation.
I'm working on it. But, at least, you've a backup in a future-proof,
standardized format.

This tool is tailored for use w/ StatusNet, but could be modified easily
to backup anything that exports Activity Streams Atom—that includes
Flattr, Google Buzz, etc.

License
-------

Copyright © 2011 Samat K Jain.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
