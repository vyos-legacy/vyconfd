# vyconf.types.base: base type validators everyone is likely to need
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

import re

from vyconf.types import types


class StringValidator(types.TypeValidator):
    """Validator for string values."""

    name = "string"

    def __init__(self):
        super(StringValidator, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        if not isinstance(value, str):
            raise types.ValidationError(
                "'%s' is not a valid string" % str)

        if constraint:
            if not isinstance(constraint, str):
                # If we take a precompiled regex, how are we going to issue
                # a meaningful error message?
                raise types.ConstraintFormatError(
                    "Constraint must be a string")
            try:
                constraint_re = re.compile(constraint)
            except Exception:
                raise types.ConstraintFormatError(
                    "'%s' is not a valid constraint for type '%s'" %
                    (self.to_string_safe(constraint), self.name))

            # Check the value against constraint
            # XXX: do we need to force strict ^...$ match here?
            if not re.match(constraint_re, str(value)):
                raise types.ValidationError(
                    "'%s' does not match pattern '%s'" % (value, constraint))
            else:
                return True
        else:
            return True


class IntegerValidator(types.TypeValidator):
    """Validates unsigned integer values """
    name = "integer"

    __range_re_str = """
        (?: # xx-yy range group and separator, comma or end of line
        (?: # xx-yy range group
        (?P<start>\d+)
        \-
        (?P<stop>\d+)
        (?:,|$))+?)
    """

    def in_range(value, min, max):
        if not ((value >= min) and (value <= max)):
            return True

    @classmethod
    def validate(self, value, constraint=None):
        """Validate an integer. Takes either string representation or
           actual integer
        """
        if (not isinstance(value, str)) and (not isinstance(value, int)):
            raise types.ValidationError(
                "'%s' is not a valid integer" % self.to_string_safe(value))

        value_int = None
        if isinstance(value, str):
            try:
                value_int = int(value)
            except Exception:
                # Likely ValueError, but we don't really care which error
                # it was
                raise types.ValidationError(
                    "{0} is not a valid integer".format(value, self.name))
        else:
            value_int = value

        if value_int < 0:
            # Anyone wants negative integers in configs?
            raise types.ValidationError(
                "\"{0}\" is not a non-negative integer")

        if constraint:
            if not isinstance(constraint, str):
                raise types.ConstraintFormatError(
                    "Constraint must be a string")

            # XXX: needs really strict validation?
            range_re = re.compile(self.__range_re_str, re.VERBOSE)
            if not range_re.match(constraint):
                raise types.ConstraintFormatError(
                    "'%s' is not a valid constraint for type '%s." %
                    (constraint, self.name))

            # That regex returns ('min', 'max') tuples, convert content to
            # integers
            ranges = map(lambda x: (int(x[0]), int(x[1])),
                         range_re.findall(constraint))
            data = map(lambda x: True if x[0] <= value_int <= x[1] else
                       False, ranges)
            if True not in data:
                raise types.ValidationError(
                    "'%s' does not fall in range '%s'" % (value, constraint))

        # If no exceptions were raised by this time, everything is fine
        return True
