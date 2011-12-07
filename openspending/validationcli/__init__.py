# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)



import argparse
import sys
import json

from openspending.validationcli.udr import UnicodeDictReader

DESCRIPTION = "Validation tools for local checks of OpenSpending " \
              "model and data files."
parser = argparse.ArgumentParser('osvalidate', description=DESCRIPTION)
parsers = parser.add_subparsers(title='Validators')


def _validate_model(file_name):
    from colander import Invalid
    from openspending.validation.model import validate_model
    try:
        fh = open(file_name, 'rb')
        model = json.load(fh)
        return validate_model(model)
    except Invalid as errors:
        for field, error in errors.asdict().items():
            message = "[%s]:\n\t%s\n" % (field, error)
            print message.encode('utf-8')
    except Exception as ex:
        print unicode(ex).encode('utf-8')

def mapping(args):
    with file(args.json_file) as fh:
        data = json.load(fh)
        print json.dumps(data["mapping"], indent=2)
    return 0

def mapping_gen(args):
    from openspending.validation.model import mapping
    mapping.dump_mapping(args.csv_file)
    return 0

def model(args):
    model = _validate_model(args.json_file)
    if model is None:
        return 1
    print "OK: data model is valid."
    return 0

def migrate(args):
    from openspending.validation.model.migration import migrate_model
    fh = open(args.json_file, 'rb')
    model = json.load(fh)
    model = migrate_model(model)
    print json.dumps(model, indent=2, encoding='utf-8')
    return 0

def data(args):
    from colander import Invalid
    from openspending.validation.data import convert_types
    return_code = 0
    model = _validate_model(args.model)
    if model is None:
        return 1
    try:
        fh = open(args.csv_file, 'rb')
        for line in UnicodeDictReader(fh):
            try:
                convert_types(model['mapping'], line)
            except Invalid as errors:
                return_code = 1
                for error in errors.children:
                    value = error.value
                    if value and len(value) > 70:
                        value = value[:66] + ' ...'
                    message = "[Column '%s' -> Attribute '%s' " \
                        "(%s)]\n\t%s\n\t(Value: %s)\n" % (
                            error.column, error.node.name, 
                            error.datatype, error.msg,
                            value)
                    print message.encode('utf-8')
    except Exception as ex:
        print unicode(ex).encode('utf-8')
        return 1
    if not return_code:
        print "OK: data validates for the model."
    return return_code

model_parser = parsers.add_parser('model',
                    help='Check a JSON model file',
                    description='This will validate the model is valid.')
model_parser.add_argument('json_file', help="JSON model document.")
model_parser.set_defaults(func=model)


mapping_parser = parsers.add_parser('mapping',
                    help='Extract the mapping from a JSON model file',
                    description='This will extract the mapping stanza from the model.')
mapping_parser.add_argument('json_file', help="JSON model document.")
mapping_parser.set_defaults(func=mapping)


mapgen_parser = parsers.add_parser('mapgen',
                    help='Generate the mapping from a CSV data file',
                    description='This will (attempt to) generate the mapping stanza from the CSV file.')
mapgen_parser.add_argument('csv_file', help="CSV data file.")
mapgen_parser.set_defaults(func=mapping_gen)


migrate_parser = parsers.add_parser('migrate',
                    help='Migrate a JSON model file to the latest schema',
                    description="This will attempt to update the model to " \
                        "the current schema.")
migrate_parser.add_argument('json_file', help="JSON model document.")
migrate_parser.set_defaults(func=migrate)

data_parser = parsers.add_parser('data',
                    help='Parse a CSV file according to the specified JSON model.',
                    description='You must specify --model.')
data_parser.add_argument('--model', action="store", dest='model',
                    default=None, metavar='json_file',
                    help="File name of JSON format model (metadata and mapping).")
data_parser.add_argument('csv_file', help="CSV file path.")
data_parser.set_defaults(func=data)

def main():
    args = parser.parse_args()
    sys.exit(args.func(args))





