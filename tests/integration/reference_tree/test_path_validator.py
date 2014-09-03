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

import vyconf.tree.referencetree as reftree
import vyconf.types as types
import vyconf.types.dummy as dummytypes

from tests.integration import base


class TestVytreePathValidator(base.TestCase):
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
        self.validator.validate(['foo', 'bar', 'somename'])

    def test_path_doesnt_exist(self):
        self.assertRaises(
            reftree.PathValidationError,
            self.validator.validate,
            ['foo', 'baz'])

    def test_leaf_node_valid_value(self):
        self.validator.validate(['quux', 'spam', 'somevalue'])
