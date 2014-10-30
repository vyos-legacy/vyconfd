#!/usr/bin/env python
#
# test_path_utils.py: unit tests for vyconf.pathutils module.
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

import vyconf.pathutils as vpu


class TestPathUtils(unittest.TestCase):
    def test_path_to_string_default(self):
        # Default separator is space
        path_str = vpu.path_to_string(['foo', 'bar'])
        self.assertEqual(path_str, "foo bar")

    def test_path_to_string_separator(self):
        path_str = vpu.path_to_string(['foo', 'bar'], separator="/")
        self.assertEqual(path_str, "foo/bar")

    def test_string_to_path_default(self):
        path = vpu.string_to_path("foo bar")
        self.assertEqual(path, ['foo', 'bar'])

    def test_string_to_path_separator(self):
        path = vpu.string_to_path("foo:bar:baz", separator=":")
        self.assertEqual(path, ['foo', 'bar', 'baz'])
