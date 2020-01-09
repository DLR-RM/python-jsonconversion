# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools


class JSONConversionConan(ConanFile):

    name = "python-jsonconversion"
    author = "Franz Steinmetz <franz.steinmetz@dlr.de>"
    license = "Simplified BSD License"

    url = "https://rmc-github.robotic.dlr.de/common/python-jsonconversion"
    homepage = "https://github.com/DLR-RM/python-jsonconversion"

    description = "Convert arbitrary Python objects into JSON strings and back. "

    topics = (
        "Development Status :: 5 - Production/Stable",
        "Framework :: Flask",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Object Brokering",
        "Topic :: Utilities"
    )

    settings = "os", "arch"

    # export everything in the directory that is not excluded by .gitignore
    exports_sources = ["*", "!.gitignore"] + ["!%s" % x for x in tools.Git().excluded_files()]

    generators = "virtualenv"

    def build(self):
        pass

    def package(self):
        self.copy("*", src="src", dst="site-packages")
        self.copy("test/*")
        self.copy("tox.ini")
        self.copy("LICENSE")

    def package_info(self):
        self.env_info.PYTHONPATH.append(os.path.join(self.package_folder, "site-packages"))

