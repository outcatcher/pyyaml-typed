# pyyaml-typed
![GitHub](https://img.shields.io/github/license/outcatcher/yaypl)

Library providing `SpecialDumper` and `SpecialLoader` for pyyaml providing `go-yaml`-like description of yaml fields as class comments

Example:

```python3
@dataclass
class Something:
    field1: int  # yaml: my_fld_1
    field2: str  # yaml: my_fld_2
    
output = yaml.dump([Something(1, "that's"), Something(2, "nice")], Dumper=SpecialDumper)
```

will create yaml:
```yaml
- my_fld_1: 1
  my_fld_2: "that's"
- my_fld_1: 2
  my_fld_2: "nice"
```
