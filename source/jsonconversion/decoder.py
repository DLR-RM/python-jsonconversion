# Copyright (C) 2016-2026 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Franz Steinmetz <franz.steinmetz@dlr.de>
# Johannes Ernst <j.ernst@dlr.de>

import json
try:
    import numpy as np
except ImportError:
    np = False

from jsonconversion import get_all_args
from jsonconversion.conversion import string2type

class JSONObjectDecoder(json.decoder.JSONDecoder):
    """Custom JSON decoder class especially for state machines

    This JSON decoder inherits from :py:class:json.decoder.JSONDecoder. It can decode
    classes deriving from :py:class:JSONObject. In addition, tuples (encoded by
    :py:class:JSONObjectEncoder) are preserved, type objects (e.g. int, object,
    and float) are handled, and dictionary keys are converted to integers where
    possible.

    For security, the decoder supports allowlists that restrict which classes and types
    can be resolved when decoding JSON data:
    -   allowed_classes specifies the classes that may be reconstructed from JSON
        metadata. It should contain trusted class objects, mapped to the qualified names
        used in the serialized data.

    -   allowed_types specifies the types that may be resolved from JSON metadata.
        It should contain trusted type objects, mapped to the identifiers used in the
        serialized data.

    -   allow_untrusted_types controls whether unrestricted type resolution is
        permitted for backward compatibility. It defaults to False. Set it to
        True only when decoding trusted JSON data and when compatibility with
        unrestricted type resolution is required.

    Applications that decode untrusted JSON should leave allow_untrusted_types
    disabled and configure allowed_classes and allowed_types for the classes
    and types they need. Only trusted classes should be allowlisted, since their
    deserialization methods (such as from_dict) may execute application code.
    Allowlisting limits which identifiers can be resolved, but does not guarantee that
    the registered classes or their deserialization methods are safe.
    """

    additional_hook = None
    substitute_modules = {}

    def __init__(
            self,
            encoding=None,
            object_hook=None,
            allowed_classes=None,
            allowed_types=None,
            allow_untrusted_types = False,
            **kwargs):
        # Registries with mapped classes and types must be provided by trusted application code
        self.allowed_classes = dict(allowed_classes or {})
        self.allowed_types = dict(allowed_types or {})
        self.allow_untrusted_types = allow_untrusted_types
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
        # Handle trusted classes with allowlist
        if '__jsonqualname__' in dictionary:
            # e.g. rafcon.statemachine.states.execution_state.ExecutionState
            qualified_name = dictionary.pop('__jsonqualname__')
            qualified_name = self.substitute_modules.get(qualified_name, qualified_name)
            try:
                cls = self.allowed_classes[qualified_name]
            except KeyError:
                raise ValueError(f"Unrecognized serialized class: {qualified_name}") from None

            # Maintain tuples instead of converting them to a list
            if cls is tuple:
                return tuple(dictionary['items'])
            # Maintain sets instead of converting them to a list
            if cls is set:
                return set(dictionary['items'])
            # Maintain NumPy ndarrays
            if np and cls is np.ndarray:
                return np.array(dictionary['items'])

            # Only explicitly approved classes (like JSONObject classes) reach this method call
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
            try:
                return self.allowed_types[type_string]
            except KeyError:
                return string2type(type_string, allow_untrusted=self.allow_untrusted_types)

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
