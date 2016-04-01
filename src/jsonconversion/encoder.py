from json.encoder import JSONEncoder
from jsonconversion.jsonobject import JSONObject


class JSONObjectEncoder(JSONEncoder):
    """Custom JSON encoder class especially for state machines

    This JSON encoder class inherits from the basic JSON encoder class. It can encode all classes deriving from
    JSONObject. In addition, tuples (encoded by :py:class:`JSONObjectEncoder`) are maintained and type objects (e.g.
    int, object, float) are handled. Finally, it is tried to convert dictionary keys to integers.
    """

    def default(self, obj):
        """This method is called after all base class encoding logic

        Here, additional conversions of objects to dictionaries can be defined. Both JSONObject and type objects are
        treated.

        :param obj: Object to be converted to a dictionary
        :return: Dictionary representing the given object
        :rtype: dict
        """
        if isinstance(obj, JSONObject):
            # to_dict must be implemented by classes deriving from JSONObject
            dictionary = obj.to_dict()
            for key, value in dictionary.iteritems():
                dictionary[key] = self.encode(value)
            # e.g. rafcon.statemachine.states.execution_state.ExecutionState
            dictionary['__jsonqualname__'] = obj.__module__ + '.' + obj.__class__.__name__
            return dictionary

        elif isinstance(obj, type):
            return {'__type__': obj.__name__}

        else:
            return super(JSONObjectEncoder, self).default(obj)

    def encode(self, obj):
        """This method is called before any object conversion of the inherited class

        The method checks for (nested) tuples and Vividicts and converts them appropriately.

        :param obj: The object to be encoded
        :return: Encoded object
        :rtype: dict
        """
        # Recursive check for tuples and Vividicts (within tuples, dicts and lists)
        def check_for_sequences(item):
            if isinstance(item, set):
                dictionary = {'__jsonqualname__': '__builtin__.set',
                              'items': [check_for_sequences(val) for val in item]}
                return dictionary

            if isinstance(item, tuple):
                dictionary = {'__jsonqualname__': '__builtin__.tuple',
                              'items': [check_for_sequences(val) for val in item]}
                return dictionary

            elif isinstance(item, dict):
                dictionary = {}
                for key, value in item.iteritems():
                    dictionary[key] = check_for_sequences(value)
                return dictionary

            elif isinstance(item, list):
                return [check_for_sequences(e) for e in item]

            return item

        return super(JSONObjectEncoder, self).encode(check_for_sequences(obj))