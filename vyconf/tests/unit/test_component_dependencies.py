#!/usr/bin/env python
#
# test_component_dependencies.py:
#    unit tests for vyconf.components.dependencies
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

import unittest

import vyconf.components.dependencies as deps


def sort_inner(l):
    for i in l:
        i.sort()


class TestComponentDependencies(unittest.TestCase):
    def test_valid_one_per_list(self):
        data = {"foo": [], "bar": ["foo"]}
        deplist = deps.DependencyList(data).get_dependencies()
        self.assertEqual(deplist, [['foo'], ['bar']])

    def test_valid_multiple_per_list(self):
        data = {"foo": [], "bar": [], "baz": ["foo", "bar"]}
        deplist = deps.DependencyList(data).get_dependencies()
        self.assertEqual(sort_inner(deplist),
                         sort_inner([["foo", "bar"], ["baz"]]))

    def test_invalid_missing_dep(self):
        data = {"foo": ["bar"]}
        self.assertRaises(deps.DependencyError,
                          deps.DependencyList, data)

    def test_invalid_loop(self):
        data = {"foo": ["bar"], "bar": ["baz"], "baz": ["foo"]}
        self.assertRaises(deps.DependencyError,
                          deps.DependencyList, data)

    def test_nondestructive(self):
        data = {"foo": [], "bar": ["foo"]}
        deplist = deps.DependencyList(data).get_dependencies()
        self.assertEqual(data, {"foo": [], "bar": ["foo"]})
