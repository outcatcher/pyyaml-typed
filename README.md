# pyyaml-typed
![GitHub](https://img.shields.io/github/license/outcatcher/yaypl)

Library providing `dump` and `load` functions for pyyaml supporting `go-yaml`-like
description of yaml fields as class comments

Dataclasses and named tuples can be used without defining field names.
Field in comment for them will override default class field name

Example:

```python3
from tyaml import dump

@dataclass
class Something:
    my_fld_1: int
    # or use `yaml:` comment to rename
    field2: str  # yaml: my_fld_2
    
output = dump([Something(1, "that's"), Something(2, "nice")])
```

will create yaml:
```yaml
- my_fld_1: 1
  my_fld_2: "that's"
- my_fld_1: 2
  my_fld_2: "nice"
```
