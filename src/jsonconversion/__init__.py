# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution("jsonconversion").version
except DistributionNotFound:
    __version__ = "unknown"

python_3_6 = False
try:
    # Python >= 3.6
    from inspect import isclass, getargspec, getfullargspec
    python_3_6 = True
except ImportError:
    # Python < 3.6
    from inspect import isclass, getargspec

