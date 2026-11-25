# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>
# Johannes Ernst <j.ernst@dlr.de>
#
# Code refinement and review were performed with the assistance of generative AI.


from testing_utils import convert_with_assertion as _convert_with_assertion


class Custom(object):
    pass


class Custom2:
    def __init__(self):
        pass


def convert_with_assertion(var):
    return _convert_with_assertion(var, allowed_types={__name__ + ".Custom": Custom, __name__ + ".Custom2": Custom2})


def test_types():
    for _type in [int, float, str, type, complex, list, dict, set, tuple, type(None)]:
        convert_with_assertion(_type)


def test_nested_type():
    convert_with_assertion([int, type(None)])
    convert_with_assertion([{'a': float, 'b': (complex, set([set, dict]))}])


def test_class_type():

    convert_with_assertion(Custom)
    convert_with_assertion(Custom2)
