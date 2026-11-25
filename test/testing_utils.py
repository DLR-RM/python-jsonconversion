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


from __future__ import print_function

import json
import numpy as np

from jsonconversion.decoder import JSONObjectDecoder
from jsonconversion.encoder import JSONObjectEncoder


# The decoder only resolves identifiers that are explicitly allowed (see README), so register the builtin classes and
# types handled by the encoder here. Tests using their own classes pass them via the allowed_* arguments.
ALLOWED_CLASSES = {"builtins.tuple": tuple, "builtins.set": set, "numpy.ndarray": np.ndarray}
ALLOWED_TYPES = {prefix + "." + t.__name__: t
                 for prefix in ("builtins", "__builtin__")
                 for t in (object, int, float, str, type, complex, list, dict, set, tuple)}


def convert(var, allowed_classes=None, allowed_types=None):

    str_var = json.dumps(var, cls=JSONObjectEncoder)
    print("\nConversion:", var, "=>", str_var, end=' ')
    var_2 = json.loads(str_var, cls=JSONObjectDecoder,
                       allowed_classes={**ALLOWED_CLASSES, **(allowed_classes or {})},
                       allowed_types={**ALLOWED_TYPES, **(allowed_types or {})})
    print("=>", var_2)
    return str_var, var_2


def convert_with_assertion(var, allowed_classes=None, allowed_types=None):
    str_var, var_2 = convert(var, allowed_classes, allowed_types)
    assert isinstance(str_var, str)
    if isinstance(var, (list, np.ndarray)):
        assert len(var) == len(var_2)
        assert all([e == e2 for e, e2 in zip(var, var_2)])
    else:
        assert var == var_2
    return str_var, var_2
