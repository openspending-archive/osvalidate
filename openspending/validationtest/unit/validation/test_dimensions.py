from colander import Invalid 

from ... import TestCase, helpers as h

from openspending.validation.model.dimensions import dimensions_schema
from openspending.validation.model.common import ValidationState

class TestDimensions(TestCase):

    def setup(self):
        self.model = h.model_fixture('default')
        self.state = ValidationState(self.model)

    def test_basic_validate(self):
        try:
            in_ = self.model['dimensions']
            schema = dimensions_schema(self.state)
            out = schema.deserialize(in_)
            assert len(out)==len(in_), out
        except Invalid, i:
            assert False, i.asdict()
    
    @h.raises(Invalid)
    def test_invalid_name(self):
        ms = self.model['dimensions']
        ms['ba nana'] = ms['function']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_no_label(self):
        ms = self.model['dimensions'].copy()
        del ms['function']['label']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_requires_one_key_column(self):
        ms = self.model['dimensions'].copy()
        del ms['function']['key']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)

    @h.raises(Invalid)
    def test_requires_time(self):
        ms = self.model['dimensions'].copy()
        del ms['time']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_requires_time_date_datatype(self):
        ms = self.model['dimensions'].copy()
        ms['time']['datatype'] = 'string'
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_requires_amount(self):
        ms = self.model['dimensions'].copy()
        del ms['amount']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_requires_amount_float_datatype(self):
        ms = self.model['dimensions'].copy()
        ms['amount']['datatype'] = 'string'
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_id_overlap(self):
        ms = self.model['dimensions'].copy()
        ms['function_id'] = ms['function']
        model = self.model.copy()
        model['dimensions'] = ms
        state = ValidationState(model)
        schema = dimensions_schema(state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_measure_has_column(self):
        ms = self.model['dimensions'].copy()
        del ms['cofinance']['column']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_measure_data_type(self):
        ms = self.model['dimensions'].copy()
        ms['cofinance']['datatype'] = 'id'
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_date_has_column(self):
        ms = self.model['dimensions'].copy()
        del ms['time']['column']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_date_data_type(self):
        ms = self.model['dimensions'].copy()
        ms['time']['datatype'] = 'id'
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_attribute_has_column(self):
        ms = self.model['dimensions'].copy()
        del ms['transaction_id']['column']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_attribute_data_type(self):
        ms = self.model['dimensions'].copy()
        ms['transaction_id']['datatype'] = 'banana'
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_has_fields(self):
        ms = self.model['dimensions'].copy()
        del ms['function']['attributes']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_field_has_name(self):
        ms = self.model['dimensions'].copy()
        del ms['function']['attributes']['name']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_field_reserved_name(self):
        ms = self.model['dimensions'].copy()
        ms['function']['attributes']['id'] = ms['function']['attributes']['description']
        del ms['function']['attributes']['description']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_field_invalid_name(self):
        ms = self.model['dimensions'].copy()
        ms['function']['attributes']['ba nanana'] = ms['function']['attributes']['description']
        del ms['function']['attributes']['description']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_field_has_column(self):
        ms = self.model['dimensions'].copy()
        del ms['function']['attributes']['description']['column']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_field_has_datatype(self):
        ms = self.model['dimensions'].copy()
        del ms['function']['attributes']['description']['datatype']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_field_invalid_datatype(self):
        ms = self.model['dimensions'].copy()
        ms['function']['attributes']['description']['datatype'] = 'banana'
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_field_name_not_datatype_id(self):
        ms = self.model['dimensions'].copy()
        ms['function']['attributes']['name']['datatype'] = 'string'
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_field_label_not_datatype_string(self):
        ms = self.model['dimensions'].copy()
        ms['function']['attributes']['label']['datatype'] = 'float'
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)
    
    @h.raises(Invalid)
    def test_compound_must_have_name(self):
        ms = self.model['dimensions'].copy()
        del ms['function']['attributes']['name']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)

    @h.raises(Invalid)
    def test_compound_must_have_label(self):
        ms = self.model['dimensions'].copy()
        del ms['function']['attributes']['label']
        schema = dimensions_schema(self.state)
        schema.deserialize(ms)


