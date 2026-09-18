# How incremental Build selection works

You changed one Weaver document, but Build selected several objects and left the rest alone. The selection comes from three questions:

1. Does the selected declaration still match the installed certification?
2. Does the selected target still contain the certified physical object in the expected form?
3. Which selected descendants depend on work that must be reconciled?

Build answers those questions inside the logical items you selected. It does not turn a dependency into permission to change another item.

## Certification is the starting point

A successful Build records certification for the installed definitions and generated work in `_.Registry`. Certification connects a logical object, its installed form and a signature. A physical Table or View with the same name but no matching certification is not automatically Weaver-owned.

The signature is an equality token for installable meaning. Changes to authored code, queries, relevant metadata, dependencies or generated work can move it. File modification time and source-control history do not decide equality, and the hash algorithm or encoding is not a public interface.

Build also reads the selected targets' physical inventory. A matching signature cannot prove that the certified object still exists or still has the expected physical kind. Certification and inventory are therefore reconciled before Build decides what work to retain.

## How an object is classified

Within the selected items, the useful classifications are:

- **New** — the declaration has no object in the expected installed form. Build installs it without first dropping an earlier Weaver installation.
- **Unchanged** — certification matches the declaration and inventory confirms the expected physical form. Build leaves it alone.
- **Changed** — the installed certification no longer represents the declaration or generated work, or physical reconciliation disproves the certified form. Build reconciles it to the selected declaration.
- **Impacted** — the object's own declaration is unchanged, but it is an existing selected descendant of changed or stale work and must be rebuilt against that upstream generation.

An uncertified physical name is not promoted to an unchanged Weaver object. A certified Table that is missing, or is now a View, is not unchanged either. Build withdraws the disproved claim and reconciles the selected desired state.

A settled second Build can therefore select no work at all: no physical changes, catalogue publication or unrelated recertification are needed.

## Why descendants appear

Consider this managed dependency chain:

```text
Parcel.Event → Parcel.CurrentStatus → Parcel.DispatchSummary
```

If `Parcel.Event` changes, it is a change root. Existing descendants in the same Build boundary can be impacted because their installed definitions were established against the earlier upstream generation. They may be rebuilt even when their own source files and signatures did not change.

Newness is narrower. Installing a new producer does not, by itself, classify every existing descendant as impacted. Build uses the managed relationships and installed state it has, rather than treating any new file as a reason to rebuild the whole estate.

The dependency order also explains why generated work can appear beside the document you edited. A Table declaration can own a physical Table, installed Load work and catalogue declarations; Build selects the parts whose installed meaning must change, not merely the source filename.

## The item boundary stops propagation

Suppose a producer is in `Lakehouse/Tracking` and a consumer is in `Warehouse/Dispatch`:

```text
Lakehouse/Tracking/Parcel.Event
              ↓ logical Shortcut
Warehouse/Dispatch/Parcel.CurrentStatus
```

Building only `Lakehouse/Tracking` can reconcile the producer, but it does not modify `Warehouse/Dispatch`. The consumer remains on its installed generation until its item is included in a later Build.

```bash
weaver build \
  --item Lakehouse/Tracking \
  --item Warehouse/Dispatch
```

When both items are selected, impact can cross the logical Shortcut and reach the consumer. This is why two Builds against the same source can select different object sets: the requested item set is the write boundary.

## Logical Shortcuts can reveal deferred staleness

A consumer behind a logical Shortcut can become stale when its producer was installed by an earlier Build after the consumer. On the next Build that selects the consumer item, Weaver refreshes the Shortcut path and affected consumers even when their authored signatures still match.

After those consumers are rebuilt against the newer producer, another identical Build settles to unchanged. The recorded installation generations make this possible; applications should not reproduce Weaver's freshness comparison or depend on its internal planning sequence.

## Mirrored objects become local only when selected work needs them

In a mirrored development estate, an unchanged borrowed object keeps its borrowed physical form. If Build selects that object as changed or impacted, successful installation replaces the borrowed form with the authored local form and removes its `_.Mirror` state. Unrelated borrowed objects remain borrowed.

This transition follows the same item boundary. Building a producer does not materialise consumers in an unselected item.

## Rebuild starts a new current state

Rebuilding a loadable Table or Folder resets its bookmark and current Load state for the new installed generation. Rebuilding a Test or Assumption resets its current Test state. An impacted descendant that is rebuilt is recertified and receives the same applicable reset even though its own source was unchanged.

Objects Build leaves unchanged keep their current state. `_.Log` and `_.LoadStatistic` are operational history and are not erased by an ordinary rebuild. A protected existing data object declared with `Prohibit rebuild` is retained instead of being dropped and rebuilt; that protection does not turn a genuinely new declaration into an existing object.

Use [Build behaviour](../reference/operation-behaviour/build.md) for exact selection, removal, certification and failure rules. [Dependencies](../core-concepts/dependencies.md) explains the managed graph, and [Mirrors](../core-concepts/mirrors.md) explains borrowed and local state.
