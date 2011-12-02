OpenSpending Model / Data Validator
===================================

This command-line tool will help to check the validity of an OpenSpending
dataset model before loading the data into the system. For this purpose, 
both model files and data files can be checked to see if they would pass
the input validation of an OpenSpending import.

Examples
--------

To validate a JSON model file, use the 'model' subcommand::

  osvalidate model mymodel.json

Or, to check that a CSV sheet satisfies the requirements of an existing
model, use the 'data' subcommand::

  osvalidate data --model mymodel.json BigData.csv

Both commands will emit error messages whenever they find an inconsistency
but otherwise try to continue the validation. Note, however, that a valid
model file is required to run the data validator.


Upgrading the Format
--------------------

The model schema changes from time to time, so a migration option is 
provided so that existing files can be upgraded::

  osvalidate migrate old.json >new.json 

This will attempt to execute pending migrations and set an appropriate 
model version.

Schema / Format
---------------

The JSON model format is described in further detail in the documentation_.

.. _documentation: http://readthedocs.org/docs/openspending/en/latest/model/design.html#modeling-mapping-schema

Installation
------------

Installation is as a conventional Python tool:

  virtualenv --no-site-packages pyenv
  . pyenv/bin/activate
  python setup.py install


Contact
-------

* E-Mail: info@openspending.org
* Issues: https://github.com/okfn/openspending/issues


