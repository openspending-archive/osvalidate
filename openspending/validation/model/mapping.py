from openspending.validation.model.common import mapping
from openspending.validation.model.common import key
from openspending.validation.model.predicates import chained, \
        nonempty_string

def keys_in_attributes(state):
    def _validator(mapping):
        for key in mapping:
            if key not in state.attributes:
                return "Mapping defined value for non-existing attribute: %s" % key
        return True
    return _validator

def attribute_schema(name, state):
    schema = mapping(name, validator=chained(
        ))
    schema.add(key('column', validator=chained(
            nonempty_string,
        )))
    return schema

def mapping_schema(state):
    schema = mapping('mapping', validator=keys_in_attributes(state))
    for name in state.attributes:
        schema.add(attribute_schema(name, state))
    return schema
