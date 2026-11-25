# Copyright (C) 2016-2026 DLR
#
# All rights reserved. This program and the accompanying materials are made
# available under the terms of the 2-Clause BSD License ("Simplified BSD
# License") which accompanies this distribution, and is available at
# https://opensource.org/licenses/BSD-2-Clause
#
# Contributors:
# Johannes Ernst <j.ernst@dlr.de>
#
# Code creation and review were performed with the assistance of generative AI.


import json

from jsonconversion.decoder import JSONObjectDecoder
from jsonconversion.encoder import JSONObjectEncoder
from jsonconversion.jsonobject import JSONObject


class Left:
    class Item(JSONObject):
        def to_dict(self):
            return {}

        @classmethod
        def from_dict(cls, data):
            return cls()


class Right:
    class Item(JSONObject):
        def to_dict(self):
            return {}

        @classmethod
        def from_dict(cls, data):
            return cls()


def encode(value):
    return json.dumps(value, cls=JSONObjectEncoder)


def test_nested_classes_have_distinct_identifiers():
    assert encode(Left.Item()) != encode(Right.Item())
    assert encode(Left.Item) != encode(Right.Item)


def test_nested_objects_roundtrip_with_allowlist():
    allowed = {__name__ + '.Left.Item': Left.Item, __name__ + '.Right.Item': Right.Item}
    for cls in (Left.Item, Right.Item):
        decoded = json.loads(encode(cls()), cls=JSONObjectDecoder, allowed_classes=allowed)
        assert type(decoded) is cls


def test_nested_types_roundtrip_untrusted_lookup():
    for cls in (Left.Item, Right.Item):
        decoded = json.loads(encode(cls), cls=JSONObjectDecoder, allow_untrusted_types=True)
        assert decoded is cls
