# Build contract

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

See [`weaver build`](../reference/cli/build.md), [`weaver install`](../reference/cli/install.md), [Catalogue](catalogue.md), and [Dependencies](dependencies.md).