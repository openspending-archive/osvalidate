from setuptools import setup, find_packages

setup(
    name='osvalidate',
    version='2012-01-17.01',
    description='OpenSpending Model/Data Validation',
    author='Open Knowledge Foundation',
    author_email='openspending-dev at lists okfn org',
    url='http://github.com/okfn/osvalidate',

    install_requires=[
        "iso8601",
        "colander==0.9.3",
        "Unidecode==0.04.9",
        "messytables==0.1.4"
    ],
    setup_requires=[
        "nose==1.1.2"
    ],
    license='GPLv3',
    packages=find_packages(exclude=['ez_setup', 'openspending.validationtest']),
    include_package_data=True,
    package_data={
        },
    namespace_packages = ['openspending'],
    test_suite='nose.collector',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'osvalidate = openspending.validationcli:main'
        ]
    }
)

