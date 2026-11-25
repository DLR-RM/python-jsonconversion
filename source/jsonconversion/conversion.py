# Copyright (C) 2016-2026 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>
# Johannes Ernst <j.ernst@dlr.de>
#
# Code refinement and review were performed with the assistance of generative AI.


import sys
from importlib import import_module
from pydoc import locate, ErrorDuringImport
from inspect import isclass

from jsonconversion import basestring, builtins, PY2_BUILTINS_STR, PY3_BUILTINS_STR


def string2type(string_value, allow_untrusted=False):
    """Converts a string into a type or class

    Make sure to use the allow_untrusted flag only with secure imports!

    :param string_value: the string to be converted, e.g. "int"
    :param allow_untrusted: flag to allow to import and locate untrusted classes or types
    :return: The type derived from string_value, e.g. int
    """
    # If the parameter is already a type, return it
    if isinstance(string_value, type) or isclass(string_value):
        return string_value

    # Special case, which cannot be handled otherwise
    if string_value.endswith('NoneType'):
        return type(None)

    # Get object associated with string
    # First check whether we are having a built in type (int, str, etc)
    if hasattr(builtins, string_value):
        obj = getattr(builtins, string_value)
        if type(obj) is type:
            return obj

    if allow_untrusted:
        if isinstance(string_value, basestring) and '.' in string_value:
            return get_class_from_qualified_name(string_value, allow_untrusted=allow_untrusted)

        # If not, try to locate the module
        try:
            obj = locate(string_value)
        except ErrorDuringImport as e:
            raise ValueError(f"Unrecognized serialized type '{e}'")

        # Check whether object is a type
        if type(obj) is type:
            return locate(string_value)

        # Check whether object is a class
        if isclass(obj):
            return obj

    # Raise error if none is the case
    raise ValueError(f"Not allowed to import untrusted class: {string_value}")


def get_qualified_name_for_class(obj, builtins_str=None):
    global PY2_BUILTINS_STR, PY3_BUILTINS_STR
    module = obj.__module__
    if module in (PY2_BUILTINS_STR, PY3_BUILTINS_STR):
        module = builtins_str
    return module + '.' + obj.__qualname__


def get_qualified_name_for_class_object(obj, builtins_str=None):
    global PY2_BUILTINS_STR, PY3_BUILTINS_STR
    module = obj.__module__
    if module in (PY2_BUILTINS_STR, PY3_BUILTINS_STR):
        module = builtins_str
    return module + '.' + obj.__class__.__qualname__


def get_class_from_qualified_name(qualified_name, allow_untrusted=False):
    ''' This tries to import the package specified in qualified name (except for builtins).

    Make sure to use the allow_untrusted flag only with secure imports!
    '''
    parts = qualified_name.split('.')
    module_name = ".".join(parts[:-1])
    # First ensure, that the module is imported
    if module_name in ['builtins', '__builtin__']:
        return getattr(builtins, parts[-1])
    if not allow_untrusted:
        raise ValueError(f"Not allowed to import untrusted class: {qualified_name}")
    # The qualified name is "<module>.<qualname>" and the qualname can contain dots for nested classes, so
    # the module is the longest importable prefix; the remaining components are attributes (nested classes)
    for split in range(len(parts) - 1, 0, -1):
        module_name = ".".join(parts[:split])
        try:
            cls = import_module(module_name)
        except ModuleNotFoundError as e:
            # Only skip prefixes that are not modules; re-raise failures of imports within an existing module
            if e.name is None or not (module_name + '.').startswith(e.name + '.'):
                raise
            continue
        # Find nested class
        for comp in parts[split:]:
            cls = getattr(cls, comp)
        return cls
    raise ValueError(f"Cannot import module for class: {qualified_name}")