#!/usr/bin/env python
"""
cloudydict 
======


Right now cloud file access in Python is about where database access
was in the mid 90's.  Each database wrapper author has their very own
nomenclature, sets of commands for doing things that are basically the
same - creating cursors, executing commands and reading rows.


cloudydict seeks to do for cloud file providers what the Python
Database API does for database access.  Cloud file style servces like
Rackspace's cloud files and Amazon's S3 really are nothing more than
dictionaries that map fixed strings to

"""

from setuptools import setup

setup(
    name='cloudydict',
    version='0.0.10',
    author='Adam DePrince',
    author_email='adeprince@nypublicradio.org',
    description='Dictionary interface to cloud providers.',
    long_description=__doc__,
    py_modules=[
        "cloudydict/__init__",
        "cloudydict/s3",
        "cloudydict/common",
        "cloudydict/cloudfiles",
        "cloudydict/django_storage",
    ],
    # packages=["cloudydict "],
    zip_safe=True,
    license='GPL',
    include_package_data=True,
    classifiers=[
    ],
    scripts=[
    ],
    url="https://github.com/wnyc/cloudydict ",
    install_requires=[
        "boto",
        "python-cloudfiles",
        # "appengine",
    ]
)
