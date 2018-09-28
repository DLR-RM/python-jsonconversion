# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

from __future__ import print_function

import json
import numpy as np

from jsonconversion.decoder import JSONObjectDecoder
from jsonconversion.encoder import JSONObjectEncoder


def convert(var):

    str_var = json.dumps(var, cls=JSONObjectEncoder)
    print("\nConversion:", var, "=>", str_var, end=' ')
    var_2 = json.loads(str_var, cls=JSONObjectDecoder)
    print("=>", var_2)
    return str_var, var_2


def convert_with_assertion(var):
    str_var, var_2 = convert(var)
    assert isinstance(str_var, str)
    if isinstance(var, (list, np.ndarray)):
        assert len(var) == len(var_2)
        assert all([e == e2 for e, e2 in zip(var, var_2)])
    else:
        assert var == var_2
    return str_var, var_2

