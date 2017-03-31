# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

from json.encoder import JSONEncoder, _make_iterencode, encode_basestring_ascii, FLOAT_REPR, INFINITY, \
    encode_basestring
from inspect import isclass
from types import ClassType
try:
    import numpy as np
except ImportError:
    np = False

from jsonconversion.jsonobject import JSONObject
from jsonconversion.conversion import get_qualified_name_for_class_object, get_qualified_name_for_class


class JSONExtendedEncoder(JSONEncoder):

    def isinstance(self, obj, cls):
        """Custom isinstance method

        Override this method if you want to custom treatment for classes inheriting from builtins such as `dict` or
        `list`. Returning `False` for these classes, causes the `default` method to be called for the object. See
        `JSONObjectEncoder` for an example on how to make use of this.

        :param obj: Object to be encoded
        :param cls: Class which is checked for
        :return: `True` if `obj` is an instance of `cls`, `False` else
        :rtype: False
        """
        return isinstance(obj, cls)

    def iterencode(self, o, _one_shot=False):
        """This is almost a copy of the base class implementation of this method

        The changes are inspired by http://stackoverflow.com/a/17684652
        The execution might be slower than that of the base class, as the `c_make_encoder` is never called. However,
        the changes allow the implementation of a custom `isinstance` method.
        """
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = encode_basestring_ascii
        else:
            _encoder = encode_basestring
        if self.encoding != 'utf-8':
            def _encoder(o, _orig_encoder=_encoder, _encoding=self.encoding):
                if isinstance(o, str):
                    o = o.decode(_encoding)
                return _orig_encoder(o)

        def floatstr(o, allow_nan=self.allow_nan, _repr=FLOAT_REPR, _inf=INFINITY, _neginf=-INFINITY):
            # Check for specials.  Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on the
            # internals.

            if o != o:
                text = 'NaN'
            elif o == _inf:
                text = 'Infinity'
            elif o == _neginf:
                text = '-Infinity'
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError("Out of range float values are not JSON compliant: " + repr(o))

            return text

        _iterencode = _make_iterencode(
            markers, self.default, _encoder, self.indent, floatstr,
            self.key_separator, self.item_separator, self.sort_keys,
            self.skipkeys, _one_shot, isinstance=self.isinstance)
        return _iterencode(o, 0)


class JSONObjectEncoder(JSONExtendedEncoder):
    """Custom JSON encoder class especially for state machines

    This JSON encoder class inherits from the basic JSON encoder class. It can encode all classes deriving from
    JSONObject. In addition, tuples (encoded by :py:class:`JSONObjectEncoder`) are maintained and type objects (e.g.
    int, object, float) are handled. Finally, it is tried to convert dictionary keys to integers.
    """

    def __init__(self, **kwargs):
        for key in ['use_decimal', 'namedtuple_as_object', 'tuple_as_array', 'bigint_as_string', 'item_sort_key',
                    'for_json', 'ignore_nan']:
            try:
                del kwargs[key]
            except KeyError:
                pass
        super(JSONObjectEncoder, self).__init__(**kwargs)
        
    def isinstance(self, obj, cls):
        if isinstance(obj, (set, tuple)):
            return False
        return super(JSONObjectEncoder, self).isinstance(obj, cls)

    def default(self, obj):
        """This method is called after all base class encoding logic

        Here, additional conversions of objects to dictionaries can be defined. Both JSONObject and type objects are
        treated.

        :param obj: Object to be converted to a dictionary
        :return: Dictionary representing the given object
        :rtype: dict
        """
        if isinstance(obj, JSONObject):
            # to_dict must be implemented by classes deriving from JSONObject
            dictionary = obj.to_dict()
            dictionary['__jsonqualname__'] = get_qualified_name_for_class_object(obj)
            return dictionary

        elif isinstance(obj, (type, ClassType)):
            if isclass(obj):
                return {'__type__': get_qualified_name_for_class(obj)}
            return {'__type__': obj.__name__}

        if isinstance(obj, set):
            dictionary = {'__jsonqualname__': '__builtin__.set',
                          'items': list(obj)}
            return dictionary

        if isinstance(obj, tuple):
            dictionary = {'__jsonqualname__': '__builtin__.tuple',
                          'items': list(obj)}
            return dictionary

        elif np and isinstance(obj, np.ndarray):
            return {'__jsonqualname__': "numpy.ndarray", "items": obj.tolist()}

        else:
            return super(JSONObjectEncoder, self).default(obj)
