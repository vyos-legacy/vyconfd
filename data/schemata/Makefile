RNG2RNC = ../../scripts/rnc2rng.sh
INTERFACE_RNC = interface_definition.rnc
INTERFACE_RNG = interface_definition.rng

interface_definition.rng: $(INTERFACE_RNC)
	$(RNG2RNC) interface_definition.rnc interface_definition.rng

all: $(INTERFACE_RNG)
