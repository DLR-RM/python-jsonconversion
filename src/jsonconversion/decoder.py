try:
    import simplejson as json
    from simplejson.decoder import JSONDecoder
except ImportError:
    import json
    from json.decoder import JSONDecoder
from jsonconversion.conversion import string2type


class JSONObjectDecoder(JSONDecoder):
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
        super(JSONObjectDecoder, self).__init__(encoding=encoding, object_hook=self._dict_to_qualified_object, **kwargs)

    def _dict_to_qualified_object(self, dictionary):
        # Handle classes deriving from JSONObject and tuples
        if '__jsonqualname__' in dictionary:
            # e.g. rafcon.statemachine.states.execution_state.ExecutionState
            qualified_name = dictionary.pop('__jsonqualname__')
            if qualified_name in self.substitute_modules:
                qualified_name = self.substitute_modules[qualified_name]
            parts = qualified_name.split('.')
            module_name = ".".join(parts[:-1])
            # First ensure, that the module is imported
            cls = __import__(module_name)
            # Find nested class
            for comp in parts[1:]:
                cls = getattr(cls, comp)

            # Maintain tuples instead of converting them to a list
            if cls is tuple:
                return tuple(dictionary['items'])
            # Maintain sets instead of converting them to a list
            if cls is set:
                return set(dictionary['items'])

            # Recursively decode JSONObject
            for key, value in dictionary.iteritems():
                # Actually, dictionary[key] = self.decode(dictionary[key]) would be sufficient here
                # The instance check and the try..except block is needed for backwards compatibility
                if isinstance(value, basestring):
                    try:
                        converted_value = json.loads(dictionary[key], cls=self.__class__,
                                                     substitute_modules=self.substitute_modules)
                        dictionary[key] = converted_value
                    except ValueError:
                        pass

            # from_dict must be implemented by classes deriving from JSONObject
            return cls.from_dict(dictionary)

        # Handle type objects
        elif '__type__' in dictionary:
            return string2type(dictionary['__type__'])

        # Try to convert dictionary keys to integers
        elif isinstance(dictionary, dict):
            # Converts keys to integers, where possible
            temp_dictionary = {}
            for key, value in dictionary.iteritems():
                try:
                    key = int(key)
                except ValueError:
                    pass
                temp_dictionary[key] = value
            dictionary = temp_dictionary

        # If an additional converter function was passes to the constructor, call it now
        if self.additional_hook:
            return self.additional_hook(dictionary)

        return dictionary
