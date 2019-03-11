# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

from setuptools import setup
from os import path

# Get the long description from README.rst
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='jsonconversion',
    version='0.2.10',
    url='https://github.com/DLR-RM/python-jsonconversion',
    download_url='https://github.com/DLR-RM/python-jsonconversion/tarball/master',
    license='BSD',
    author='Franz Steinmetz',
    maintainer='Franz Steinmetz',
    author_email='franz.steinmetz@dlr.de',
    maintainer_email='franz.steinmetz@dlr.de',
    description='This python module helps converting arbitrary Python objects into JSON strings and back.',
    long_description=long_description,
    keywords=('json', 'conversion', 'serialization'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Flask',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: Utilities'
    ],

    packages=['jsonconversion'],
    package_dir={'': 'src'},  # tell distutils packages are under src

    python_requires='>=2.6',
    setup_requires=['pytest-runner'],
    install_requires=[],
    tests_require=['pytest', 'numpy'],

    zip_safe=True
)
