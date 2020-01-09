# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools


class python-jsonconversionConan(ConanFile):

        # ######################################################### #
    #                package meta-information
    # ######################################################### #

    # * package name (string) [required]
    #       name of the package
    name = "python-jsonconversion"

    # * author (string) [required]
    #       package provider (and maintainer)
    author = "Franz Steinmetz <franz.steinmetz@dlr.de>"

    # * license (string) [recommended]:
    #       please use the "official" licence identifier
    #       you can lookup the identifier on https://spdx.org/licenses/
    license = "<license_identifier>"

    # * url (string) [required]
    #       url to internal rmc-github repository
    url = "https://rmc-github.robotic.dlr.de/common/python-jsonconversion"

    # * homepage (string) [recommended]
    #       url to project page for containing more documentation
    homepage = "<url of homepage>"

    # * description (string) [recommended]
    description = "<Description of Testproject here>"

    # * topics (tuple of strings) [optional]:
    #       tags that describe the package
    #       e.g. topics = ("<Put some tag here>", "<here>", "<and here>")
    topics = ()

    # * requires (list) [optional]
    #       package (runtime) dependecies
    #       use conan syntax, e.g. "OtherLib/2.1@otheruser/testing"
    #
    requires = []

    # * build_requires (list) [optional]
    #       package (build) dependecies, i.e.
    #       all packages that are need for build
    #       but not in 'requires'.
    #       use conan syntax, e.g. "OtherLib/2.1@otheruser/testing"
    #
    build_requires = []

    # ######################################################### #
    #               build system information
    # ######################################################### #

    # * settings (tuple of strings) [recommended]:
    #       defines ???
    #default: ???
    settings = "os", "compiler", "build_type", "arch"

    # * export_sources (array of filesU/pattern) [required]:
    #       defines all files that are part of the source package
    # default: export everything in the directory that is not excluded by .gitignore
    exports_sources = ["*", "!.gitignore"] + ["!%s" % x for x in tools.Git().excluded_files()]

    # * options (dict of <option key : <value range>) [optional]:
    #       defines options that are made public
    #       e.g. options = {"shared": [True, False]}
    # default: empty
    options = {}

    # * default_options (dict of <option key> ; <default value>) [optional]:
    #       specifies the default value for all options
    #       e.g. default_options = {"shared": False}
    # default: empty
    default_options = {}

    # * source_dir (path):
    #       path to sources
    source_dir = "."


    # ######################################################### #
    #            common functions for building and packaging
    # ######################################################### #

    #
    # source function:
    #       this function is used for providining and manipulating the source files
    #       using the cissy-3rdpyart-cli, the source is already available in a
    #       subfolder, defined by 'self.source_dir' (default folder is 'source').
    #       the functions automatically applies all patches that are found in a
    #       'patches' subfolder.
    #       (see https://docs.conan.io/en/latest/reference/conanfile/methods.html#source)
    #
    def source(self):
        pass


    # package_info function:
    #       Finally, the package_info() method defines
    #       e.g. that a consumer must link with a certain library when using this package.
    #       Other information as include or lib paths can be defined as well.
    #       (see https://docs.conan.io/en/latest/reference/conanfile/methods.html#package-info)
    #
    def package_info(self):
        # examples:
        # self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        # self.cpp_info.libs = []  # The libs to link against
        # self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        # self.cpp_info.resdirs = ['res']  # Directories where resources, data, etc can be found
        # self.cpp_info.bindirs = ['bin']  # Directories where executables and shared libs can be found
        # self.cpp_info.srcdirs = []  # Directories where sources can be found (debugging, reusing sources)
        # self.cpp_info.defines = []  # preprocessor definitions
        # self.cpp_info.cflags = []  # pure C flags
        # self.cpp_info.cxxflags = []  # C++ compilation flags
        # self.cpp_info.sharedlinkflags = []  # linker flags
        # self.cpp_info.exelinkflags = []  # linker flags

        #
        # at least define required libraries
        #
        # self.cpp_info.libs = []
        pass


    #
    # add python_interpreter
    #
    options += {"python_interpreter": ["python2", "python3"]}
    default_options += {"python_interpreter": "python2"}

    # ######################################################### #
    #        python specific functions and variables
    # ######################################################### #

    #
    # necesseray generators:
    #       virtualbuildenv generates an shell environment with all neccessary flags
    #       (see https://docs.conan.io/en/latest/reference/generators/virtualbuildenv.html)
    #
    generators = "virtualbuildenv"

    def get_python_version(self):
        pass


    # build function:
    #       the build() should configure and build the project
    #       (see https://docs.conan.io/en/latest/reference/conanfile/methods.html#build)
    #
    def build(self):
        #
        # call python setup.py build
        #
        self.run("{python} setup.py build {source}".format(python=self.options.python_interpreter.value, source=self.source_dir))


    # package function:
    #       The package() method should copy artifacts (headers, libs)
    #       from the build folder to the final package folder.
    #       (see https://docs.conan.io/en/latest/reference/conanfile/methods.html#package)
    #
    def package(self):
        #
        # call python setup.py install
        #
        self.run("{python} setup.py build --prefix . {source}".format(python=self.options.python_interpreter.value, source=self.source_dir))

