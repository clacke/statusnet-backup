StatusNet Timelines Backup
==========================

Backs up StatusNet 1.0 streams in Activity Streams Atom format.

Installation
------------

This tool isn't very robust yet; clone the repository, install the
dependencies, and backup into the folder you cloned it for best results.

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

 $ StatusNet-Backup.py --username billgates --timeline friends_timeline

This tool will start at page 1, and go as far back as possible until it
encounters an entry it's seen before (e.g. you can add the above to cron
to continually add new entries to your backup).

This tool can cause a lot of server load. Please use it during off-peak
times, and use it responsibly.

Known Issues
------------

### Unicode problems

This tool works on Ubuntu 9.10. However, when I run it on identical (as far
as I can tell) Debian testing system, I get a Python Unicode error:

 Traceback (most recent call last):
   File "Identica-Backup.py", line 157, in <module>
     main()
   File "Identica-Backup.py", line 120, in main
     document = etree.fromstring(raw_document)
   File "lxml.etree.pyx", line 2743, in lxml.etree.fromstring (src/lxml/lxml.etree.c:52665)
   File "parser.pxi", line 1564, in lxml.etree._parseMemoryDocument (src/lxml/lxml.etree.c:79843)
 ValueError: Unicode strings with encoding declaration are not supported.

The error is from lxml: it is claiming that a document it attempts to parse
(from Identi.ca/your StatusNet installation) says it is not Unicode—when it
is! Again, the same thing works on Ubuntu, and I've no idea how to fix this.
If you've an idea how to FIX it (i.e. I don't want your it's-MY-fault-
Unicode-is-a-headache-in-Python lecture), please let me know.

### Incomplete backups

The first time you run this tool, it'll attempt to backup your entire timeline.

But what if something happens before it finishes? At the moment, the tool
does not resume, and you have to handle the situation manually. When it
fails, take note of the last page number processed. Then, run with --page
and --force to start downloading from that page again. E.g.:

 $ StatusNet-Backup.py --username billgates --page 43 --force

Details
-------

This tool saves timelines in [Activity Streams Atom format][as-atom] as is
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
