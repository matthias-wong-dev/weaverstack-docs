# Semantic-model extension API

Use `Annotation` to transform native TMDL during Build. `TmdlDefinition` also exposes editable native parts without a deployment. These imports are the supported extension surface; compiler, editor, contribution and registry internals are not extension APIs.

```python
from weaver.semantic_models.annotation import Annotation
from weaver.semantic_models.objects import TmdlDefinition
```

## Define an annotation

Put exactly one self-contained subclass in `PowerBI/annotations/Parcel__HideKeys.py`. The filename stem and class name must match. `__` separates namespace segments, giving the TMDL name `Parcel.HideKeys`. Each segment starts and ends with an alphanumeric character and contains alphanumerics or underscores. Weaver's namespace is reserved; case-only annotation-name collisions are rejected.

```python
from weaver.semantic_models.annotation import Annotation

class Parcel__HideKeys(Annotation):
    scopes = frozenset({"table"})

    def apply(self, target):
        if not self.boolean():
            return
        for column in target.columns:
            if column.name.endswith("Key"):
                column.isHidden = True
```

This is a transformation fragment, used on a table already declared in the model:

```tmdl
ref table Deliveries
    annotation 'Parcel.HideKeys' = true
```

`apply(target)` mutates the live object and returns nothing. Non-empty `scopes` names native object kinds, case-insensitively, not a string. Accepted scope kinds at this revision are `annotation`, `column`, `dataAccessOptions`, `database`, `expression`, `formatStringDefinition`, `hierarchy`, `level`, `measure`, `member`, `model`, `partition`, `relationship`, `role`, `source`, `table`, `tablePermission`. Invalid scopes, missing `apply`, mismatched filenames and more than one subclass in a file fail discovery. Project annotation files are trusted executable code loaded during project parsing, including Check. They are not sandboxed; use only code and installed packages you trust. Handler execution occurs in Build compilation, not in Power BI Desktop or every model refresh.

`value` returns trimmed declaration text with surrounding double quotes removed. `lines()` returns unquoted non-blank lines. `boolean()` accepts exactly lowercase `true` or `false`. Call `error(message)` for a located configuration error; unexpected handler exceptions also identify the declaration, class and file.

## Phases

`phase` defaults to `post_schema`; the other accepted value is `schema`. Schema handlers run before managed-source column/partition completion. Post-schema handlers see the resulting columns and run afterward. Use `schema` when adding a source declaration or structure needed for generation. Introducing a new managed source during `post_schema` is refused. Composition merges raw definitions before handlers run; inherited handlers run once on the final model. `Weaver.Source` and `Weaver.MeasureTable` are schema-phase built-ins. `Weaver.BaseSemanticModels` is a composition directive, not an executed handler.

## Edit native parts

`TmdlDefinition(parts)` takes a mapping of native relative paths to UTF-8 bytes. `.model` returns the root live object; `.parts` returns a new mapping of the resulting bytes. Unedited spans remain unchanged.

```python
parts = {"definition/model.tmdl": b"model Model\n"}
definition = TmdlDefinition(parts)
definition.model.tables.add("Metrics")
measure = definition.model.tables["Metrics"].measures.add("Deliveries", "1")
measure.formatString = "0"
resulting_parts = definition.parts
```

Objects supplied to annotations and reached through `.model` have these interfaces. The generated object/collection entries describe returned live views, not supported direct constructors:

- `name` is read-only; `parent` reaches the containing object and is `None` at the model root. Renaming through property assignment is unsupported.
- `obj.dataType` and `obj["dataType"]` read the same native property; missing properties return `None`. Native Boolean flags read as booleans; other scalar values generally remain text. `isHidden`, `formatString`, `description` and `expression` are native properties, not separately enumerated Weaver fields.
- Assignment edits that property in place. Assignment of `None`, `del obj[key]` and attribute deletion remove it. Block properties expose live objects; edit their members instead of replacing the block with a scalar.
- `.tables`, `.columns`, `.measures`, `.relationships`, `.partitions` and other native plural collections support definition-order iteration, length, case-insensitive membership/lookup and deletion by name. Missing lookup raises `KeyError`.
- `objects(kind)` addresses a collection of any native child kind, including kinds not interpreted by Weaver.
- `collection.add(name, expression=None, description=None, **properties)` creates and returns a live child; duplicate names fail. `expression` supplies the header assignment. Properties use native names and values.
- `set_expression(key, expression)` writes an expression-valued property using `=`, including multiline expressions.
- `remove()` deletes the object and its native references. The model root cannot be removed. Removing an object does not rewrite unrelated DAX references or supply security policy.

See [Annotations](../power-bi/annotations.md) and [TMDL merging](../power-bi/tmdl.md) for declarative alternatives and deployment checks.

<!-- BEGIN GENERATED SEMANTIC PYTHON -->

## Supported extension signatures

### `weaver.semantic_models.annotation.Annotation`

```python
Annotation.apply(self, target: TmdlObject) -> None
Annotation.boolean(self) -> bool
Annotation.error(self, message: str) -> NoReturn
Annotation.lines(self) -> list[str]
Annotation.phase = 'post_schema'
Annotation.scopes = frozenset()
Annotation.value  # property
```

### `weaver.semantic_models.objects.TmdlDefinition`

```python
TmdlDefinition.__init__(self, parts)
TmdlDefinition.model  # property
TmdlDefinition.parts  # property
```

### `weaver.semantic_models.objects.TmdlObject`

```python
TmdlObject.__delitem__(self, key)
TmdlObject.__getitem__(self, key)
TmdlObject.__setitem__(self, key, value)
TmdlObject.name  # property
TmdlObject.objects(self, kind)
TmdlObject.parent  # property
TmdlObject.remove(self)
TmdlObject.set_expression(self, key, expression)
```

### `weaver.semantic_models.objects.TmdlCollection`

```python
TmdlCollection.__contains__(self, name)
TmdlCollection.__delitem__(self, name)
TmdlCollection.__getitem__(self, name)
TmdlCollection.__iter__(self)
TmdlCollection.__len__(self)
TmdlCollection.add(self, name, expression=None, *, description=None, **properties)
```

<!-- END GENERATED SEMANTIC PYTHON -->
