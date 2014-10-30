#!/usr/bin/env python
#
#    reference_node_loader.py: unit tests for
#       vyconf.tree.referencetree.ReferenceTreeLoader
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
import testtools

from vyconf.tree import referencetree as reftree
from vyconf.tests.integration.reference_tree import base


class MockType(object):
    @staticmethod
    def get_format_string(constraint):
        return "fgsfds"


class TestVytreeReferenceLoader(base.ReferenceTreeTestCase):
    def setUp(self):
        super(TestVytreeReferenceLoader, self).setUp()
        self.reference_tree = reftree.ReferenceNode('root')

        # For testing interface that expands other node
        self.reference_tree.insert_child(['quux'])

        loader = self.get_loader(
            "interface_definition_valid.xml",
            {"mock": MockType},
            'schemas/interface_definition.rng')

        loader.load(self.reference_tree)

    def test_get_child(self):
        child = self.reference_tree.get_child(['quux', 'foo', 'bar'])
        self.assertIsInstance(child, reftree.ReferenceNode)

    def test_should_not_be_tag_node(self):
        child = self.reference_tree.get_child(['quux', 'foo'])
        self.assertFalse(child.is_tag())

    def test_should_be_tag_node(self):
        child = self.reference_tree.get_child(['quux', 'foo', 'bar'])
        self.assertTrue(child.is_tag())

    def test_should_be_leaf_node(self):
        child = self.reference_tree.get_child(['quux', 'foo', 'bar', 'baz'])
        self.assertTrue(child.is_leaf())

    # Try loading an invalid definition
    def test_invalid_interface_definition(self):
        with testtools.ExpectedException(reftree.ReferenceTreeLoaderError):
            self.get_loader(
                'interface_definition_invalid.xml',
                {"mock": MockType},
                'schemas/interface_definition.rng')

    def test_duplicate_node(self):
        with testtools.ExpectedException(reftree.ReferenceTreeLoaderError):
            l = self.get_loader(
                'interface_definition_duplicate.xml',
                {"mock": MockType},
                'schemas/interface_definition.rng')
            t = reftree.ReferenceNode("root")
            l.load(t)
            l.load(t)
