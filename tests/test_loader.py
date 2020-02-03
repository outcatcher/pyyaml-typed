import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import yaml
from pytest import fixture, mark, raises

from tyaml import load


@dataclass
class DataClass:
    name: str
    data: Dict[str, int]


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


@dataclass
class _NestedWithOpt:
    id: int
    sub: Optional[DataClass] = None


def test_nested_with_optional(obj):
    _id = random.randrange(0xffff)
    yml = (f"id: {_id}\n"
           f"sub:\n"
           f"  name: {obj.name}\n"
           f"  data:\n"
           f"    a: {obj.data['a']}\n"
           f"    b: {obj.data['b']}\n")
    loaded = load(yml, _NestedWithOpt)
    assert loaded == _NestedWithOpt(_id, obj)


def test_nested_with_optional_none():
    _id = random.randrange(0xffff)
    yml = f"id: {_id}\n"
    loaded = load(yml, _NestedWithOpt)
    assert loaded == _NestedWithOpt(_id)


@mark.parametrize("typ", [Any, List, Dict], ids=str)
def test_ignored_types(typ):
    _id = random.randrange(0xffff)
    yml = f"id: {_id}\n"
    loaded = load(yml, typ)
    assert loaded
    assert isinstance(loaded, dict)


@mark.parametrize("invalid_type", [
    Union[int, str, None],
    Union[int, str],
], ids=str)
def test_multi_union(invalid_type):
    with raises(TypeError):
        loaded = load("", invalid_type)
        print(loaded)


def test_optional_in_list():
    @dataclass
    class __Simple:
        a: int
        b: int

    expected = [[{"a": 1, "b": 2}]]
    yml = yaml.safe_dump(expected)
    loaded = load(yml, List[List[Optional[__Simple]]])
    assert loaded == [[__Simple(1, 2)]]
