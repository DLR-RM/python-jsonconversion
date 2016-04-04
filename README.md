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


