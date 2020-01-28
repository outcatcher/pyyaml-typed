import logging

import yaml

from .dumper import SpecialDumper as __SpecialDumper

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARNING)


def dump(data, stream=None, **kwargs):
    """Dump data with yaml.dump with tyaml.SpecialDumper as dumper"""
    _k_dumper = kwargs.pop("Dumper", None)
    if _k_dumper is not None:
        LOGGER.warning("'Dumper' argument will be ignored")  # pragma: nocover
    return yaml.dump(data, stream, Dumper=__SpecialDumper, **kwargs)
