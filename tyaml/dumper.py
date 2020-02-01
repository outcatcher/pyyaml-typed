from yaml import Dumper

from tyaml.types import get_mappings


class SpecialDumper(Dumper):  # pylint: disable=too-many-ancestors
    """Dumper overriding standard `represent_object` method"""

    def represent_object(self, data):
        mappings = get_mappings(type(data))  # find yaml fields mappings
        if not mappings:
            return super().represent_object(data)
        result_dict = {}
        for attribute, field_name in mappings.items():
            result_dict[field_name] = getattr(data, attribute)
        return self.represent_dict(result_dict)


SpecialDumper.add_multi_representer(object, SpecialDumper.represent_object)
