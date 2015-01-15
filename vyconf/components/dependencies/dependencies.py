# vyconf.components.dependencies: dependency sorting functions
#
# Copyright (C) 2014 VyOS Development Group <maintainers@vyos.net>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301
# USA

import copy


class DependencyError(Exception):
    def __init__(self, message, components):
        super(DependencyError, self).__init__(message)
        self.strerror = message
        self.components = components


class DependencyList(object):

    def __init__(self, components):
        missing = self._check_missing_deps(components)
        if missing:
            error = ""
            line_format = \
                "Component \"{0}\" required by \"{1}\" does not exist\n"
            for i in missing:
                line = line_format.format(i[1], i[0])
                error = error + line
            raise DependencyError(error, None)

        self.__deps = self._sort_dependencies(components)

    def get_dependencies(self):
        return self.__deps

    def _subset_of(self, l1, l2):
        s1 = set(l1)
        s2 = set(l2)
        return s1.issubset(s2)

    def _check_missing_deps(self, components):
        keys = components.keys()
        missing = []

        for k in keys:
            for i in components[k]:
                if i not in keys:
                    missing.append((k, i))

        return missing

    def _sort_dependencies(self, components):
        """Sorts dependencies in topological order

            Args:
                components (dict): A dictionary of component names and lists
                of their dependencies.

            Returns:
                list: a list of lists of components with the same priority
        """

        # The idea:
        # 1. Move components that have no dependencies to the first item
        #    of the sorted list and remember them in seen_deps list.
        # 2. Find components that depend only on components from the
        #    seen_deps list, add them to the next item of the sorted list
        #    and add to seen_deps.
        # 3. Repeat this until the component list is empty.
        #    if nothing is removed in a step, it means there is either
        #    a loop or a non-existent dependency.

        _components = copy.copy(components)
        seen_deps = []
        sorted = []

        while _components:
            cur_level = []
            cur_len = len(_components)

            __components = copy.copy(_components)
            for key in __components.keys():
                deps = __components[key]
                if self._subset_of(deps, seen_deps):
                    cur_level.append(key)
                    del _components[key]

            # If no components were deleted in the inner loop,
            # it means there's a cycle
            if len(_components) == cur_len:
                raise DependencyError("Dependency graph has at least one loop",
                                      _components)

            sorted.append(cur_level)
            seen_deps = seen_deps + cur_level

        return sorted
