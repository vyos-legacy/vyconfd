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
from vyconf.types import TypeValidator, ValidationError, ConstraintFormatError

class StringValidator(TypeValidator):
    """ Validator for string values """

    name = "string"

    def __init__(self):
       	super(StringValidator, self).__init__()

    @classmethod
    def validate(self, value, constraint=None):
        # Most of objects can be converted to strings,
        # so the fact it has string representation doesn't really
        # mean anything
        value_str = ""
        if not isinstance(value, str):
            # Unlikely to fail, but...
            try:
                value_str = repr(value)
            except:
                pass
            raise ValidationError("\"{0}\" is not a valid value of type \"{1}\"".format(value_str, self.name))

        if constraint:
            if not isinstance(constraint, str):
                # If we take a precompiled regex, how are we going to issue
                # a meaningful error message?
                raise ConstraintFormatError("Constraint must be a string")
            try:
                constraint_re = re.compile(constraint)
            except:
                constraint_str = ""
                try:
                    constraint_str = repr(constraint)
                except:
                    pass
                raise ConstraintFormatError("\"{0}\" is not a valid constraint for type \"{1}\"".format(constraint_str, self.name))

            # Check the value against constraint
            if not re.match(constraint_re, str(value)):
                raise ValidationError("\"{0}\" value does not satisfy constraint \"{1}\"".format(value, constraint))
            else:
                return True
        else:
            return True




