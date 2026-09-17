# Resources and artefacts

You author **resources** through Weaver **documents**. Build turns those declarations into the physical objects and runnable **artefacts** needed to install and operate the resource.

```text
project document → declared resource → installed object and runnable artefact
```

These are different views of the same intent. Documents are the files you edit. Resources are the named parts of the logical estate. Artefacts are what Build installs so later operations can realise or run those resources.

[Projects and estates](projects-and-estates.md) explains where desired and installed state live. [Logical and physical items](logical-and-physical-items.md) explains how the owning item reaches a Fabric target.

## Resources are the public logical model

A resource is a named declaration owned by a logical item. Common resources include:

- Lakehouse Folders, Tables and Views;
- Warehouse Tables and Views;
- schemas and shortcuts;
- Tests and Assumptions;
- supported Warehouse programmables.

The owning item is part of the resource's identity. Lakehouse data resources also name their Fabric area:

```text
Lakehouse/Landing/Files/Parcel.Events
Lakehouse/Landing/Tables/Parcel.Event
Warehouse/Operations/Parcel.CurrentStatus
```

`Files/Parcel.Events` and `Tables/Parcel.Events` are distinct Lakehouse resources. A Warehouse resource uses `Schema.Object` without a `Files` or `Tables` area. The same `Schema.Object` may appear in different items because each item owns its own resources.

This logical identity is what dependencies, item selection, reports and catalogue state refer back to. The physical workspace and target name do not become part of it.

## Documents declare resources

A document is an authored file with a contract Weaver understands. Its location, filename and metadata establish the resource it declares.

For example, `Lakehouse/Landing/Tables/Parcel__Event.py` declares `Table ID: Parcel.Event`. The path places the resource in `Lakehouse/Landing/Tables`; the filename and `Table ID` identify the same `Parcel.Event` resource. Weaver checks that these agree. The corresponding public identity is:

```text
Lakehouse/Landing/Tables/Parcel.Event
```

Warehouse SQL follows the same ownership rule without a Lakehouse area. The document `Warehouse/Operations/Parcel.Status.sql` declares `Table ID: Parcel.Status`, producing the public identity `Warehouse/Operations/Parcel.Status`.

A document may contain SQL, Python or YAML according to the resource and item kind. Use the [Lakehouse pipeline](../guides/lakehouse-pipeline.md) and [Warehouse pipeline](../guides/warehouse-pipeline.md) for complete, parser-checked forms rather than treating this concept page as an authoring reference.

Files under an item can also support documents without becoming resources themselves. For example, Lakehouse modules and data under `lib/` can travel with the item, but they are not independently selectable Tables, Folders, Tests or Views.

## Artefacts realise and run resources

An artefact is installed output that Weaver builds from project source. Depending on the declaration, Build may install:

- the physical definition of a table, folder or view;
- runnable work used by Load;
- runnable work used by Test;
- metadata that records identity, dependencies and the installed generation.

The relationship is not one resource to one visible Fabric object.

A parcel Table has a physical table definition and, when Weaver is responsible for populating it, installed work that Load can run. A View has a physical view definition but no separate Load step: querying the view is its behaviour. A Test has installed work that Test can run, but it does not materialise a business table. Helper source can support runnable work without becoming a separately operated resource.

These differences explain why Build, Load and Test remain separate:

- **Build** installs or updates the resource definitions and artefacts.
- **Load** runs installed loadable resources.
- **Test** runs installed Tests and Assumptions.

See [How Weaver works](how-weaver-works.md#build) for the lifecycle and the [Load contract](../contracts/load.md#execution-boundary) for the installed-source boundary.

## Operate resources, not generated internals

Generated artefacts are managed output. Do not edit them in Fabric as the source of a lasting change. Edit the declaring document or its supporting project source, run `weaver check`, and Build the owning item again.

Likewise, command selection stays in the public logical vocabulary:

```bash
weaver build --item Lakehouse/Landing
weaver load Lakehouse/Landing \
  --name Tables/Parcel.Event
weaver test Warehouse/Operations
```

`--name` selects an installed loadable resource, not an implementation file or procedure created by Build. A Lakehouse name can include `Tables/` or `Files/`; a Warehouse name is `Schema.Object`. Name selection deliberately runs only those named resources, while item-wide Load applies dependency ordering. The [CLI reference](../reference/cli.md#load-test-and-health-selection) and [Load contract](../contracts/load.md#dependencies) own those operational details.

The practical rule is simple: preserve project documents as the source of intent, use Build to install their current generation, and use Load, Test and Health to operate and inspect the resulting estate. Start with [First project](../get-started/first-project.md) to see one Table and one Test move through that lifecycle.
