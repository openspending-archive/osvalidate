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

You can generate a bare mapping from a JSON model file using::

  osvalidate mapping mymodel.json

If you don't have a JSON model file, you can generate one from a CSV file
as follows::

  osvalidate mapgen data.csv

You will need to edit the result of this to add information (like textual
explanations of the fields) can't be programmatically inferred from the
contents of the CSV file.


Installation
------------

Installation is as a conventional Python tool::

  virtualenv pyenv

  . pyenv/bin/activate

  python setup.py install

Developer notes
---------------

Each new version of ``osvalidate`` needs to be published in a few steps:

* Update the version in ``setup.py`` to a new release of the form
  ``YYYY-MM-DD.SS`` with the last two digits signifying a serial number for the
  day.
* Commit and push the new release to the GitHub repository.
* Upload a source distribution to pypi (``python setup.py sdist upload``).
* Update the required version of ``osvalidate`` in the main ``openspending``
  app.

How to write a migration - Migrations of model formats are simple functions, 
usually named ``mYYYY_MM_DD_purpose`` and stored in the ``migrations`` module.
They must both accept and return a model file and be registered in
``openspending.validation.model.migration:MIGRATIONS`` with an increasing
version stamp (i.e. the current date). The version stamp of the latest executed 
migration will automatically be saved to the model and used as a minimum for 
the next run. 

In general, migrations should make as few assumptions about the input they 
receive as possible and execute idempotently. Migrations cannot change the 
``dataset`` section of the model.

Contact
-------

* E-Mail: info@openspending.org
* Issues: https://github.com/openspending/openspending/issues


