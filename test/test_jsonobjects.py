# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

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
        return "{0}: a = {1} {4}, b = {2} {5}, c = {3} {6}".format(self.__class__.__name__, self.a, self.b, self.c,
                                                                   type(self.a), type(self.b), type(self.c))


def test_simple_objects():
    j1 = JO(1, 2, 3)
    j2 = JO(1.1, 2.2, 3.3)
    j3 = JO('a', "bcd", None)
    j4 = JO('1.1', "3", "0")
    j5 = JO(-2, "preempted", float)

    convert_with_assertion(j1)
    convert_with_assertion(j2)
    convert_with_assertion(j3)
    convert_with_assertion(j4)
    convert_with_assertion(j5)


def test_nested_objects():
    l1 = [JO(1, 2, 3), JO('1.1', "3", "0")]
    t1 = tuple(l1[:])
    d1 = {0: l1[:], 1: tuple(t1)}

    convert_with_assertion(l1)
    convert_with_assertion(t1)
    convert_with_assertion(d1)


def test_complex_objects():
    j1 = JO({0: 'a', 1: int, 2: -5}, dict(enumerate(list("abc"))), (1, 2, 3))
    j2 = JO([1, 2, {3: 'a'}, (4, 5, set([6, 7]))], {0: [1, 2], 1: (3, 4), 'abc': [{'x': 1, 'y': 2}]}, j1)
    j3 = JO({0: j1, 1: {0: j1}}, {0: list, 1: {0: float}}, {0: None, 1: {0: None}})
    j4 = JO({0: JO(1, 2, 3), 1: {0: JO(1, 2, 3)}},
            {0: JO(-2, "preempted", float), 1: {0: JO(-2, "preempted", float)}},
            JO(-2, "preempted", float))

    convert_with_assertion(j1)
    convert_with_assertion(j2)
    convert_with_assertion(j3)
    convert_with_assertion(j4)
