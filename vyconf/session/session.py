import copy

import vyconf.tree.referencetree as rt
import vyconf.tree.configtree as ct

OP_MODE = 0
CONF_MODE = 1


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

    def configure(self):
        self._proposed_config = \
            copy.deepcopy(self._running_config)
        self._mode = CONF_MODE

    def set(self, config_path):
        self._validator.validate(config_path)

        path, value = self._validator.split_path(config_path)
        last_node = self._proposed_config.insert_child(path)

        if value:
            last_node.add_value(value)

    def delete(self, config_path):
        self._validator.validate(config_path)
        path, value = self._validator.split_path(config_path)
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
        pass

    def exists(self, config_path):
        self._validator.validate(config_path)
        path, value = self._validator.split_path(config_path)
        try:
            node = self._proposed_config.get_child(path)
            if value is not None:
                if value in node.get_values():
                    return True
                else:
                    return False
            else:
                return True
        except:
            return False

    def get_values(self, config_path):
        node = self._proposed_config.get_child(config_path)
        values = node.get_values()
        return values

    def commit(self):
        pass
