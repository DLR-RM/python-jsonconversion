import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


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
    name='jsonconversion',
    version='0.1.12',
    url='https://rmc-github.robotic.dlr.de/common/python-jsonconversion',
    license='BSD',
    author='Franz Steinmetz',
    maintainer='Franz Steinmetz',
    author_email='franz.steinmetz@dlr.de',
    maintainer_email='franz.steinmetz@dlr.de',
    description='This python module helps converting arbitrary Python objects into JSON strings and back.',
    keywords=('json', 'conversion', 'serialization'),

    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},   # tell distutils packages are under src

    install_requires=[],
    tests_require=['pytest', 'numpy'],

    cmdclass={'test': PyTest},
)
