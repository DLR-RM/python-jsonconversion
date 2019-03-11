
The ``jsonconversion`` package
==============================

This python module helps converting arbitrary Python objects into JSON strings and back. It extends the basic features
of the ``JSONEncoder`` and ``JSONDecoder`` classes provided by the native ``json`` package. For this purpose,
``jsonconversion`` ships with these four classes:

The ``JSONObject`` class
------------------------

Your serializable classes should inherit from this class. Hereby, they must implement the methods ``from_dict`` and
``to_dict``. The example further down describes how to do so.

The ``JSONExtendedEncoder`` class
---------------------------------

This is a class used internally by ``JSONObjectEncoder``. However, it can also be used directly, if you do not need the
features of ``JSONObjectEncoder`` but want to implement your own encoders.

The class is especially helpful, if you want custom handling of builtins (``int``, ``dict``, ...) or classes deriving
from builtins. This would not be possible if directly inheriting from ``JSONEncoder``. To do so, override the
``isinstance`` method and return ``False`` for all types you want to handle in the ``default`` method.

If you look at the source code of ``JSONObjectEncoder``, you will see how this can be used.

The ``JSONObjectEncoder`` class
-------------------------------

Encodes Python objects into JSON strings. Supported objects are:

-  Python builtins: ``int``, ``float``, ``str``, ``list``, ``set``, ``dict``, ``tuple``
-  ``type`` objects: ``isinstance(object, type)``
-  All classes deriving from ``JSONObject``

Those objects can of course also be nested!

The ``JSONObjectDecoder`` class
-------------------------------

Decodes JSON strings converted using the ``JSONObjectEncoder`` back to Python objects.

The class adds a custom keyword argument to the ``load[s]`` method: ``substitute_modules``. This parameter takes a
``dict`` in the form ``{"old.module.MyClass": "new.module.MyClass"}``. It can be used if you have serialized
``JSONObject``\s who's module path has changed.

Usage
=====

Using ``jsonconversion`` is easy. You can find further code examples in the ``test`` folder.

Encoding and Decoding
---------------------

In order to encode Python objects with JSON conversion and to later decode them, you have to import the Python module
``json``. The module provides the methods ``dump``/``dumps`` for encoding and ``load``/``loads`` for decoding:

.. code:: python

    import json

    from jsonconversion.decoder import JSONObjectDecoder
    from jsonconversion.encoder import JSONObjectEncoder

    var = (1, 2, 3)  # variable to be serialized

    # "dumps" converts the variable to a string, "dump" directly writes it to a file
    str_var = json.dumps(var, cls=JSONObjectEncoder)
    # Equivalently, "loads" converts the object back from a string. "load" from a file
    var_2 = json.loads(str_var, cls=JSONObjectDecoder)
    assert var == var_2

Deriving from JSONObject
------------------------

In order to serialize arbitrary, self-written classes, they must derive from ``JSONObject`` and implement the two
methods ``from_dict`` and ``to_dict``:

.. code:: python

    class MyClass(JSONObject):

        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self.c = c

        @classmethod
        def from_dict(cls, dict_):
            return cls(dict_['a'], dict_['b'], dict_['c'])

        def to_dict(self):
            return {'a': self.a, 'b': self.b, 'c': self.c}

        def __eq__(self, other):
            return self.a == other.a and self.b == other.b and self.c == other.c

General notes
-------------

-  ``jsonconversion`` stores the class path in the JSON string when serializing a JSONObject. When decoding the object
   back, it automatically imports the correct module. You only have to ensure that the module is within your
   ``PYTHONPATH``.

-  The ``to_dict`` and ``from_dict`` methods only need to specify the elements of a class, needed to recreate the
   object. Derived attributes of a class (like ``age`` from ``year_born``) do not need to be serialized.

-  If you compare the original object with the object obtained from serialization and deserialization using ``is``, they
   will differ, as these are objects at different locations in memory. Also a comparison of JSONObject with ``==`` will
   fail, if you do not tell Python how to compare two objects. This is why ``MyClass`` overrides the ``__eq__`` method.
