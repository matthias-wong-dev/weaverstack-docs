# Protecting data

**Ownership should match recoverability.** Before bringing data under Weaver management, ask whether the physical contents can be reconstructed. For truly irreplaceable data, keep the contents in an external physical item and expose them through a physical Shortcut. If Weaver should own the object but Build must preserve its existing contents, declare `Prohibit rebuild: true`.

## Choose the ownership boundary

Use the strongest boundary that fits the source:

| Situation | Pattern |
| --- | --- |
| Manually supplied Excel dump | External data + physical Shortcut |
| One-time historical source archive | External data + physical Shortcut |
| Another team owns the source | Physical Shortcut |
| Weaver Table accumulated through costly API calls | `Prohibit rebuild: true` |
| Weaver-managed Folder containing unrecoverable API responses | `Prohibit rebuild: true` |
| Ordinary reproducible derived Table | Normal Weaver management |

The distinction matters. A Shortcut keeps the data beyond Weaver's ownership boundary. `Prohibit rebuild` keeps the data inside that boundary and changes how Build reconciles an existing object.

## Keep irreplaceable sources outside Weaver ownership

Use a physical Shortcut when no repeatable process can reconstruct the source. Typical examples include:

- manually supplied Excel workbooks;
- one-off historical extracts;
- files supplied by another organisation;
- manually curated reference data;
- external archives; and
- any source without repeatable extraction.

Weaver manages the Shortcut destination in the local item: it may create, replace or remove that pointer as its declaration changes. Weaver does **not** manage the underlying physical source named by the Shortcut. This is the strongest ownership boundary because Build and Load do not treat the source contents as a Weaver-owned Table or Folder.

For example, a Lakehouse physical Folder Shortcut can expose an archive held in another workspace without making that archive part of the local estate's managed data. Follow [Connect data with Shortcuts](../basics/shortcuts.md) for the authoring workflow, and use the [Shortcut reference](../reference/weaver-documents/shortcut.md) for exact physical target forms and workspace rules.

## Retain an existing Weaver-owned object

Use `Prohibit rebuild: true` on a Table, Folder or View when Weaver should own the object, but Build must not satisfy a change by dropping and recreating the existing physical object. Add the field to the document's metadata header:

```yaml
Prohibit rebuild: true
```

This is appropriate for Weaver-owned data such as:

- costly API history accumulated over many Loads;
- API history that the provider no longer makes available;
- a Folder containing retained external responses;
- an object whose reconstruction is expensive;
- history built from an upstream that exposes only current state; or
- data whose reconstruction would breach rate limits or operational constraints.

When planning finds an existing protected object that would otherwise be rebuilt, it records that object as prohibited and omits its physical drop and build actions. The existing object is retained; Build does not fail merely because the changed object is protected. Other work in the plan can continue, including installation of new objects. Catalogue metadata, certification and separately generated load work can still reconcile when the change does not require replacing the protected physical object.

A source change that requires a different physical shape does not update that shape in place. The old object remains. Review the plan and resulting physical shape rather than assuming the edited declaration has been materialised. [Build behaviour](../reference/operation-behaviour/build.md) owns the exact planning, certification and installation semantics; [Common metadata](../reference/weaver-documents/common-metadata.md) owns the accepted field and default.

## Know what `Prohibit rebuild` does not do

**Warning:** `Prohibit rebuild` guards destructive replacement during Build only. It does not protect from Wipe, deliberate reload, or re-mirroring a destination containing it.

`Prohibit rebuild` is a Build replacement guard, not a general freeze:

- It does not freeze or prevent edits to the source document.
- It does not prevent first installation when no existing physical object is present.
- It does not prohibit normal Load reconciliation against an installed Table or Folder.
- It does not put the physical object outside Weaver ownership.
- It does not protect the external target behind a Shortcut; that target is already outside Weaver ownership.

A non-destructive metadata or load-logic change may therefore be installed while the physical object remains in place. A change requiring destructive recreation must not replace the existing object. If the desired physical shape must change, preserve or migrate the data deliberately before removing the protection or the existing object.

## Revisit the choice when recovery changes

Recoverability can change independently of code. A repeatable upstream may stop retaining history, a manual archive may gain a governed extraction process, or an API may impose new limits. Reassess both questions when that happens:

1. Should Weaver own the physical data at all?
2. If it should, can Build recreate the object without unacceptable loss or cost?

Use a physical Shortcut when the answer to the first question is no. Use `Prohibit rebuild` when the first answer is yes and the second is no. Use ordinary Weaver ownership when both answers are yes.
