# Copyright

from setuptools import setup, find_packages


setup(
    name='jsonconversion',
    version='0.2.0',
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

    python_requires='<=2.7',
    setup_requires=['pytest-runner'],
    install_requires=[],
    tests_require=['pytest', 'numpy'],

    zip_safe=True
)
