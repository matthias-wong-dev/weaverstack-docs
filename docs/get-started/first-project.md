# First project

This project declares one Warehouse Table and one Test in deterministic T-SQL. It exercises the normal lifecycle without Spark-authored code:

```text
initialise → check → build → load → test → health → weaver workflow full
```

The declarations below are also kept as a [checked example fixture](https://github.com/matthias-wong-dev/weaverstack-docs/tree/main/examples/parcel-first-project).

## Prerequisites

- [Weaver installed](installation.md).
- Access to a Microsoft Fabric workspace you can modify.
- Permission to create or reuse two Warehouses and the default Fabric Environment.
- A working credential path, confirmed with `weaver doctor --workspace "Parcel Development"`.

The names in the commands are examples. Replace `Parcel Development`, `Catalogue`, and `Operations` if your Fabric items use other names.

## 1. Initialise the project

Run this from the directory that should contain the new `parcel-ops` folder:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-ops \
  --catalogue Catalogue \
  --warehouse Operations \
  --no-example
```

Initialisation creates or reuses the catalogue Warehouse and project Warehouse, then writes the project. It also creates or reuses the default `Weaver` Environment and writes its local definition. This Warehouse-only project does not publish or use that Environment.

Without `--non-interactive`, the command lets you review the choices before it changes Fabric. For unattended setup, provide the project folder, workspace, and Warehouse as above, then add `--non-interactive`; that mode cannot fall back to browser sign-in.

Move to the project root:

```bash
cd parcel-ops
```

You should now have these generated paths:

```text
parcel-ops/
├── README.md
├── workspace-config.yml
├── workflow.yml
├── Environment/
│   └── Weaver.Environment/
└── Warehouse/
    └── Operations/
```

`workspace-config.yml` binds the logical `Warehouse/Operations` item to the physical Warehouse selected during setup. The separate catalogue Warehouse holds Weaver's installed and operational state. [How Weaver works](../core-concepts/how-weaver-works.md) explains this distinction.

## 2. Declare the Table

Create `Warehouse/Operations/Parcel.Status.sql`:

```sql
/*
Table ID: Parcel.Status

Description: Current status for the parcels in this example.

Lineage: A deterministic VALUES seed.

Primary key: Parcel ID

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
*/
select v.ParcelId as [Parcel ID]
     , v.ParcelStatus as [Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'Delivered')
) as v (ParcelId, ParcelStatus)
```

A `.sql` document directly under a Warehouse item uses T-SQL. Its filename and `Table ID` must identify the same `Schema.Object`.

## 3. Declare the Test

Create `Warehouse/Operations/tests/Parcel.StatusMatches.sql`:

```sql
/*
Test ID: Parcel.StatusMatches

Description: Parcel status contains the rows declared by this example.

Primary key: Parcel ID
*/
select v.ParcelId as [Parcel ID]
     , v.ParcelStatus as [Status]
from (values
    ('P-1001', 'In transit'),
    ('P-1002', 'Delivered')
) as v (ParcelId, ParcelStatus);

select [Parcel ID], [Status]
from [Parcel].[Status];
```

A Warehouse Test returns the expected rows first and the actual rows second. Weaver compares the result sets by the declared primary key.

At this point the authored files are:

```text
Warehouse/Operations/
├── Parcel.Status.sql
└── tests/
    └── Parcel.StatusMatches.sql
```

## 4. Check the project locally

```bash
weaver check
```

A valid project prints:

```text
Project valid.
```

`check` parses and validates the current project without contacting Fabric. It catches declaration, identity, and metadata errors; it does not check workspace permissions or Fabric connectivity.

## 5. Build the structure

```bash
weaver build
```

From the project root, Weaver reads `workspace-config.yml` automatically. Build applies the declared structure and installs the Table and Test definitions. It does not run the Table query to populate business rows. The first build also creates Weaver's catalogue tables in the configured catalogue Warehouse.

Continue only after Build reports success. For the source-to-installed-state model, see [Build in How Weaver works](../core-concepts/how-weaver-works.md#build).

## 6. Load the rows

```bash
weaver load Warehouse/Operations
```

Load runs the installed work owned by the logical item. The successful report names `Parcel.Status`, marks it `succeeded`, and records the outcome in the catalogue. Load uses the installed definition, so rebuild after changing the source. See the [Load contract](../contracts/load.md) for selection, ordering, and failure behaviour.

## 7. Run the Test

```bash
weaver test Warehouse/Operations
```

The successful report names `Parcel.StatusMatches` as passed. A failed Test, or a Test that cannot run, returns a non-zero status.

## 8. Read health

```bash
weaver health --item Warehouse/Operations
```

After the successful Build, Load, and Test, the report shows `Weaver Health  Green` and Green Build, Load, and Tests sections. Health exits `0` only for Green; Amber and Red reports include findings and exit `1`.

## 9. Run the lifecycle as a workflow

Initialisation generated a `full` workflow. Its declaration is:

```yaml
workflows:
  full:
    - build
    - load
    - test
    - health
```

Run it from the project root:

```bash
weaver workflow full
```

The commands run in order in one Session. The workflow stops at the first non-zero command result. The [CLI reference](../reference/cli.md) covers workflow and item-selection syntax.

## Next action

After changing either declaration, validate and rerun the lifecycle:

```bash
weaver check
weaver workflow full
```

Build, Load, and Test remain separate operations: Build installs changed declarations, Load runs installed data work, and Test checks the installed estate. Wipe is not part of the normal loop.

Continue with the [Warehouse pipeline](../guides/warehouse-pipeline.md) for a larger SQL project, or the [Lakehouse pipeline](../guides/lakehouse-pipeline.md) when the project needs Delta, files, or Spark-authored work.
