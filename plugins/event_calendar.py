# Pelican Event Calendar plugin for NBLUG.org
# Copyright (C) 2014 Tom Most
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Generate an iCalendar file which contains events defined in Pelican articles.

The calendar is written to the location specified by the
``FEED_ALL_ICALENDAR`` setting.
"""

from __future__ import unicode_literals

import errno
import re
import os
import datetime

import pytz
import icalendar
import jinja2
from pelican import signals


# Matches a time range like "2014-01-02 7:00 am to 4:00 pm" or "2013/3/4
# 07:30PM - 09:00PM".
EVENT_RE = re.compile('''
    (?P<year>\d\d\d\d)
    \D
    (?P<month>\d\d?)
    \D
    (?P<day>\d\d?)
    \s+
    (?P<start_hour>\d\d?)
    :
    (?P<start_min>\d\d)
    (?P<start_p>\s*[ap]m?)
    \s+
    \D+
    (?P<end_hour>\d\d?)
    :
    (?P<end_min>\d\d)
    (?P<end_p>\s*[ap]m?)
''', re.IGNORECASE | re.VERBOSE)


def get_generators(pelican):
    # NB: This must be a global function, as signal receivers are
    # weakly-referenced.
    return CalendarGenerator


def register():
    signals.article_generator_context.connect(coerce_metadata)
    signals.get_generators.connect(get_generators)


def coerce_metadata(generator, metadata=None):
    """
    Called when an article is read to convert the ``'event'`` metadata element
    into ``'event_start'`` and ``'event_end'`` keys.
    metadata keys into :class:`datetime.datetime` instances.

    :param generator:
        the :class:`pelican.generators.ArticleGenerator` instance
    :param dict metadata:
        a mapping of article metadata which might contain (lowercased) keys we
        find interesting
    :raises ValueError: for unparseable date strings
    """
    if not metadata or 'event' not in metadata:
        return

    event_str = metadata.pop('event')
    m = EVENT_RE.match(event_str)
    if m is None:
        raise ValueError("Invalid event {!r}: try something like '1970-01-01 7:00 pm to 9:30 pm'".format(
            event_str))

    date = datetime.date(
        int(m.group('year')),
        int(m.group('month')),
        int(m.group('day')),
    )

    def ampm_offset(s):
        if 'p' in s.lower():
            return 12
        return 0

    start = datetime.time(
        int(m.group('start_hour')) + ampm_offset(m.group('start_p')),
        int(m.group('start_min')),
    )
    end = datetime.time(
        int(m.group('end_hour')) + ampm_offset(m.group('end_p')),
        int(m.group('end_min')),
    )

    if start >= end:
        raise ValueError('Invalid event {!r}: ends before it starts!'.format(
            event_str))

    metadata['event_start'] = datetime.datetime.combine(date, start)
    metadata['event_end'] = datetime.datetime.combine(date, end)


def event_from_article(article):
    """
    :param pelican.content.Article article:
    :rtype: :class:`icalendar.Event`
    """


class CalendarGenerator(object):
    """
    Output a calendar based on events defined in the articles.
    """

    def __init__(self, context, settings, path, theme, output_path):
        self.context = context
        self.settings = settings
        self.timezone = pytz.timezone(settings['TIMEZONE'])

    def generate_context(self):
        """
        Scrape calendar events from articles and generate a calendar.
        """
        cal = icalendar.Calendar()
        cal.add('version', '2.0')
        cal.add('prodid', '-//Pelican Calendar Plugin//nblug.org//')
        cal.add('x-wr-calname', 'NBLUG Events')

        threshold = pytz.utc.localize(datetime.datetime.utcnow() - datetime.timedelta(days=60))

        for article in self.context['articles']:
            start = getattr(article, 'event_start', None)
            if start and self.timezone.localize(start) > threshold:
                e = icalendar.Event()
                e.add('summary', jinja2.Markup(article.title).striptags())
                e.add('dtstart', self.timezone.localize(start).astimezone(pytz.utc))
                e.add('dtend', self.timezone.localize(article.event_end).astimezone(pytz.utc))
                e.add('status', 'CONFIRMED')
                if getattr(article, 'location', ''):
                    e['location'] = icalendar.vText(article.location)
                cal.add_component(e)

        self.calendar = cal

    def _open_w(self, writer, name):
        path = os.path.join(writer.output_path, name)
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        return open(path, 'w')

    def generate_output(self, writer):
        """
        Write the calendar to the output directory.
        """
        with self._open_w(writer, self.settings['FEED_ALL_ICALENDAR']) as f:
            f.write(self.calendar.to_ical())
