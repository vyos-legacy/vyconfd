#!/usr/bin/env python
#
#    path_validator_path.py: unit tests for
#       vyconf.tree.referencetree.PathValidator
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

import copy

import vyconf.tree.referencetree as reftree
import vyconf.types as types
import vyconf.types.dummy as dummytypes

from .base import ReferenceTreeTestCase


class TestVytreePathValidator(ReferenceTreeTestCase):
    def setUp(self):
        super(TestVytreePathValidator, self).setUp()
        self.types_dict = types.get_types(dummytypes)

        self.reference_tree = reftree.ReferenceNode('root')

        loader = self.get_loader(
            'interface_definition_validation_test.xml',
            self.types_dict,
            'schemas/interface_definition.rng')
        loader.load(self.reference_tree)

        self.validator = reftree.PathValidator(
            self.types_dict, self.reference_tree)

    def test_path_exists(self):
        self.validator.validate(['foo'])

    def test_path_doesnt_exist(self):
        self.assertRaises(
            reftree.PathValidationError,
            self.validator.validate,
            ['foo', 'baz'])

    def test_incomplete_tag_node_path(self):
        self.assertRaises(
            reftree.PathValidationError,
            self.validator.validate,
            ['foo', 'bar'])

    def test_incomplete_leaf_node_path(self):
        self.assertRaises(
            reftree.PathValidationError,
            self.validator.validate,
            ['foo', 'bar', 'aaa', 'baz'])

    def test_leaf_node_value_valid(self):
        self.validator.validate(['quux', 'spam', '123'])

    def test_leaf_node_value_invalid(self):
        self.assertRaises(
            reftree.PathValidationError,
            self.validator.validate,
            ['quux', 'xyzzy', 'aaa'])

    def test_garbage_after_leaf_node(self):
        self.assertRaises(
            reftree.PathValidationError,
            self.validator.validate,
            ['quux', 'spam', 'aaa', 'bbb'])

    def test_tag_node_content_valid(self):
        self.validator.validate(['foo', 'bar', 'qwerty', 'baz', 'xyz'])

    def test_split_path(self):
        path, value = self.validator.split_path(
            ['quux', 'spam', '123'])

        self.assertTrue(
            (path == ['quux', 'spam']) and (value == '123'))

    def test_split_path_typeless(self):
        path, value = self.validator.split_path(
            ['quux', 'cheese'])

        self.assertTrue(
            (path == ['quux', 'cheese']) and (value is None))

    def test_split_path_nonleaf(self):
        path, value = self.validator.split_path(
            ['foo', 'bar'])
        self.assertTrue(
            (path == ['foo', 'bar']) and (value is None))

    def test_split_path_tag(self):
        path, value = self.validator.split_path(
            ['foo', 'bar', 'asdf', 'baz', '123'])
        self.assertTrue(
            (path == ['foo', 'bar', 'asdf', 'baz'])
            and (value == '123'))

    # Ensure methods that take a list argument do not
    # mangle it

    def test_validate_non_destructive(self):
        path = ['foo', 'bar', 'asdf', 'baz', '123']
        _path = copy.copy(path)
        self.validator.validate(path)
        self.assertEqual(path, _path)

    def test_split_path_non_destructive(self):
        path = ['foo', 'bar', 'asdf', 'baz', '123']
        _path = copy.copy(path)
        self.validator.split_path(path)
        self.assertEqual(path, _path)
