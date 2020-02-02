from copy import deepcopy
from dataclasses import is_dataclass
from typing import Any, Type, Union, _GenericAlias, _SpecialForm

from yaml import CollectionNode, FullLoader, MappingNode, SequenceNode

from tyaml.types import get_mappings


def _is_generic(cls):
    if isinstance(cls, _GenericAlias):
        return True

    if isinstance(cls, _SpecialForm):
        return cls not in {Any}

    return False


TypeOrGeneric = Union[type, _GenericAlias]


def _real_cls(cls: TypeOrGeneric) -> type:
    return cls.__origin__


def __kwarg_constructor(loader, node, typ, fld_mappings):
    fields = loader.construct_mapping(node, True)
    kwargs = {cls_field: fields[yml_field] for cls_field, yml_field in fld_mappings.items()}
    return typ(**kwargs)


def _type_tag(typ):
    return f"!!python/object:{typ.__module__}.{typ.__name__}"


def _add_single_cls_loader(typ, loader: Type[FullLoader], base_path: list):
    tag = _type_tag(typ)
    field_mappings = get_mappings(typ)
    if not field_mappings:
        return

    loader.add_constructor(tag, lambda l, n: __kwarg_constructor(l, n, typ, field_mappings.copy()))
    loader.add_path_resolver(tag, base_path[:], MappingNode)

    if hasattr(typ, "__annotations__"):
        # go deeper
        for field, f_typ in typ.__annotations__.items():
            if f_typ in [str, int, float]:
                continue
            el_path = deepcopy(base_path)
            el_path.append(field)
            _add_path_resolvers(f_typ, loader, el_path)


def _add_complex_resolver(typ, loader: Type[FullLoader], base_path: list, node_type: Type[CollectionNode]):
    item_types = [typ]
    base_path = base_path[:]
    base_path.append((node_type, False))
    if hasattr(typ, "__origin__"):
        if typ.__origin__ is Union:  # Union or Optional
            item_types.extend(typ.__args__)
        raise ValueError(f"Only top-level generics are allowed, but {typ} was given")
    if typ in item_types:
        _add_single_cls_loader(typ, loader, base_path)


def _add_path_resolvers(typ: TypeOrGeneric, loader: Type[FullLoader], base_path: list = None):
    if base_path is None:
        base_path = []
    if _is_generic(typ):
        args = typ.__args__
        if not args:
            return  # can't create new path resolver for generic without arguments
        typ = _real_cls(typ)  # convert typing generics to class
        if typ in [list, tuple, set, frozenset]:
            el_type = args[0]  # type: type
            _add_complex_resolver(el_type, loader, base_path, SequenceNode)
        if issubclass(typ, dict):
            el_type = args[1]
            _add_complex_resolver(el_type, loader, base_path, MappingNode)
    if is_dataclass(typ) or hasattr(typ, "_fields"):
        _add_single_cls_loader(typ, loader, base_path)


def special_loader(as_type: type) -> Type[FullLoader]:
    """Construct new loader class supporting current class structure"""

    class TypedLoader(FullLoader):  # pylint: disable=too-many-ancestors
        """Custom loader with typed resolver"""
        ...

    _add_path_resolvers(as_type, TypedLoader)  # we need to add resolver only to the root typed item

    return TypedLoader
