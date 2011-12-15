import datetime

from ... import TestCase, helpers as h
from openspending.validation.data import convert_types

class TestTypes(TestCase):

    def test_convert_types_value(self):
        mapping = {"foo": {"column": "foo"}}
        dimensions = {"foo": {"datatype": "string"}}
        row = {"foo": "bar"}
        out = convert_types(dimensions, mapping, row)
        assert isinstance(out, dict), out
        assert 'foo' in out, out
        assert out['foo']=='bar'

    def test_convert_types_compound(self):
        dimensions = {
                    "foo": {"attributes": {
                        "name": {"datatype": "string"},
                        "label": {"datatype": "string"}
                        }
                    }
                  }
        mapping = {"foo.name": {"column": "foo_name"},
                   "foo.label": {"column": "foo_label"}}
        row = {"foo_name": "bar", "foo_label": "qux"}
        out = convert_types(dimensions, mapping, row)
        assert isinstance(out, dict), out
        assert 'foo' in out, out
        assert isinstance(out['foo'], dict), out
        assert out['foo']['name']=='bar'
        assert out['foo']['label']=='qux'

    def test_convert_types_casting(self):
        dimensions = {"foo": {"datatype": "float"}}
        mapping = {"foo": {"column": "foo"}}
        row = {"foo": "5.0"}
        out = convert_types(dimensions, mapping, row)
        assert isinstance(out, dict), out
        assert 'foo' in out, out
        assert out['foo']==5.0

    def test_convert_dates(self):
        dimensions = {"foo": {"datatype": "date"}}
        mapping = {"foo": {"column": "foo"}}
        row = {"foo": "2010"}
        out = convert_types(dimensions, mapping, row)
        assert out['foo']==datetime.date(2010, 1, 1)
    
        row = {"foo": "2010-02"}
        out = convert_types(dimensions, mapping, row)
        assert out['foo']==datetime.date(2010, 2, 1)
        
        row = {"foo": "2010-02-03"}
        out = convert_types(dimensions, mapping, row)
        assert out['foo']==datetime.date(2010, 2, 3)

        row = {"foo": "2010-02-03Z"}
        out = convert_types(dimensions, mapping, row)
        assert out['foo']==datetime.date(2010, 2, 3)

    def test_convert_dates_custom_format(self):
        dimensions = {
                    "foo": {"format": "%d.%m.%Y", 
                            "datatype": "date"}
                  }
        mapping = {"foo": {"column": "foo"}}
        row = {"foo": "7.5.2010"}
        out = convert_types(dimensions, mapping, row)
        assert out['foo']==datetime.date(2010, 5, 7)

