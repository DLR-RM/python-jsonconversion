from jsonconversion.jsonobject import JSONObject
from testing_utils import convert_with_assertion


class JO(JSONObject):

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

    def __str__(self):
        return "{0}: a = {1}, b = {2}, c = {3}".format(self.__class__.__name__, self.a, self.b, self.c)


def test_simple_object():
    j1 = JO(1, 2, 3)
    j2 = JO(1.1, 2.2, 3.3)
    j3 = JO('a', "bcd", None)

    convert_with_assertion(j1)
    convert_with_assertion(j2)
    convert_with_assertion(j3)


def test_simple_object():
    j1 = JO({0: 'a', 1: 'b', 2: 'c'}, dict(enumerate(list("abc"))), (1, 2, 3))
    j2 = JO([1, 2, {3: 'a'}, (4, 5, set([6, 7]))], {0: [1, 2], 1: (3, 4), 'abc': [{'x': 1, 'y': 2}]}, j1)

    convert_with_assertion(j1)
    convert_with_assertion(j2)