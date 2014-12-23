#    vyconf.session.util.item_status: list merging functions
#
#    Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#    USA


ADDED = 0
DELETED = 1
UNCHANGED = 2


def merge_with_status(old, new):
    """ Merge two lists and add a status:
        ADDED if item exists in new but not in old
        DELETED if item exists in old but not in new
        UNCHANGED if item exists in both
    """
    xs = []
    # Identify deleted and unchanged items first
    for i in old:
        if i in new:
            xs.append((UNCHANGED, i))
        else:
            xs.append((DELETED, i))

    # Now identify added items
    for i in new:
        if i not in old:
            xs.append((ADDED, i))

    return xs
