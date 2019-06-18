import json

from jsonconversion.encoder import JSONObjectEncoder

def test_dict():
    dump = json.dumps({"b": 2.3, 'a': 1}, cls=JSONObjectEncoder, indent=4, sort_keys=True, separators=(',', ': '))
    target_dump = \
"""{
    "a": 1,
    "b": 2.3
}"""
    assert dump == target_dump
