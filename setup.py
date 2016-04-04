from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from os import path
import sys


def read_version_from_pt_file():
    pt_file_name = 'python-jsonconversion.pt'
    pt_file_path = path.join(path.dirname(path.realpath(__file__)), pt_file_name)
    with open(pt_file_path) as pt_file:
        for line in pt_file:
            if line.strip().startswith('VERSION'):
                parts = line.split('=')
                version = parts[1].strip()
                return version
    return 0


class PyTest(TestCommand):
    """Run py.test with JSON conversion tests

    Copied from https://pytest.org/latest/goodpractises.html#integrating-with-setuptools-python-setup-py-test
    """
    # This allows the user to add custom parameters to py.test, e.g.
    # python setup.py test -a "-v"
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['-xs']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        error_number = pytest.main(self.pytest_args)
        sys.exit(error_number)



setup(
    name='JSON Conversion',
    version=read_version_from_pt_file(),
    url='https://rmc-github.robotic.dlr.de/common/python-jsonconversion',
    license='LGPL',
    author='Franz Steinmetz',
    maintainer='Franz Steinmetz',
    author_email='franz.steinmetz@dlr.de',
    maintainer_email='franz.steinmetz@dlr.de',
    description='This python module helps converting arbitrary Python objects into JSON strings and back.',
    keywords=('json', 'conversion', 'serialization'),

    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},   # tell distutils packages are under src

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires=['json'],

    tests_require=['pytest'],

    cmdclass={'test': PyTest},
)
