# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

class JSONObject(object):
    """Interface class

    Classes deriving from this class can be stored as JSON objects.
    """

    @classmethod
    def from_dict(cls, dictionary):
        """Abstract method

        This method must be implemented by the deriving classes. It must return an object of type cls, created from the
        parameters defined in dictionary. The type of cls is the type of the class the method is called on.

        :param dict dictionary: A Python dict with all parameters needed for creating an object of type cls
        :return: An instance of cls
        :rtype: cls
        """
        raise NotImplementedError()

    def to_dict(self):
        """Abstract method

        This method must be implemented by the deriving classes. It must return a Python dict with all parameters of
        self, which are needed to create a copy of self.

        :return: A Python dict with all needed parameters of self
        :rtype: dict
        """
        raise NotImplementedError()
