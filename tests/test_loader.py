import random
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from pytest import fixture, mark

from tyaml import load


@dataclass
class DataClass:
    name: str
    data: dict


@dataclass
class DataClassWithDataClass:
    id: int
    items: List[DataClass]


@fixture
def obj():
    return DataClass("akodfk", {"a": 1, "b": 2, })


@mark.parametrize('seq_type', [List, Set, Tuple], ids=str)
def test_typed_list_loader(obj, seq_type):
    yml = (f"- name: {obj.name}\n"
           "  data:\n"
           f"    a: {obj.data['a']}\n"
           f"    b: {obj.data['b']}\n")
    loaded = load(yml, seq_type[DataClass])
    assert loaded == [obj]


def test_typed_dict_loader(obj):
    yml = (f"key:\n"
           f"  name: {obj.name}\n"
           "  data:\n"
           f"    a: {obj.data['a']}\n"
           f"    b: {obj.data['b']}\n")
    loaded = load(yml, Dict[str, DataClass])
    assert loaded == {"key": obj}


def test_typed_loader(obj):
    yml = (f"name: {obj.name}\n"
           "data:\n"
           f"  a: {obj.data['a']}\n"
           f"  b: {obj.data['b']}\n")
    loaded = load(yml, DataClass)
    assert loaded == obj


@fixture
def superobj(obj):
    return DataClassWithDataClass(random.randrange(0xffff), [
        obj,
        DataClass("1535", {"a": 1, "b": 3, }),
    ])


def test_nested_typed_loader(superobj):
    items = superobj.items
    yml = (f"id: {superobj.id}\n"
           f"items:\n")
    yml = yml + "\n".join(
        f"- name: '{o.name}'\n"
        f"  data:\n"
        f"    a: {o.data['a']}\n"
        f"    b: {o.data['b']}\n"
        for o in items
    )
    loaded = load(yml, DataClassWithDataClass)
    assert loaded == superobj
