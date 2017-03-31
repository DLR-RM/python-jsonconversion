# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

import __builtin__
from pydoc import locate, ErrorDuringImport
from inspect import isclass


def string2type(string_value):
    """Converts a string into a type or class

    :param string_value: the string to be converted, e.g. "int"
    :return: The type derived from string_value, e.g. int
    """
    # If the parameter is already a type, return it
    if isinstance(string_value, type) or isclass(string_value):
        return string_value

    # Special case, which cannot be handled otherwise
    if string_value == "NoneType" or string_value == "__builtin__.NoneType":
        return type(None)

    # Get object associated with string
    # First check whether we are having a built in type (int, str, etc)
    if hasattr(__builtin__, string_value):
        obj = getattr(__builtin__, string_value)
        if type(obj) is type:
            return obj

    if isinstance(string_value, basestring) and '.' in string_value:
        return get_class_from_qualified_name(string_value)

    # If not, try to locate the module
    try:
        obj = locate(string_value)
    except ErrorDuringImport as e:
        raise ValueError("Unknown type '{0}'".format(e))

    # Check whether object is a type
    if type(obj) is type:
        return locate(string_value)

    # Check whether object is a class
    if isclass(obj):
        return obj

    # Raise error if none is the case
    raise ValueError("Unknown type '{0}'".format(string_value))


def get_qualified_name_for_class(obj):
    return obj.__module__ + '.' + obj.__name__


def get_qualified_name_for_class_object(obj):
    return obj.__module__ + '.' + obj.__class__.__name__


def get_class_from_qualified_name(qualified_name):
    parts = qualified_name.split('.')
    module_name = ".".join(parts[:-1])
    # First ensure, that the module is imported
    cls = __import__(module_name)
    # Find nested class
    for comp in parts[1:]:
        cls = getattr(cls, comp)
    return cls
