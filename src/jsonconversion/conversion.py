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
    if string_value == "NoneType":
        return type(None)

    # Get object associated with string
    # First check whether we are having a built in type (int, str, etc)
    if hasattr(__builtin__, string_value):
        obj = getattr(__builtin__, string_value)
        if type(obj) is type:
            return obj

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
