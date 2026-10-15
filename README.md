# The `jsonconversion` package

This python module helps converting arbitrary Python objects into JSON
strings and back. It extends the basic features of the `JSONEncoder` and
`JSONDecoder` classes provided by the native `json` package, making it possible to preserve object information when saving data and reconstructing it later.

The package is useful for applications that need to store Python objects in a JSON-based format, including objects representing application-specific data structures.

## Installation

Install the package using pip:

```bash
pip install jsonconversion
```

## The `JSONObject` class

Your serializable classes should inherit from this class. Hereby, they
must implement the methods `from_dict` and `to_dict`. The example
further down describes how to do so.

## The `JSONExtendedEncoder` class

This is a class used internally by `JSONObjectEncoder`. However, it can
also be used directly, if you do not need the features of
`JSONObjectEncoder` but want to implement your own encoders.

The class is especially helpful, if you want custom handling of builtins
(`int`, `dict`, \...) or classes deriving from builtins. This would not
be possible if directly inheriting from `JSONEncoder`. To do so,
override the `isinstance` method and return `False` for all types you
want to handle in the `default` method.

If you look at the source code of `JSONObjectEncoder`, you will see how
this can be used.

## The `JSONObjectEncoder` class

Encodes Python objects into JSON strings. Supported objects are:

-   Python builtins: `int`, `float`, `str`, `list`, `set`, `dict`,
    `tuple`
-   `type` objects: `isinstance(object, type)`
-   All classes deriving from `JSONObject`

Those objects can of course also be nested!

## The `JSONObjectDecoder` class

Decodes JSON strings converted using the `JSONObjectEncoder` back to
Python objects.

The class adds a custom keyword argument to the `load[s]` method:
`substitute_modules`. This parameter takes a `dict` in the form
`{"old.module.MyClass": "new.module.MyClass"}`. It can be used if you
have serialized `JSONObject`s who\'s module path has changed.

## Controlling deserialization

Deserialization can involve resolving serialized class and type identifiers back into Python objects. Because resolving arbitrary identifiers can import modules and invoke application code, the decoder provides three parameters to control this behavior:

- `allowed_classes`
- `allowed_types`
- `allow_untrusted_types`

These parameters should be configured by the application that uses `jsonconversion`.

### `allowed_classes`

`allowed_classes` defines the classes that may be resolved when reconstructing serialized objects identified by `__jsonqualname__`.

It should be a mapping from serialized class identifiers to trusted Python class objects. For example:

```python
allowed_classes = {
    "my_package.models.ExampleObject": ExampleObject,
}
```

Only classes that the application intentionally supports should be included. The registered class objects should be imported and supplied by trusted application code rather than dynamically selected based on the JSON input.

The application should provide all classes required to reconstruct its serialized objects, including any application-specific classes needed to load saved data.

### `allowed_types`

`allowed_types` defines the types that may be resolved from serialized type identifiers stored in the `__type__` field.

It should be a mapping from serialized type identifiers to trusted Python type objects. For example:

```python
allowed_types = {
    "int": int,
    "str": str,
    "float": float,
    "bool": bool,
    "builtins.int": int,
    "builtins.str": str,
}
```

The identifiers must match those emitted by the encoder or otherwise expected in the serialized data. Register only the types required by the application.

Applications may construct this mapping programmatically where appropriate, but should not automatically trust arbitrary type identifiers from a JSON document.

### `allow_untrusted_types`

`allow_untrusted_types` controls whether the decoder may resolve type identifiers that are not covered by the configured allowlist, using the package's unrestricted legacy resolution behavior.

By default, this option is `False`:

```python
allow_untrusted_types = False
```

With the default setting, applications should provide the required `allowed_classes` and `allowed_types` mappings. Unrecognized identifiers should not be resolved through unrestricted dynamic lookup.

Setting `allow_untrusted_types=True` enables compatibility with data that references types not explicitly registered. Depending on the identifier and the resolution path, this may cause additional modules to be imported or application-defined code to be executed.

**Security warning: Only set `allow_untrusted_types=True` when the JSON data comes from a trusted source and you accept the risks of dynamic type resolution. Never enable it when loading potentially malicious or untrusted JSON.**

The option is intended for compatibility with existing workflows where the set of user-defined types cannot be known in advance. It should not be considered a security mechanism or a sandbox.

# Usage

Using `jsonconversion` is easy. You can find further code examples in
the `test` folder.

## Encoding and Decoding

In order to encode Python objects with JSON conversion and to later
decode them, you have to import the Python module `json`. The module
provides the methods `dump`/`dumps` for encoding and `load`/`loads` for
decoding:

``` python
import json

from jsonconversion.decoder import JSONObjectDecoder
from jsonconversion.encoder import JSONObjectEncoder

var = (1, 2, 3)  # variable to be serialized

allowed_classes = {
    "my_package.models.ExampleObject": ExampleObject,
}

allowed_types = {"int": int, "tuple": tuple,}

# "dumps" converts the variable to a string, "dump" directly writes it to a file
str_var = json.dumps(var, cls=JSONObjectEncoder)

# Equivalently, "loads" converts the object back from a string. "load" from a file
var_2 = json.loads(
    str_var,
    cls=JSONObjectDecoder
    allowed_classes=allowed_classes,
    allowed_types=allowed_types,
    allow_untrusted_types=False,
)
assert var == var_2
```

## Deriving from JSONObject

In order to serialize arbitrary, self-written classes, they must derive
from `JSONObject` and implement the two methods `from_dict` and
`to_dict`:

``` python
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
```

## Compatibility

The `substitute_modules` decoder parameter can be used to map serialized identifiers that reference older module paths to their current names. This can help applications load data created before classes were moved or renamed.

Module substitutions should be configured by trusted application code. They do not replace the need to configure the allowed classes and types.

## General notes

-   `jsonconversion` stores the class path in the JSON string when
    serializing a JSONObject. When decoding the object back, it
    automatically imports the correct module. You only have to ensure
    that the module is within your `PYTHONPATH`.
-   The `to_dict` and `from_dict` methods only need to specify the
    elements of a class, needed to recreate the object. Derived
    attributes of a class (like `age` from `year_born`) do not need to
    be serialized.
-   If you compare the original object with the object obtained from
    serialization and deserialization using `is`, they will differ, as
    these are objects at different locations in memory. Also a
    comparison of JSONObject with `==` will fail, if you do not tell
    Python how to compare two objects. This is why `MyClass` overrides
    the `__eq__` method.

## License

See the repository's license file for licensing information.

