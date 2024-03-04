# Copyright (C) 2016-2017 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>

import json
try:
    import numpy as np
except ImportError:
    np = False

from jsonconversion import get_all_args
from jsonconversion.conversion import string2type, get_class_from_qualified_name


class JSONObjectDecoder(json.decoder.JSONDecoder):
    """Custom JSON decoder class especially for state machines

    This JSON decoder class inherits from the basic JSON decoder class. It can decode all classes deriving from
    JSONObject. In addition, tuples (encoded by :py:class:`JSONObjectEncoder`) are maintained and type objects (e.g.
    int, object, float) are handled. Finally, it is tried to convert dictionary keys to integers.
    """

    additional_hook = None
    substitute_modules = {}

    def __init__(self, encoding=None, object_hook=None, **kwargs):
        if isinstance(kwargs.get('substitute_modules', None), dict):
            self.substitute_modules = kwargs['substitute_modules']
            del kwargs['substitute_modules']
        self.additional_hook = object_hook
        parental_constructor = super(JSONObjectDecoder, self).__init__
        parental_constructor_args = get_all_args(parental_constructor)
        if 'encoding' in parental_constructor_args:
            super(JSONObjectDecoder, self).__init__(encoding=encoding, object_hook=self._dict_to_qualified_object, **kwargs)
        else:
            super(JSONObjectDecoder, self).__init__(object_hook=self._dict_to_qualified_object, **kwargs)

    def _dict_to_qualified_object(self, dictionary):
        # Handle classes deriving from JSONObject and tuples
        if '__jsonqualname__' in dictionary:
            # e.g. rafcon.statemachine.states.execution_state.ExecutionState
            qualified_name = dictionary.pop('__jsonqualname__')
            qualified_name = self.substitute_modules.get(qualified_name, qualified_name)
            cls = get_class_from_qualified_name(qualified_name)

            # Maintain tuples instead of converting them to a list
            if cls is tuple:
                return tuple(dictionary['items'])
            # Maintain sets instead of converting them to a list
            if cls is set:
                return set(dictionary['items'])
            # Maintain NumPy ndarrays
            if np and cls is np.ndarray:
                return np.array(dictionary['items'])

            # Probably a JSONObject, as it must implement the from_dict method
            if hasattr(cls, "from_dict"):
                return cls.from_dict(dictionary)

            # If an additional converter function was passed to the constructor, it will hopefully take care of this
            # special __jsonqualname__
            if self.additional_hook:
                return self.additional_hook(dictionary)

            # That is all we can do now
            return dictionary

        # Handle type objects
        elif '__type__' in dictionary:
            type_string = dictionary['__type__']
            type_string = self.substitute_modules.get(type_string, type_string)
            return string2type(type_string)

        # Try to convert dictionary keys to integers
        elif isinstance(dictionary, dict):
            # Converts keys to integers, where possible
            temp_dictionary = {}
            for key, value in dictionary.items():
                try:
                    key = int(key)
                except ValueError:
                    pass
                temp_dictionary[key] = value
            dictionary = temp_dictionary

        # If an additional converter function was passed to the constructor, call it now
        if self.additional_hook:
            return self.additional_hook(dictionary)

        return dictionary
