import functools
import inspect
import re
from dataclasses import fields, is_dataclass

MAPPING_RE = re.compile(r"\s+([\w_\d]+?):?\s.*#\s*yaml:\s?(\w+)\n?")


def _get_container_fields(cls):
    # data classes
    if is_dataclass(cls):
        return {field.name: field.name for field in fields(cls)}
    # named tuples
    if hasattr(cls, "_fields"):
        return {field: field for field in getattr(cls, "_fields")}
    return {}


@functools.lru_cache(maxsize=64, typed=True)
def get_mappings(cls) -> dict:
    """Get `class field`: `yaml field` mapping for a class"""
    _fields = _get_container_fields(cls)

    try:
        src = inspect.getsource(cls)
    except OSError:  # e.g. this happens with collections.namedtuple
        return _fields
    except TypeError:  # in case of built-ins
        return {}

    src_lines = src.split("\n")
    for line in src_lines:
        match = MAPPING_RE.match(line)
        if match is None:
            continue
        _fields[match.group(1)] = match.group(2)
    return _fields
