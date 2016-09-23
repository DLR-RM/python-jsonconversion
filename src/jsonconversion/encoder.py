import numpy as np
from inspect import isclass
from types import ClassType

from json.encoder import JSONEncoder
from jsonconversion.jsonobject import JSONObject
from jsonconversion.conversion import get_qualified_name_for_class_object, get_qualified_name_for_class


class JSONObjectEncoder(JSONEncoder):
    """Custom JSON encoder class especially for state machines

    This JSON encoder class inherits from the basic JSON encoder class. It can encode all classes deriving from
    JSONObject. In addition, tuples (encoded by :py:class:`JSONObjectEncoder`) are maintained and type objects (e.g.
    int, object, float) are handled. Finally, it is tried to convert dictionary keys to integers.
    """

    def __init__(self, nested_jsonobjects=True, **kwargs):
        self.nested_jsonobjects = nested_jsonobjects
        for key in ['use_decimal', 'namedtuple_as_object', 'tuple_as_array', 'bigint_as_string', 'item_sort_key',
                    'for_json', 'ignore_nan']:
            try:
                del kwargs[key]
            except KeyError:
                pass
        super(JSONObjectEncoder, self).__init__(**kwargs)

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
            if self.nested_jsonobjects:
                for key, value in dictionary.iteritems():
                    dictionary[key] = self.encode(value)
            # e.g. rafcon.statemachine.states.execution_state.ExecutionState
            dictionary['__jsonqualname__'] = get_qualified_name_for_class_object(obj)
            return dictionary

        elif isinstance(obj, (type, ClassType)):
            if isclass(obj):
                return {'__type__': get_qualified_name_for_class(obj)}
            return {'__type__': obj.__name__}

        elif isinstance(obj, np.ndarray):
            return {'__jsonqualname__': "numpy.ndarray", "items": obj.tolist()}

        else:
            return super(JSONObjectEncoder, self).default(obj)

    def encode(self, obj):
        """This method is called before any object conversion of the inherited class

        The method checks for (nested) tuples and Vividicts and converts them appropriately.

        :param obj: The object to be encoded
        :return: Encoded object
        :rtype: dict
        """
        # Recursive check for sequence types
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
