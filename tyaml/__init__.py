import logging
from typing import (
    Type as __Type,
    TypeVar as __TypeVar
)

import yaml

from .dumper import SpecialDumper as __SpecialDumper
from .loader import (
    TypeOrGeneric as __TypeOrGeneric,
    special_loader as __special_loader
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARNING)


def dump(data, stream=None, **kwargs):
    """Dump data with yaml.dump with tyaml.SpecialDumper as dumper"""
    _k_dumper = kwargs.pop("Dumper", None)
    if _k_dumper is not None:
        LOGGER.warning("'Dumper' argument will be ignored")  # pragma: nocover
    return yaml.dump(data, stream, Dumper=__SpecialDumper, **kwargs)


T = __TypeVar("T")


def load(stream, as_type: __Type[T]) -> T:
    """Load yaml"""
    return yaml.load(stream, Loader=__special_loader(as_type))
