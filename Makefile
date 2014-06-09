#    vyconf/Makefile: top level makefile.
#
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


SCHEMA_DIR = data/schemata
RNC2RNG = scripts/rnc2rng.sh
INTERFACE_RNC = $(SCHEMA_DIR)/interface_definition.rnc
INTERFACE_RNG = $(SCHEMA_DIR)/interface_definition.rng

$(INTERFACE_RNG): $(INTERFACE_RNC)
	$(RNC2RNG) $(INTERFACE_RNC) $(INTERFACE_RNG)

.PHONY: schema
schema: $(INTERFACE_RNG)

.PHONY:	test
test: schema
	scripts/runtests.sh

.PHONY:	all
all: schema
