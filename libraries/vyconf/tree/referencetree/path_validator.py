#    vyconf.tree.tree.referencetree.path_validator:
#        config path validator
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

import vyconf.tree
from .reference_node import ReferenceNodeError

class PathValidationError(Exception):
    """ Raised when config path validation fails
    """
    def __init__(self, message):
        super(PathValidationError, self).__init__(message)
        self.strerror = message


class PathValidator(object):
    def __init__(self, types=None, tree=None):
        """ Creates a path validator object

            Args:
                types (dict): dictionary of type names and validators
        """
        if types is None:
            self.types = {}

        else:
            self.types = types

        if tree is None:
            self.tree = None
        else:
            self.tree = tree

    def validate(self, config_path, config_level=None):
        """ Validates a config path against

            Args:
                config_path (list): a list representing config path
        """
        # We are going to mangle it, so copy it first
        path = config_path[:]

        if config_level is not None:
            path = config_level + path

        try:
            child = self.tree.get_child(path)
        except vyconf.tree.ChildNotFoundError:
            raise PathValidationError(""" Configuration path "{0}" is not valid""".format(" ".join(config_path)))
