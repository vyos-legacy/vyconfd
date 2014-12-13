#    vyconf.session.session: VyConf session interface
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

# Who said "God object"? It's a facade!

import copy
import vyconf.pathutils as vpu

OP_MODE = 0
CONF_MODE = 1

UNCHANGED = 0
CHANGED = 1
ADDED = 2
DELETED = 3


class SessionError(Exception):
    def __init__(self, msg):
        super(SessionError, self).__init__(msg)
        self.strerror = msg


class Session(object):
    def __init__(self,
                 running_config,
                 validator,
                 user):
        self._running_config = running_config
        self._proposed_config = None
        self._validator = validator
        self._user = user
        self._level = None
        self._mode = OP_MODE
        self._changed = False

    def _make_path(self, config_path, abspath):
        if self._level and (not abspath):
            return self._level + config_path
        else:
            return config_path[:]

    def configure(self):
        self._proposed_config = \
            copy.deepcopy(self._running_config)
        self._mode = CONF_MODE

    def set(self, config_path, abspath=False):
        _config_path = self._make_path(config_path, abspath)
        self._validator.validate(_config_path)

        path, value = self._validator.split_path(_config_path)

        if value:
            node = None
            if not self.exists(path, abspath=True):
                node = self._proposed_config.insert_child(path)
            else:
                node = self._proposed_config.get_child(path)

            if self._validator.check_node(path, lambda x: x.is_multi()):
                if node.has_value(value):
                    raise SessionError("Node \"{0}\" already has value \"{1}\"".format(
                        vpu.path_to_string(path), value))
                else:
                    node.add_value(value)
            else:
                node.set_value(value)
        else:
            self._proposed_config.insert_child(path)

    def delete(self, config_path, abspath=False):
        _config_path = self._make_path(config_path, abspath)
        self._validator.validate(_config_path)
        path, value = self._validator.split_path(_config_path)
        node = self._proposed_config.get_child(path)

        if value and (len(node.get_values()) > 1):
            # If the node has more than one value,
            # delete only specified value
            node.delete_value(value)
        else:
            # Otherwise delete the whole node,
            # since we don't allow leaf nodes without values
            self._proposed_config.delete_child(path)

    def set_level(self, level):
        if not isinstance(level, list):
            raise SessionError(
                "{0} is not a valid config level".format(repr(level)))
        else:
            self._level = level

    def get_level(self):
        return self._level

    def exists(self, config_path, abspath=False):
        _config_path = self._make_path(config_path, abspath)
        path, value = self._validator.split_path(_config_path)
        try:
            node = self._proposed_config.get_child(path)
            if value is not None:
                if value in node.get_values():
                    return True
                else:
                    return False
            else:
                return True
        # TODO(dmbaturin): Fixup to use more specific exceptions
        except Exception:
            return False

    def get_values(self, config_path, abspath=False):
        _config_path = self._make_path(config_path, abspath)
        node = self._proposed_config.get_child(_config_path)
        values = node.get_values()
        return values

    def set_comment(self, config_path, comment, abspath=False):
        if not isinstance(comment, str):
            raise SessionError(
                "{0} is not a valid comment strine".format(comment))

        _config_path = self._make_path(config_path, abspath)
        path, value = self._validator.split_path(_config_path)
        node = self._proposed_config.get_child(_config_path)
        node.set_comment(comment)

    def get_comment(self, config_path, abspath=False):
        _config_path = self._make_path(config_path, abspath)
        path, value = self._validator.split_path(_config_path)
        node = self._proposed_config.get_child(path)
        return node.get_comment()

    def get_node_status(self, config_path, abspath=False):
        _config_path = self._make_path(config_path, abspath)
        path, value = self._validator.split_path(_config_path)
        return self.__get_node_status(self._running_config, self._proposed_config, path)

    def __get_node_status(self, running, proposed, path):
        cur_level = path.pop(0)
        if running.child_exists(cur_level) and proposed.child_exists(cur_level):
            running_child = running.find_child(cur_level)
            proposed_child = proposed.find_child(cur_level)
            if path:
                # We need to go deeper
                self.__get_node_status(running_child, proposed_child, path)
            else:
                # It's a leaf node, we need to compare values
                if set(running_child.get_values()) == set(proposed_child.get_values()):
                    return UNCHANGED
                else:
                    return CHANGED
        elif running.child_exists(cur_level) and not proposed.child_exists(cur_level):
            return DELETED
        elif not running.child_exists(cur_level) and proposed.child_exists(cur_level):
            return ADDED
        else:
            # Shouldn't happen
            raise SessionError("Could not determine status of {0}: missing from both trees".format(cur_level))
              
    def commit(self):
        pass
