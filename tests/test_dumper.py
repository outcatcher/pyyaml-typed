import random
from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Callable, NamedTuple

import pytest

from tyaml import dump


def cls_variant() -> Callable[[int, str], Any]:
    @dataclass
    class ExampleDataClass:
        int_field: int
        str_field: str

    yield ExampleDataClass

    @dataclass(frozen=True)
    class ExampleDataClassFrozen:
        int_field: int
        str_field: str

    yield ExampleDataClassFrozen

    yield namedtuple("ExampleNamedTuple", ["int_field", "str_field"])

    class ExampleTypedNamedTuple(NamedTuple):
        int_field: int
        str_field: str

    yield ExampleTypedNamedTuple

    class SimpleCommentedClass:
        int_field: int  # yaml: int_field
        str_field: str  # yaml: str_field
        other_field: str = 'asd'

        def __init__(self, i_fld, s_fld):
            self.int_field = i_fld
            self.str_field = s_fld

    yield SimpleCommentedClass

    @dataclass
    class ClassFieldRenamed:
        int_field: int
        not_str_field: str  # yaml: str_field

    yield ClassFieldRenamed


@pytest.mark.parametrize("cls", cls_variant())
def test_typed_fields(cls):
    int_field = random.randrange(100)
    str_field = "fhjldgfhjsdfgj"

    res = dump(cls(int_field, str_field))
    assert res == f"int_field: {int_field}\nstr_field: {str_field}\n"


def test_plain_class():
    class ThatClass:
        int_field: int
        str_field: str

        def __init__(self, i_fld, s_fld):
            self.int_field = i_fld
            self.str_field = s_fld

    res = dump(ThatClass(1, "2"))
    assert res == "!!python/object:test_dumper.ThatClass\nint_field: 1\nstr_field: '2'\n"
