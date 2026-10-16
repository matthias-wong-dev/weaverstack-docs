# Schemas, keys and protected data

The [event Table](first-project.md) declares its business columns and composite key. The [incremental variation](incremental.md) uses a parcel key to match updates and explicit deletes. These declarations tell Weaver how to maintain rows; ownership decides whether those rows may be reconstructed at all.

## Choose the business shape and row identity

Warehouse SQL Tables can declare `Schema` or let Build infer business names and physical types from the query result. The first example declares it so the four-column shape is explicit. A declared query must return every business column and no extra one; Views take their shape from their query. Neither authored SQL nor staging data supplies Weaver's managed audit, signature or identity columns.

`Primary key: Parcel ID, Event sequence` makes the first Table's identity an event. `Primary key: Parcel ID` makes the incremental Table's identity a parcel. The key's ordered columns are implicitly non-null; an incremental Table requires a key to match updates and delete claims. Declaring it does not promise a physical index or database-enforced constraint.

A matching key with changed comparison values becomes an update. By default, comparison uses every business column outside the primary key; narrow `Comparison columns` only when an excluded value should not trigger an update. Foreign keys describe logical relationships, but do not establish execution order or enforce referential integrity. Query references or explicit dependencies supply ordering.

[Schemas, keys and managed columns](../advanced/schemas-keys-and-managed-columns.md) explains inferred and declared shapes, nullability, unique and foreign keys, identity and engine-specific managed columns. [Table](../reference/weaver-documents/table.md) and [Common metadata](../reference/weaver-documents/common-metadata.md) own the accepted fields and combinations.

## Keep the source outside the managed target

The mutable-source example keeps `ParcelSource` outside `targets` and exposes its Table through a physical Shortcut. Weaver manages the local pointer, not the underlying external Table. That is the stronger boundary for manually supplied, one-off or irreplaceable data: the source is not a managed object that Build or Load can reconstruct.

Keep reproducible transformations inside the managed Warehouse. Keep data you cannot re-extract in a separate physical item, even if a derived Table reads it. [Protecting data](../advanced/protecting-data.md#choose-the-ownership-boundary) covers how recoverability changes that choice; [Shortcuts](../reference/weaver-documents/shortcut.md) defines the physical target forms.

## Retain an existing managed object during Build

When Weaver should own an object but Build must not replace its existing physical contents, add this field inside its metadata header:

```yaml
Prohibit rebuild: true
```

The first event feed is reproducible, so it does not need this flag. Accumulated API history that is no longer available upstream may need it. For an existing protected object requiring replacement, Build omits the physical drop and recreation; it does not fail solely because the object is protected. Other work can continue, and metadata or generated load logic may still reconcile without replacing the object. A changed declaration does not guarantee that a new physical shape was installed: inspect the Build preview and retained shape.

**Warning:** `Prohibit rebuild` guards replacement during Build only. It does not guard normal Load changes, destructive reload, Wipe or Mirror/reset, and does not move the object outside Weaver ownership. External ownership is the stronger boundary for irreplaceable sources.

[Protecting data](../advanced/protecting-data.md#know-what-prohibit-rebuild-does-not-do) explains the full limits, including protected materialisation in a Mirror. [Build behaviour](../reference/operation-behaviour/build.md) owns the exact planning and installation rules.

Once individual Tables are working, [Coordinate your estate](../estate/index.md) connects their dependencies, environment mappings and recorded state. [The development cycle](../estate/development-cycle.md) puts source edits and Build previews into ordinary work; [Recover failed work](../estate/recovery.md) covers choosing the smallest recovery action before any reset.
