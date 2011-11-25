import os

from setuptools import setup, find_packages
from openspending.validation import __version__


setup(
    name='osvalidate',
    version=__version__,
    description='OpenSpending Model/Data Validation',
    author='Open Knowledge Foundation',
    author_email='openspending-dev at lists okfn org',
    url='http://github.com/okfn/osvalidate',

    install_requires=[
        "colander==0.9.3",
        "Unidecode==0.04.9",
        "messytables==0.1.2"
    ],
    setup_requires=[
        "nose==1.1.2"
    ],
    license='GPLv3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'validationtest']),
    include_package_data=True,
    namespace_packages = ['openspending', 'openspending.validation',
       'openspending.validationtest', 'openspending.validationcli'],
    test_suite='nose.collector',
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'osvalidate = openspending.validationcli:main'
        ]
    }
)
