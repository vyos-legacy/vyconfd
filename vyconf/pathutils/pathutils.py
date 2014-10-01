#    vyconf.pathutils.pathutils:
#        miscellaneous path handling functions
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


import re


def path_to_string(path, separator=" "):
    """ Converts path list to a string """
    if not isinstance(separator, str):
        raise ValueError("Separator must be a string")

    item_list = []

    for item in path:
        item_str = ""
        if not isinstance(item, str):
            item_str = str(item)
        else:
            item_str = item

        # We need to quote string that contain whitespace
        if re.search('\s', item_str):
            item_str = "'" + item_str + "'"

        item_list.append(item_str)

    return separator.join(item_list)

def string_to_path(path_str, separator=" "):
    """ Converts a string to a path list. """
    path = path_str.split(separator)
    return path
