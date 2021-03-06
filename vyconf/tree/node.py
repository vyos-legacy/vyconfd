#    vyconf.tree.node: base classes for VyConf configuration management backend
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

# An ash I know, Yggdrasil its name,
# With water white is the great tree wet;
# Thence come the dews that fall in the dales,
# Green by Urth's well does it ever grow.
#                   From The Poetic Edda, Voluspa

import copy


class ChildNotFoundError(Exception):
    """Raised on attempts to look up a non-existent path."""
    def __init__(self, node, child):
        message = "Node {0} has no child {1}".format(node, child)
        super(ChildNotFoundError, self).__init__(message)
        self.strerror = message


class ChildAlreadyExistsError(Exception):
    """Raised on attempts to insert the same child more than one time."""
    def __init__(self, node, child):
        message = "Node {0} already has child {1}".format(node, child)
        super(ChildAlreadyExistsError, self).__init__(message)
        self.strerror = message


class Node(object):
    """The base class for configuration and reference tree nodes.

        This class is not supposed to be used directly.
    """

    def __init__(self, name, parent=None):
        self.__name = name
        self.__children = []
        self.__properties = {}
        self.__parent = parent

    @staticmethod
    def to_list(arg):
        """If the argument is not a list, makes a single-item list of it.
            Many functions of this class treat path as a list internally,
            but converting it manually in calls is too annoying.

        :param arg: list to be returned unchanges or anything that converts to
                    list
        """
        if not isinstance(arg, list):
            return [arg]
        else:
            return arg

    @classmethod
    def _make_path(self, arg):
        _arg = self.to_list(arg)
        return copy.copy(_arg)

    def get_name(self):
        """Returns node name."""
        return self.__name

    def dump_properties(self):
        return self.__properties

    def find_child(self, name):
        """Finds an immediate child by name.

        :param name: Child name
        :type name: str

        :rtype: None
        :raises: ChildNotFoundError
        """

        # XXX: insert function guarantees that names are unique,
        # so we don't check it here
        result = [x for x in self.__children if x.get_name() == name]
        if result:
            return result[0]
        else:
            raise ChildNotFoundError(self.get_name(), name)

    def list_children(self):
        """Lists immediate children.

        :returns: List of node names
        """
        names = [x.get_name() for x in self.__children]
        return names

    def get_child(self, path_or_name):
        """Finds a child node by path.

        :param path_or_name: The path to a child node.
                             Example: ["org", "branches", "depts"] or
                                      "branches"
        :type path_or_name: str

        :returns: Node: Child node
        :raises: ChildNotFoundError
        """
        path = self._make_path(path_or_name)

        # Special case for empty path
        # Returning self is probably the most reasonable approach
        if not path:
            return self

        next_level = path.pop(0)
        if not path:
            # It was the last path level
            # So it's either an immediate child or there's no such node
            child = self.find_child(next_level)
            return child
        else:
            # It's not, we need to recurse
            child = self.find_child(next_level)
            return child.get_child(path)

    def insert_child(self, path_or_name):
        """Inserts a new child.

        :param args: The path to a child node.

        :returns: Node: Inserted child node
        :raises: ChildNotFoundError ChildAlreadyExistsError
        """
        path = self._make_path(path_or_name)

        next_level = path.pop(0)
        if not path:
            # That was the last item of the path,
            # so the node is going to be an immediate child

            # Check if we are not trying to add the same name twice
            children = self.list_children()
            if next_level in children:
                raise ChildAlreadyExistsError(self.get_name(), next_level)

            node_type = type(self)
            child = node_type(next_level, self)
            self.__children.append(child)
            return child
        else:
            # It is not, so we need to recurse,
            # but first decide if we have where to recurse.
            try:
                next_child = self.find_child(next_level)
            except ChildNotFoundError:
                next_child = self.insert_child([next_level])

            return next_child.insert_child(path)

    def delete_child(self, path_or_name):
        """Delete child node.

        :param path_or_name: The path to a child node.
        """
        path = self._make_path(path_or_name)

        next_level = path.pop(0)
        if not path:
            # It was the last path level
            # So it's either an immediate child or there's no such node
            child = self.find_child(next_level)
            self.__children.remove(child)
        else:
            # It's not, we need to recurse
            child = self.find_child(next_level)
            child.delete_child(path)

    def child_exists(self, path_or_name):
        """Checks if specific path to a child exists."""
        path = self.to_list(path_or_name)
        try:
            self.get_child(path)
            return True
        except ChildNotFoundError:
            return False

    def is_empty(self):
        """Checks if a node has any children."""
        if self.list_children():
            return False
        else:
            return True

    def get_children(self):
        """ Returns a list of children (not names) """
        return self.__children

    def get_parent(self):
        return self.__parent

    def set_property(self, key, value):
        """Set property value by key."""
        try:
            self.__properties[key] = value
        except TypeError:
            raise TypeError("Wrong property key type: {0}".format(
                type(key).__name__))

    def get_property(self, key):
        """Get property value by key."""

        try:
            if key in self.__properties:
                return self.__properties[key]
            else:
                return None
        except TypeError:
            raise TypeError("Wrong property key type: {0}".format(
                type(key).__name__))
