import numpy as np

from testing_utils import convert_with_assertion


def test_numbers():
    arr = np.array([1., 2., 3.])

    convert_with_assertion(arr)
