import re
from datetime import datetime

from colander import SchemaNode, String, Invalid, Mapping

from openspending.validation.util import slugify


class InvalidData(Invalid):
    """ Subclass of colander.Invalid to describe a data validation
    problem, including source column, dimension name and data type.
    """

    def __init__(self, attribute, column, datatype, value, message):
        node = SchemaNode(String(), name=attribute)
        self.column = column
        self.value = value
        self.datatype = datatype
        super(InvalidData, self).__init__(node, message)


class AttributeType(object):
    """ A attribute type maintains information about the parsing
    and conversion operations possible on the attribute, providing
    methods to check if a type is applicable to a given value and
    to convert a value to the type. """

    def test(self, row, meta):
        """ Test if the value is of the given type. The
        default implementation calls ``cast`` and checks if
        that throws an exception. If the conversion passes, True
        is returned. Otherwise, a message is given back. """
        try:
            self.cast(row, meta)
            return True
        except Exception, e:
            return unicode(e)

    def cast(self, row, meta):
        """ Convert the value to the type. This may throw
        a quasi-random exception if conversion fails (i.e. it is
        assumed that validation was performed before and errors
        were already handled. """
        raise TypeError("No casting method defined!")

    def _column_name(self, meta):
        return meta.get('column')

    def _column_or_default(self, row, meta):
        """ Utility function to handle using either the column 
        field or the default value specified. """
        column_name = self._column_name(meta)
        if not column_name in row:
            raise ValueError("Column '%s' does not exist in source data." %
                    column_name)
        value = row.get(column_name)
        if (value is None) or not len(value.strip()):
            if meta.get('default_value') is not None:
                value = meta.get('default_value')
            else:
                raise ValueError("Column is empty")
        return value

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __hash__(self):
        return hash(self.__class__)

    def __repr__(self):
        return self.__class__.__name__.rsplit('Type', 1)[0]

class StringAttributeType(AttributeType):
    """ Test if the given values can be represented as a 
    string. """

    def cast(self, row, meta):
        value = self._column_or_default(row, meta)
        return unicode(value)

class IdentifierAttributeType(StringAttributeType):
    """ Type for slug fields, i.e. attributes that will be 
    converted to a URI-compatible representation. """

    def cast(self, row, meta):
        value = self._column_or_default(row, meta)
        return slugify(value)

class FloatAttributeType(AttributeType):
    """ Accept floating point values with commas as thousands
    delimiters (anglo-saxon style). """

    RE = re.compile(r'^[0-9-\,]*(\.[0-9]*[Ee]?\+?[0-9]*)?$')

    def cast(self, row, meta):
        value = self._column_or_default(row, meta)
        if not self.RE.match(value):
            raise ValueError("Numbers must only contain digits, periods, "
                             "dashes and commas")
        return float(unicode(value).replace(",", ""))


class DateAttributeType(AttributeType):
    """ Date parsing. """

    def cast(self, row, meta):
        value = unicode(self._column_or_default(row, meta))
        if 'format' in meta and meta['format']:
            try:
                return datetime.strptime(value, meta['format']).date()
            except ValueError:
                raise ValueError("date does not match the specified format (%s)"
                        %  meta['format'])

        for format in ["%Y-%m-%dZ", "%Y-%m-%d", "%Y-%m", "%Y"]:
            try:
                return datetime.strptime(value, format).date()
            except ValueError: pass
        raise ValueError("'%s': invalid date value." % value)


ATTRIBUTE_TYPES = {
    'string': StringAttributeType(),
    'id': IdentifierAttributeType(),
    'float': FloatAttributeType(),
    'date': DateAttributeType()
    }

def _cast(row, meta, attribute_name):
    """ Test if type conversion is possible, otherwise emit an 
    error. """
    datatype = meta['datatype']
    type_ = ATTRIBUTE_TYPES.get(datatype.lower().strip(),
            StringAttributeType())
    test_result = type_.test(row, meta)
    if test_result is not True:
        try:
            value = type_._column_or_default(row, meta)
        except ValueError:
            value = None
        raise InvalidData(attribute_name, type_._column_name(meta),
                          datatype, value, test_result)
    return type_.cast(row, meta)


def convert_types(mapping, row):
    """ Translate a row of input data (e.g. from a CSV file) into the
    structure understood by the dataset loader, i.e. where all 
    dimensions are dicts and all types have been converted. 

    This will validate the incoming data and emit a colander.Invalid
    exception if validation was unsuccessful."""
    out = {}
    errors = Invalid(SchemaNode(Mapping(unknown='preserve')))

    for dimension, meta in mapping.items():
        meta['dimension'] = dimension

        # handle AttributeDimensions, Measures and DateDimensions.
        # this is clever, but possibly not always true.
        if 'column' in meta:
            try:
                out[dimension] = _cast(row, meta, dimension)
            except Invalid, i:
                errors.add(i)

        # handle CompoundDimensions.
        else:
            out[dimension] = {}

            for attribute, ameta in meta.get('attributes', {}).items():
                try:
                    out[dimension][attribute] = \
                            _cast(row, ameta, dimension + '.' +
                                    attribute)
                except Invalid, i:
                    errors.add(i)

    if len(errors.children):
        raise errors

    return out
