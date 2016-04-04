[![BuildBot Status](http://rmc-chimaere:8010/badge.png?builder=common/python-jsonconversion&branch=master)](http://rmc-chimaere:8010/builders/common%2Fpython-jsonconversion/)

# JSON Conversion

This python module helps converting arbitrary Python objects into JSON strings and back. For this purpose,
three classes are provided:

## JSONObject

Your own classes should inherit from this class. Hereby, they must implement the methods `from_dict` and
`to_dict`.

## JSONObjectEncoder

Encodes Python objects into JSON strings. Supported objects are:

* Python builtins: `int`, `float`, `str`, `list`, `set`, `dict`, `tuple`
* types (`isinstance(object, type)`)
* All classes deriving from `JSONObject`

## JSONObjectDecoder

Decodes JSON strings converted using the `JSONObjectEncoder` back to Python objects.


# Usage

Using JSON conversion is easy. You can find code examples in the `test` folder.

## Encoding and Decoding

In order to encode Python objects with JSON conversion and to later decode them, you have to import the
Python module `json`. The module provides the methods `dump`/`dumps` for encoding and `load`/`loads` for
decoding:

```python
import json

from jsonconversion.decoder import JSONObjectDecoder
from jsonconversion.encoder import JSONObjectEncoder

var = (1, 2, 3)  # variable to be serialized

# "dumps" converts the variable to a string, "dump" directly writes it to a file
str_var = json.dumps(var, cls=JSONObjectEncoder)
# Equivalently, "loads" converts the object back from a string. "load" from a file
var_2 = json.loads(str_var, cls=JSONObjectDecoder)
assert var == var_2
```

## Deriving from JSONObject

In order to serialize arbitrary, self-written classes, they must derive from `JSONObject` and implement the
two methods `from_dict` and `to_dict`:

```python
class MyClass(JSONObject):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def from_dict(cls, _dict):
        return cls(_dict['a'], _dict['b'], _dict['c'])

    def to_dict(self):
        return {'a': self.a, 'b': self.b, 'c': self.c}

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c
```

## General notes

JSON conversion stores the class path in the JSON string on serialization of JSONObjects. When decoding the
object back, it autimatically imports the correct module.

The `to_dict` and `from_dict` methods only need to specify the elements of the classes, needed to reacreate the
object. Parameters of a class, that are derived from other (like `age` from `year_born`) do not need to be
serialized.

If you compare the original object with the object obtained from serialization and deserialization using `is`,
they will differ, as these are objects at different locations in memory. Also a comparison of JSONObject with
`==` will fail, if you do not tell Python how to compare two objects. This is why `MyClass` overrides th
`__eq__` method.

