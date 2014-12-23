#!/usr/bin/env python
#
#    test_utils.py: unit tests for vyconf.utils functions
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
import unittest

import vyconf.utils as vu


class TestVyconfUtils(unittest.TestCase):

    def test_merge_with_status_nonempty(self):
        old = [1, 2, 3]
        new = [2, 3, 4]
        self.assertEqual(vu.merge_with_status(old, new),
                         [(vu.DELETED, 1),
                          (vu.UNCHANGED, 2),
                          (vu.UNCHANGED, 3),
                          (vu.ADDED, 4)])

    def test_merge_with_status_old_empty(self):
        old = []
        new = [1, 2]
        self.assertEqual(vu.merge_with_status(old, new),
                         [(vu.ADDED, 1), (vu.ADDED, 2)])

    def test_merge_with_status(self):
        old = [1, 2]
        new = []
        self.assertEqual(vu.merge_with_status(old, new),
                         [(vu.DELETED, 1), (vu.DELETED, 2)])
