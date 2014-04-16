#!/usr/bin/env python
#
#    node_test.py: unit tests for vytree.Node
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
import unittest


class TestVytreeNode(unittest.TestCase):

    def setUp(self):
        self.node = vytree.Node("root")

    def test_create_node(self):
        self.assertIsInstance(self.node, vytree.Node)

    def test_get_name(self):
        self.assertEqual(self.node.get_name(), "root")

    def test_insert_immediate_child(self):
        child = self.node.insert_child(['foo'])
        self.assertIsInstance(child, vytree.Node)

    def test_insert_duplicate_child(self):
        self.node.insert_child(['foo'])
        self.assertRaises(vytree.ChildAlreadyExistsError,
                          self.node.insert_child,
                          ['foo'])

    def test_find_immediate_child(self):
        self.node.insert_child(['foo'])
        child = self.node.find_child('foo')
        self.assertIsInstance(child, vytree.Node)

    def test_get_child(self):
        child = self.node.insert_child(['foo'])
        self.assertIsInstance(child, vytree.Node)

    def test_get_child_multi_level(self):
        foo_child = self.node.insert_child(['foo'])
        bar_child = foo_child.insert_child(['bar'])
        self.assertEqual(bar_child, self.node.get_child(['foo', 'bar']))

    def test_delete_child(self):
        self.node.insert_child(['foo'])
        self.node.delete_child(['foo'])
        self.assertRaises(vytree.ChildNotFoundError,
                          self.node.find_child,
                          ['foo'])

    def test_delete_child_multi_level(self):
        self.node.insert_child(['foo', 'bar'])
        self.node.delete_child(['foo', 'bar'])
        self.assertRaises(vytree.ChildNotFoundError,
                          self.node.find_child,
                          ['foo', 'bar'])
        self.assertIsInstance(self.node.get_child(['foo']),
                              vytree.Node)

    def test_delete_child_subtree(self):
        self.node.insert_child(['foo', 'bar'])
        self.node.delete_child(['foo'])
        self.assertRaises(vytree.ChildNotFoundError,
                          self.node.find_child,
                          ['foo', 'bar'])

    def test_exists(self):
        node = vytree.Node('root')
        node.insert_child(['foo', 'bar'])
        self.assertTrue(node.child_exists(['foo', 'bar']))

    def test_does_not_exist(self):
        node = vytree.Node('root')
        self.assertFalse(node.child_exists(['foo']))

    def test_empty(self):
        node = vytree.Node('root')
        self.assertTrue(node.is_empty())

    def test_not_empty(self):
        node = vytree.Node('root')
        node.insert_child(['foo'])
        self.assertFalse(node.is_empty())

    def test_set_property(self):
        node = vytree.Node('test')
        node.set_property('key', 'value')
        self.assertEqual(node.get_property('key'), 'value')

    def test_set_property_bad_key(self):
        node = vytree.Node('test')
        self.assertRaises(TypeError,
                          node.set_property,
                          [{}, 'value'])

    def test_get_property_nonexistent_key(self):
        node = vytree.Node('test')
        self.assertRaises(vytree.UndefinedPropertyError,
                          node.get_property,
                          'fgsfds')


if __name__ == '__main__':
    unittest.main()
