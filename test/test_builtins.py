# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

from testing_utils import convert_with_assertion


def test_numbers():
    i = 1
    f = 1.1

    convert_with_assertion(i)
    convert_with_assertion(f)


def test_strings():
    c = 'a'
    s = 'abc'
    i = '3'
    f = '3.14'

    convert_with_assertion(c)
    convert_with_assertion(s)
    convert_with_assertion(i)
    convert_with_assertion(f)


def test_lists():
    l1 = [1, 2, 3]
    l2 = list("abc")

    convert_with_assertion(l1)
    convert_with_assertion(l2)


def test_sets():
    s1 = (1, 2, 3)
    s2 = set("abc")

    convert_with_assertion(s1)
    convert_with_assertion(s2)


def test_dicts():
    d1 = {0: 'a', 1: 'b', 2: 'c'}
    d2 = dict(enumerate(list("abc")))

    convert_with_assertion(d1)
    convert_with_assertion(d2)


def test_nested():
    n1 = [1, 2, {3: 'a'}, (4, 5, set([6, 7]))]
    n2 = {0: [1, 2], 1: (3, 4), 'abc': [{'x': 1, 'y': 2}]}

    convert_with_assertion(n1)
    convert_with_assertion(n2)
