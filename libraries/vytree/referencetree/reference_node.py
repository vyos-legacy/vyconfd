#    vytree.reference_node: Interface definition storage classes for VyConf configuration management backend
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


import vytree

class ReferenceNodeError(Exception):
    """ Raised on attempts to create incorrectly configure ReferenceNode
        instance (e.g. set mutually exlusive flags at the same time)
    """
    def __init__(self, message):
        super(ChildNotFoundError, self).__init__(message)
        self.strerror = message

class ReferenceNode(vytree.Node):
    def __init__(self, name, parent=None):
        super(ReferenceNode, self).__init__(name, parent)

        # Default flags
        self.set_property("leaf", False)
        self.set_property("tag", False)
        self.set_property("multi", False)
        self.set_property("name_constraint", {})
        self.set_property("value_constraints", [])
        self.set_property("help_string", "")

    def set_leaf(self):
        self.set_property("leaf", True)

    def is_leaf(self):
        return self.get_property("leaf")

    def set_tag(self):
        self.set_property("tag", True)

    def is_tag(self):
        return self.get_property("tag")

    def set_multi(self):
        self.set_property("multi", True)

    def is_multi(self):
       	return self.get_property("multi")

    def set_name_constraint(self, name_type, name_constraint):
        self.set_property("name_constraint", {"type": name_type, "constraint": name_constraint})

    def get_name_constraint(self):
        return self.get_property("name_constraint")

    def add_value_constraint(self, type, constraint):
        if (not isinstance(type, str)) and (not isinstance(constraint, str)):
            raise TypeError("Type and constraint must be strings")
        self.get_property("value_constraints").append({"type": type, "constraint": constraint})

    def get_value_constraints(self):
        return self.get_property("value_constraints")

    def set_help_string(self, value):
        self.set_property("help_string", value)

    def get_help_string(self):
        return self.get_property("help_string")
