#    vyconf.tree.referencetree.path_validator:
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
import vyconf.types
import vyconf.tree
import vyconf.tree.referencetree
import vyconf.pathutils as vpu


class PathValidationError(Exception):
    """ Raised when config path validation fails
    """
    def __init__(self, message, additional_messages=None):
        super(PathValidationError, self).__init__(message)
        self.strerror = message
        if additional_messages is not None:
            self.errors = additional_messages


class PathValidator(object):
    def __init__(self, types=None, tree=None):
        """ Creates a path validator object

            Args:
                types (dict): dictionary of type names and validators
                tree (vyconf.tree.ReferenceTree):
                    a reference tree instance
        """
        if types is None:
            self.types = {}

        else:
            self.types = types

        if tree is None:
            self.tree = None
        else:
            self.tree = tree

    def _validate_leaf_or_tag_node(self, types, node, value):
        """ Validates a value or next child name against node constraints.

            Args:
                types (dict): a dict of vyconf.types.TypeValidator ancestors
                node (vyconf.tree.referencetree.ReferenceNode): a leaf or
                tag node
                value: a value (or name) to validate
        """
        valid = False
        errors = []

        constraint_list = None
        if node.is_leaf():
            constraint_list = node.get_value_constraints()
        else:
            constraint_list = [node.get_name_constraint()]

        for constraint_dict in constraint_list:
            current_type = constraint_dict['type']
            current_constraint = constraint_dict['constraint']
            try:
                self.types[current_type].validate(value, current_constraint)
                valid = True
                break
            except vyconf.types.ValidationError as e:
                errors.append(e.strerror)
        if valid:
            return (True, [])
        else:
            # Error messages go to the user, so we need to
            # pass them to the caller
            return (False, errors)

    def _validate(self, config_path, node):
        # We are going to mangle the path, so copy it first
        path = config_path[:]

        # There are two tricky cases: tag nodes and leaf nodes,
        # which need special validation of the immediate child.
        if node.is_leaf() or node.is_tag():
            next_item = None
            if path:
                next_item = path.pop(0)
            else:
                raise PathValidationError(
                    "Configuration path [%s] is incomplete" %
                    vpu.path_string(config_path))

            (result, errors) = self._validate_leaf_or_tag_node(self.types,
                                                               node,
                                                               next_item)
            if not result:
                msg = ""
                if node.is_leaf():
                    msg = "Value validation failed"
                else:
                    msg = "Node name validation failed"
                raise PathValidationError(msg,
                                          additional_messages=errors)
            else:
                if node.is_leaf():
                    if not path:
                        return True
                    else:
                        # There are extra items after a leaf node
                        raise PathValidationError(
                            "Configuration path [%s] has extra items" %
                            vpu.path_string(config_path))
                else:
                    if path:
                        next_item = path.pop(0)
                        next_node = node.find_child(next_item)
                        self._validate(path, next_node)
                    else:
                        return True
        else:
            # It's a normal node, just recurse to it, if we have where to
            # recurse
            if path:
                next_node = node.find_child(path.pop(0))
                self._validate(path, next_node)
            else:
                return True

    def validate(self, config_path, config_level=None):
        """ Validates a config path against

            Args:
                config_path (list): a list representing config path
        """
        path = config_path[:]
        if config_level is not None:
            path = config_level + path

        try:
            self._validate(path, self.tree)
        except vyconf.tree.ChildNotFoundError:
            raise PathValidationError(
                "Configuration path [%s] is not valid"
                % vpu.path_string(config_path))
