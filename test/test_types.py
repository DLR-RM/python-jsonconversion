from testing_utils import convert_with_assertion

def test_types():
    for _type in [int, float, str, type, complex, list, dict, set, tuple, type(None)]:
        convert_with_assertion(_type)