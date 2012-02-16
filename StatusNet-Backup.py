#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import json
import os
import sys
import time
import urllib

import dateutil.parser
import requests

from lxml import etree


class StatusNet(object):
    timeline_url = None

    headers = {'user-agent': 'StatusNet 1.0 Backup'}
    stream_types = ('friends_timeline', 'user_timeline', 'favorites', 'memberships', 'subscriptions')

    namespaces = {
        'activity': 'http://activitystrea.ms/spec/1.0/',
        'app': 'http://www.w3.org/2007/app',
        'atom': 'http://www.w3.org/2005/Atom'
    }

    urls = {} # Cache URLs for streams

    def __init__(self, user_name, endpoint="http://identi.ca"):
        self.user_name = user_name
        self.endpoint = endpoint

        user_agent = '%s (User Contact: %s/%s)' \
            % (self.headers['user-agent'], endpoint, user_name)
        self.headers['user-agent'] = user_agent

        self.rs = requests.session(headers=self.headers)

    def _cacheTimelineUrls(self):
        # Request service document
        service_doc_url = '%s/api/statusnet/app/service/%s.xml' % (self.endpoint, self.user_name)
        response = self.rs.get(service_doc_url)

        if response is None:
            return None

        document = etree.fromstring(response.content)
        
        streams = document.xpath('//app:collection[@href]', namespaces=self.namespaces)
        if not streams:
            return None

        # TODO: figure out a smarter way to write this
        urls = {}
        for s in streams:
            url = s.get('href')
            for t in self.stream_types:
                if t in url:
                    urls[t] = url
                continue

        # HACK: Don't know how to discover this—hard-coded for now
        url = '%s/api/statuses/friends_timeline/%s.atom' % (self.endpoint, self.user_name)
        urls['friends_timeline'] = url

        self.urls = urls
        return urls

    def getTimelineUrl(self, timeline):
        if timeline in self.urls:
            return self.urls[timeline]

        urls = self._cacheTimelineUrls()

        if timeline in urls:
            return urls[timeline]

    def fetch(self, timeline, pageNo, format='atom'):
        url = self.getTimelineUrl(timeline) + '?page=%d' % pageNo

        if format in ('as', 'json'):
            url = url.replace('.atom', '.as')

        response = self.rs.get(url)

        if response.status_code != requests.codes.ok:
            return None

        return response.content


def main():
    parser = argparse.ArgumentParser(description='Backup your Identi.ca account')
    parser.add_argument('--username', required=True)
    parser.add_argument('--endpoint', default='http://identi.ca', help='(default: %(default)s)')
    parser.add_argument('--timeline', choices=StatusNet.stream_types, default='user_timeline')
    parser.add_argument('--page', type=int, default=1, help='Page number from which to start backup')
    parser.add_argument('--force', action='store_true', default=False, help='Force overwrite, ignoring previously backed-up entries')

    config = parser.parse_args()

    sn = StatusNet(config.username, config.endpoint)
    format = 'atom' # Hard-coded for now
    skippedEntries = 0

    # Create output directory
    try:
        os.makedirs(config.timeline)
    except Exception:
        pass
    os.chdir(config.timeline)

    for pageNo in range(config.page, 300):
        print('Processing page %d' % pageNo)
        raw_document = sn.fetch(config.timeline, pageNo, format=format)

        if raw_document is None:
            print('Error loading, skipping page', file=sys.stderr)
            continue
        
        if format == 'atom':
            # Fix for: ValueError: Unicode strings with encoding declaration are not supported
            # Dear lxml and Python: go die in a fire w/ your Unicode idiocy, thanks
            try:
                raw_document = raw_document.encode('utf-8')
            except UnicodeDecodeError:
                pass
            document = etree.fromstring(raw_document)
        elif format == 'as':
            document = json.loads(raw_document)

    #    for entry in json_document['items']:
    #        entry_id = entry['id']
    #        entry_text = entry['title']
    #        print entry_id, entry_text

        for entry in document.xpath('//atom:entry', namespaces=sn.namespaces):
            entry_id = entry.xpath('atom:id', namespaces=sn.namespaces)[0].text

            # Get published time & calculate file timestamp
            published_time = entry.xpath('atom:published', namespaces=sn.namespaces)[0].text
            published_time = dateutil.parser.parse(published_time)
            f_time = time.mktime(published_time.timetuple())

            filename = urllib.quote_plus(entry_id) + '.atom'

            # We've seen this entry before
            if os.path.isfile(filename) and not config.force:
                print('Skipping %s' % filename, file=sys.stderr)
                # this should be return to stop, continue to skip current entry
                # return
                if skippedEntries > 2:
                    return
                skippedEntries = skippedEntries + 1
                continue

            print('Backing up %s' % filename)
            f = file(filename, 'w')
            f.write(etree.tostring(entry))
            f.close()

            # Set last modified time for entry
            os.utime(filename, (f_time, f_time))

        time.sleep(5)


if __name__ == '__main__':
    main()
