# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

AUTHOR = 'NBLUG Board Members'
SITENAME = 'North Bay Linux Users Group'

# Default to the devserver address.
SITEURL = os.environ.get('SITEURL', 'http://localhost:8000')

MENUITEMS = (
    ('News', ''),
    ('Find Our Meetings', 'locations/'),
    ('About Us', 'about/'),
    ('Archives', 'articles/'),
)

TIMEZONE = 'America/Los_Angeles'
DEFAULT_LANG = 'en'

THEME = './theme'
TYPOGRIFY = True

DEFAULT_CATEGORY = 'News'
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2}).*'

DELETE_OUTPUT_DIRECTORY = True
DIRECT_TEMPLATES = ('index', 'archives')

# Save article pages to subdirectories based on publication year.
ARTICLE_URL = 'articles/{date:%Y}/{slug}.html'
ARTICLE_SAVE_AS = 'articles/{date:%Y}/{slug}.html'

# Pages get top-level URLs.
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

# Enable yearly archives and an index page for them.
ARCHIVES_URL = 'articles/'
ARCHIVES_SAVE_AS = 'articles/index.html'
YEAR_ARCHIVE_SAVE_AS = 'articles/{date:%Y}/index.html'
YEAR_ARCHIVE_URL = 'articles/{date:%Y}/'

# Disable page generation for authors and tags.  If you enable this stuff
# you'll also need to update the templates to include links to these pages.
TAG_SAVE_AS = ''
TAGS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATH = 'plugins'
PLUGINS = ['drupal_urls']
