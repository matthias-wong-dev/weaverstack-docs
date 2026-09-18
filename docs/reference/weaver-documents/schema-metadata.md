# Schema metadata

A schema metadata document optionally describes an item-owned schema or declares a schema that no other document uses. Object, validation and non-schema Shortcut identities imply their schemas, so a separate file is not required merely to create a normal object namespace.

## Location and identity

Schema metadata is supported in both item types at:

```text
<ItemType>/<Item>/schemas/<Schema>.yml
```

The file sits directly under `schemas/`. `<Schema>.yml` and `Schema ID` must match exactly, including case. `Schema ID` is one non-empty bare name: whitespace, forward slash, backslash, dot and colon are not accepted. Exact duplicates and case-only collisions with explicit or implied schemas are errors.

## Keys

| Key | Required | Value and default |
| --- | --- | --- |
| `Schema ID` | Yes | One bare schema name matching the filename. |
| `Description` | No | Non-empty string when present. Default: no description. |

No other keys are accepted. This file has no SQL or Python body, dependency declaration, class, method or return form. Its `Description` is literal schema prose; the object-metadata `$...` reference syntax is not interpreted here.

```yaml
Schema ID: Parcel
Description: Curated parcel tracking objects.
```

Path: `Lakehouse/Curated/schemas/Parcel.yml` or `Warehouse/Reporting/schemas/Parcel.yml`.

## Operations and managed state

- **Check** validates the YAML mapping, allowed keys, identity agreement and collisions.
- **Build** includes an explicit schema document in the owning item's source signature. Physical schema creation is planned when a selected object, programmable or non-schema Shortcut needs that schema; a standalone unused schema document is valid source but does not by itself select a physical schema for creation. A file describing a schema already implied by another declaration changes that one schema's metadata rather than creating a second identity.
- **Load** and **Test** do not execute schema metadata.

For schemas used by retained installed declarations, `_.SchemaDictionary` records item type, item name, schema name, optional description, a null description reference and the schema signature. Inferred schemas have no authored description and use a deterministic signature derived from the schema name. Ordinary schema declarations do not add a load or test status and have no managed row-audit or business columns of their own.
