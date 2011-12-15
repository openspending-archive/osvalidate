from colander import Invalid 

from ... import TestCase, helpers as h

from openspending.validation.model.mapping import mapping_schema
from openspending.validation.model.common import ValidationState

class TestMapping(TestCase):

    def setup(self):
        self.model = h.model_fixture('default')
        self.state = ValidationState(self.model)

    def test_basic_validate(self):
        try:
            in_ = self.model['mapping']
            schema = mapping_schema(self.state)
            out = schema.deserialize(in_)
            assert len(out)==len(in_), out
        except Invalid, i:
            assert False, i.asdict()
    
    @h.raises(Invalid)
    def test_invalid_name(self):
        ms = self.model['mapping']
        ms['ba nana'] = ms['transaction_id']
        schema = mapping_schema(self.state)
        schema.deserialize(ms)

    @h.raises(Invalid)
    def test_invalid_name_multiple_dots(self):
        ms = self.model['mapping']
        ms['function.dot.dot'] = ms['function.name']
        schema = mapping_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_non_existing_dimension(self):
        ms = self.model['mapping']
        ms['bla'] = ms['function.name']
        schema = mapping_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_missing_column(self):
        ms = self.model['mapping']
        ms['function.name'] = {}
        schema = mapping_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_column_no_name(self):
        ms = self.model['mapping']
        ms['function.name'] = {'column': ''}
        schema = mapping_schema(self.state)
        schema.deserialize(ms)
