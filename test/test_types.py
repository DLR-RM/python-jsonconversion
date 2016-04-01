from testing_utils import convert_with_assertion


def test_types():
    for _type in [int, float, str, type, complex, list, dict, set, tuple, type(None)]:
        convert_with_assertion(_type)


def test_nested_type():
    convert_with_assertion([int, type(None)])
    convert_with_assertion([{'a': float, 'b': (complex, set([set, dict]))}])
