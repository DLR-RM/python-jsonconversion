from testing_utils import convert_with_assertion


class Custom(object):
    pass


class Custom2:
    def __init__(self):
        pass


def test_types():
    for _type in [int, float, str, type, complex, list, dict, set, tuple, type(None)]:
        convert_with_assertion(_type)


def test_nested_type():
    convert_with_assertion([int, type(None)])
    convert_with_assertion([{'a': float, 'b': (complex, set([set, dict]))}])


def test_class_type():

    convert_with_assertion(Custom)
    convert_with_assertion(Custom2)
