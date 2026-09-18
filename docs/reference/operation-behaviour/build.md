# Build behaviour


---

## Build contract

Build turns a project snapshot into installed Weaver definitions. It validates project source, compares selected logical items with their installed and physical state, creates a deployment bundle and, unless asked for a bundle only, installs that bundle.

## Source and item selection

`SOURCE` names a project directory. On the CLI it defaults to the current directory; inside a Fabric session the default is Notebook Resources and an `abfss` directory is also accepted. Weaver snapshots the complete source tree before parsing it, so edits made after discovery do not alter the bundle being prepared.

Build selects logical items with repeatable `--item` values:

```bash
weaver build ./parcel \
  --item Lakehouse/Landing \
  --item Warehouse/Operations=Warehouse/Operations_Dev
```

A value before `=` is a logical `Lakehouse/Name` or `Warehouse/Name`. The optional value after `=` is a physical target of the same kind. Without an override, the target comes from workspace configuration. Naming no item selects every configured target; if neither an item nor a configured target exists, Build fails.

The selected items are the write boundary. Build reads the whole project to resolve and validate declarations, but it does not install, remove or recertify project items outside the selection. Dependencies do not add an unselected item.

## Validation and planning

Before changing Fabric, Build parses the project and rejects invalid declarations, identities, dependencies, cycles, item selections and target bindings. It then reads the catalogue and the physical inventory of selected targets.

For each selected item, Build compares source, installed certification and physical inventory:

- a source document with no installed certification is new;
- a changed declaration, generated definition or disproved physical certification is changed;
- an installed descendant of changed work is impacted when it is inside the selected items;
- installed work removed from source is selected for removal;
- unchanged, physically present work is not rebuilt;
- a document that prohibits rebuilding is retained rather than dropped and rebuilt.

Changed and impacted work follows dependency order. Producers are installed before consumers; removals reverse the applicable dependency order. Cross-item impact is followed only where both items are selected.

## Deployment bundles

Every plan is written as a deployment bundle with a bundle identifier, selected targets, ordered work and the payloads required for installation. The bundle contains the prepared installation, not a copy of project source.

`--bundle-only` stops after creating that bundle. `--bundle-path` retains it in a new or empty directory and is valid only with `--bundle-only`. The resulting directory or `.weaver.zip` archive can be passed to `weaver install`; installation validates the bundle and its payloads before executing anything and does not reopen source or replan against it.

A bundle created from the same source and prepared state has the same identity. Installation uses the plan in the bundle rather than inferring additional work from the destination host.

## Installation and certification

Installation applies the bundle in its declared order. Catalogue certification follows the physical work it certifies. A physical object is installed only when the selected item binding and matching certification have been published successfully.

When a selected definition is rebuilt, its applicable current Load or Test state is reset to pending. Historical Load and Test records are retained. Unselected items and their current state remain outside the Build write boundary.

A successful Build reports `succeeded`. Its result identifies the source snapshot, selected logical items, bundle identifier, whether installation occurred and the retained bundle path when there is one.

## Failure and partial state

Source, request, state-read and bundle-validation failures stop before installation. During installation, a failed piece of work is reported as `failed`; work that cannot run after that failure is reported as `skipped`. The Build result is `failed` and carries the failed installed objects and source paths where available.

Build has no operation-wide rollback. Physical changes and catalogue updates that completed before a later failure remain in place. Certification is ordered after the physical work so a failed installation does not certify later work that never ran, but earlier successful changes are not undone. Rerunning Build replans from the state that remains.

For a retained bundle, installation writes an installation report beside its plan with one outcome for every planned piece of work. A normal Build returns the same installation report through its result.

## Defined behaviour

The Build contract specifies that Build:

1. snapshots and validates the project before planning installation;
2. treats selected logical items as its installation and catalogue boundary;
3. derives new, changed, impacted and removed work from source, certification and physical inventory;
4. orders selected changes by managed dependencies without adding unselected items;
5. creates a self-contained, validated deployment bundle before installation;
6. installs exactly the prepared bundle rather than reopening source or replanning;
7. publishes certification only for installed selected state;
8. stops later installation work after a failure and reports every planned outcome; and
9. does not roll back successful work from earlier in a failed installation.

See [`weaver build`](../cli/build.md), [`weaver install`](../cli/install.md), [Catalogue](../catalogue-schema.md), and [Dependencies](shared-selection-and-identity.md).

---

## Signatures and change-detection contract

Build compares the selected authored estate with the installed estate recorded in the catalogue and with current physical inventory. Signatures identify whether an installed definition still represents what Weaver would install; inventory establishes whether the certified physical object is actually present in the expected form.

A signature is an equality token, not a public content digest. Its algorithm, encoding and length are not part of this contract.

## What counts as a detectable change

For selected items, Weaver detects changes that alter the installable meaning of a document or generated work. This includes, where applicable:

- authored structure, query, Python or SQL body;
- installed metadata such as descriptions, lineage, keys, load behaviour and declared dependencies;
- a Shortcut's destination and source identity;
- generated Load or validation work derived from a document; and
- a change in Weaver's installation implementation for generated or managed physical work.

The comparison is against the installed certification, not file modification times or source-control history. Rewriting a file without changing its interpreted installable meaning need not select physical work. Conversely, generated work can change after a Weaver implementation change even when authored source is unchanged.

Build also detects certified objects that are absent from the selected target or present in a different physical form. Such an object is not treated as unchanged merely because its recorded signature matches.

## New, unchanged, changed and impacted

Within the selected items:

- **new** means the declared installable object is not present in the expected physical form;
- **unchanged** means its installed signature matches and physical reconciliation confirms the expected form;
- **changed** means the installed signature does not represent the selected declaration or generated work;
- **impacted** means an existing selected descendant must be reconciled because a changed or stale upstream object can affect what it installs.

Changed objects are impact roots. Impact follows the managed dependency graph through existing descendants selected for the same Build. A new object is installed, but newness alone does not classify all existing descendants as impacted. Cross-item impact reaches a consumer only when that consumer's item is selected.

A selected consumer can also be stale when an installed producer behind a logical Shortcut was rebuilt later. Weaver selects the stale Shortcut path and affected selected consumers even if their source signatures still match. Once the consumer has been rebuilt against the newer producer, the same state converges to unchanged.

An unchanged Build selects no physical or catalogue work. A changed Build does not republish unrelated unchanged catalogue tables merely because some other table changed.

## Physical reconciliation and pruning

Signatures do not establish physical existence or ownership. Build compares catalogue certification with target inventory before deciding what to retain, install or remove.

- A matching certified object in the expected form can remain unchanged.
- A certified object missing physically loses the claims that describe it and is handled as new work if still declared and selected.
- An object whose installed physical kind differs from the declared kind is reconciled to the selected declaration.
- A physical object with no Weaver certification does not become Weaver-owned merely because its name matches a declaration.
- Removing a declaration from a selected item removes the obsolete certification and permits pruning within that item's managed target scope.
- Objects and catalogue rows outside the selected items remain outside reconciliation.

`Prohibit rebuild` prevents replacement of an existing owned data object when a change would otherwise rebuild it. It does not suppress installation of a genuinely new object. A retained protected object keeps its applicable runtime state.

## Certification and runtime state

`_.Registry` records the installed signature only for work Build certifies. Physical presence without certification is not enough, and a declaration is not certified merely because it was discovered.

When Build replaces or refreshes installed work, the resulting object is certified again, including an unchanged descendant rebuilt because of impact. A borrowed mirrored object remains borrowed while unchanged; selected changed or impacted borrowed work becomes local when successfully installed.

Rebuilding a loadable object resets its current bookmark and Load state. Rebuilding a Test or Assumption resets its current Test state. Current state for unaffected objects and append-only operational history remain unchanged. Physical reconciliation alone does not erase runtime state before the selected lifecycle determines that the corresponding installed generation is being replaced or removed.

## Boundaries

This contract does not expose:

- signature hash algorithms, byte encodings or salts;
- bundle identity algorithms;
- internal planning node names or action ordering;
- a guarantee that every textual edit changes a signature;
- a guarantee that signatures are portable between different object kinds or execution engines; or
- permission to compare or manufacture catalogue signatures outside Weaver.

A signature should be compared only in the context of the same installed logical object and its Weaver-managed physical form.

## Defined behaviour

The Signatures and change-detection contract specifies that Weaver:

1. compares selected installable meaning with installed certification rather than timestamps or source-control state;
2. detects authored, generated and supported installation-implementation changes;
3. confirms physical presence and form separately from signature equality;
4. leaves a matching selected object unchanged and performs no work at a settled fixed point;
5. selects changed roots and existing selected descendants affected through managed dependencies;
6. does not widen impact into unselected items;
7. removes obsolete or disproved claims only within the selected managed boundary;
8. certifies rebuilt and refreshed work, including impacted descendants;
9. preserves unaffected current state and history while resetting state owned by rebuilt work; and
10. treats signature representation and internal installation sequencing as implementation details.
