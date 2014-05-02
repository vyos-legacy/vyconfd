#!/usr/bin/env python
#
#    reference_node_loader.py: unit tests for vytree.referencetree.ReferenceTreeLoader
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
import vytree.referencetree
import unittest

import pkg_resources

class MockType(object):
    @staticmethod
    def get_format_string(constraint):
        return "fgsfds"

class TestVytreeReferenceLoader(unittest.TestCase):
    def setUp(self):
        self.reference_tree = vytree.referencetree.ReferenceNode('root')
        xml = pkg_resources.resource_filename(__name__, "interface_definition_valid.xml")

        loader = vytree.referencetree.ReferenceTreeLoader(xml, {"mock": MockType})
        loader.load(self.reference_tree)

    def test_get_child(self):
        child = self.reference_tree.get_child(['foo', 'bar'])
        self.assertIsInstance(child, vytree.referencetree.ReferenceNode)
