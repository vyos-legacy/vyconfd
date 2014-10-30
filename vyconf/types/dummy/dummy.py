# vyconf.types.dummy: dummy type validators for demonstration and testing
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

from vyconf.types import types


class AlwaysValid(types.TypeValidator):
    """Dumb type validator which thinks any value is valid"""
    name = "alwaysvalid"

    def __init__(self):
        super(AlwaysValid, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        return True


class NeverValid(types.TypeValidator):
    """Dumb type validator which thinks the value is never valid"""
    name = "nevervalid"

    def __init__(self):
        super(NeverValid, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        raise types.ValidationError(
            "Value '%s' is not a valid value of type '%s'" %
            (value, self.name))


class BadConstraint(types.TypeValidator):
    """Dumb type validator, always complains about constraint format"""
    name = "badconstraint"

    def __init__(self):
        super(BadConstraint, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        raise types.ConstraintFormatError(
            "Constraint string '%s' is not valid for type '%s'" %
            (value, self.name))
