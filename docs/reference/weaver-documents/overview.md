# Weaver documents

This section specifies how to author files that Weaver discovers as declarations. It covers paths, filenames, metadata, authored bodies, defaults and operation participation. The [Python API reference](../python/index.md) instead specifies public classes, constructors and runtime methods; a Python-authored document must satisfy both surfaces without duplicating their full specifications here.

## Document model

A Weaver document has four parts:

1. **Path** — selects the owning logical item and, for most kinds, the declaration family.
2. **Kind** — selected by the single ID key in object metadata, by the shortcut filename, by `schemas/`, or by `programmables/`.
3. **Metadata** — YAML in a Python module docstring or opening SQL `/* ... */` comment; shortcut, schema and programmable forms have their own schemas.
4. **Body** — Python class, SQL program, shortcut declarations, schema YAML or one Warehouse procedure statement.

Check and Build read the complete project statically. They parse Python but do not import or execute it. Build installs selected definitions; Load and Test later use the installed definitions rather than reopening project source.

The first two path components are exactly `Lakehouse/<Item>` or `Warehouse/<Item>`. Lakehouse data documents live directly in `Tables/` or `Files/`; Warehouse Tables and Views live at the item root. Tests, Assumptions, schema metadata and Warehouse programmables live directly in their named directories, with no nested declaration directories.

A Lakehouse `lib/` tree and each item shortcut file are supporting source, not independently selectable documents. Other files become declarations only in a supported location and form.

## Supported forms

| Kind | Lakehouse | Warehouse |
| --- | --- | --- |
| [Table](table.md) | Python or Spark SQL in `Tables/` | T-SQL at the item root |
| [Folder](folder.md) | Python in `Files/` | Not supported |
| [View](view.md) | Spark SQL in `Tables/` | T-SQL at the item root |
| [Test](test.md) | Python or Spark SQL in `tests/` | T-SQL in `tests/` |
| [Assumption](assumption.md) | Python or Spark SQL in `assumptions/` | T-SQL in `assumptions/` |
| [Shortcut](shortcut.md) | `shortcuts.py` | `shortcuts.yml` |
| [Schema metadata](schema-metadata.md) | YAML in `schemas/` | YAML in `schemas/` |
| [Warehouse programmable](warehouse-programmable.md) | Not supported | T-SQL in `programmables/` |

Python object and validation filenames are `Schema__Object.py`; SQL filenames are `Schema.Object.sql`. The metadata ID is `Schema.Object`. Filename, ID, kind-specific directory and directly declared Weaver class must agree exactly, including case. Duplicate identities and case-only collisions are errors.

The owning item selects the SQL dialect: Lakehouse `.sql` is Spark SQL; Warehouse `.sql` is T-SQL. A suffix does not select another dialect.

## Metadata and bodies

Object and validation metadata is a YAML mapping in the first module docstring or opening SQL block comment. It must contain exactly one kind-specific ID key. `Description` is required for every object and validation; data objects also require `Lineage`. See [Common metadata](common-metadata.md) for shared value syntax and each kind page for the complete accepted key set.

A Python file declares exactly one class that directly inherits its metadata kind. Helper classes may coexist. The class name equals the filename stem and implements the methods named on the kind page.

A SQL file starts with metadata and leaves the executable SQL as its body. Weaver validates the supported program shape statically; target-engine syntax and execution errors that require Fabric remain Build, Load or Test failures.

## Dependencies

When `Dependencies` is absent, Weaver infers document dependencies from authored Python imports or SQL relation references. A present `Dependencies` key replaces inference; `Dependencies: []` explicitly declares no dependencies. Entries are item-relative `Schema.Object` names and must resolve to objects or shortcut destinations in the same item. Tests and Assumptions may depend on data objects but cannot themselves be dependency targets.

Spark SQL **Tables and Views still require an explicit `Dependencies` key**, including `Dependencies: []`. Spark SQL Tests and Assumptions are validation documents and may omit it; Weaver then infers their SQL references.

Logical Shortcuts add cross-item edges. Physical references and physical Shortcuts have no project producer to order. Descriptive `$...` metadata references and foreign-key metadata do not create execution dependencies. Document and item dependency graphs must be acyclic; explicit replacement does not permit an item cycle.

## Page map

- [Common metadata](common-metadata.md) — shared text, references, revision notes and dependency syntax.
- [Table](table.md) — Python, Spark SQL and Warehouse Table declarations.
- [Folder](folder.md) — Lakehouse file-set declarations.
- [View](view.md) — Spark SQL and Warehouse Views.
- [Test](test.md) — expected-versus-actual validations.
- [Assumption](assumption.md) — violating-row validations.
- [Shortcut](shortcut.md) — exact Lakehouse Python and Warehouse YAML forms.
- [Schema metadata](schema-metadata.md) — optional schema descriptions and empty-schema declarations.
- [Warehouse programmable](warehouse-programmable.md) — authored stored procedures managed by Build.
