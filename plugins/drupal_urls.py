# Drupal Migration Plugin for NBLUG.org
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
Modify articles which sport a "drupal_node" metadata parameter to have a URL of
``/node/{id}/`` because Cool URLs Don't Change.

Note that in the old side things were available at both ``/node/{id}`` and
``/node/{id}/``, with most links pointing at the version without a trailing
slash.  This plugin uses the form with the trailing slash because Apache will
automatically redirect from the first to the second when the first is
a directory.
"""

from __future__ import unicode_literals

from pelican import signals


def register():
    signals.content_object_init.connect(url_from_drupal_node)


def url_from_drupal_node(content):
    node = content.metadata.get('drupal_node')
    if not node:
        return

    content.override_save_as = 'node/{}/index.html'.format(node)
    content.override_url = 'node/{}/'.format(node)
