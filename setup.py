# Copyright

from setuptools import setup, find_packages


setup(
    name='jsonconversion',
    version='0.2.2',
    url='https://github.com/DLR-RM/python-jsonconversion',
    download_url='https://github.com/DLR-RM/python-jsonconversion/archive/0.2.2.tar.gz',
    license='BSD',
    author='Franz Steinmetz',
    maintainer='Franz Steinmetz',
    author_email='franz.steinmetz@dlr.de',
    maintainer_email='franz.steinmetz@dlr.de',
    description='This python module helps converting arbitrary Python objects into JSON strings and back.',
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
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: Utilities'
    ],

    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},   # tell distutils packages are under src

    python_requires='<=2.7',
    setup_requires=['pytest-runner'],
    install_requires=[],
    tests_require=['pytest', 'numpy'],

    zip_safe=True
)
