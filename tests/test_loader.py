from dataclasses import dataclass
from typing import List, Set, Tuple

from pytest import fixture, mark

from tyaml import load


@dataclass
class DataClass:
    name: str
    data: dict


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


def test_typed_loader(obj):
    yml = (f"name: {obj.name}\n"
           "data:\n"
           f"  a: {obj.data['a']}\n"
           f"  b: {obj.data['b']}\n")
    loaded = load(yml, DataClass)
    assert loaded == obj
