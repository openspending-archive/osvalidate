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
            pass
        except Invalid, i:
            assert False, i.asdict()
    
    @h.raises(Invalid)
    def test_invalid_name(self):
        pass
