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

    def set(self, path):
        pass

    def delete(self, path):
        pass

    def set_level(self, level):
        pass

    def commit(self):
        pass
