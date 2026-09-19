# First project

This tutorial creates one Warehouse Table and one Test, then runs the complete Weaver lifecycle:

```text
initialise → check → build → load → test → health → workflow full
```

Before starting, [install Weaver and check access to Fabric](installation.md). The examples use a workspace named `Parcel Development`; replace that name if your workspace is different.

## 1. Initialise the project

From the directory that should contain the new project, run:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-ops \
  --catalogue Catalogue \
  --environment Weaver \
  --warehouse Operations \
  --no-example \
  --non-interactive
```

This fully specified command does not start the setup wizard. Weaver creates or reuses the `Catalogue` and `Operations` Warehouses and the `Weaver` Environment, creates `parcel-ops`, and writes its workspace configuration, workflow, Environment definition and empty Warehouse source directory. It does not publish the Environment.

`Operations` is now a Weaver-managed physical target. Build reconciles selected managed items and may prune undeclared co-located content. Keep manually supplied or irreplaceable source data in a separate physical item and connect it through a physical Shortcut; [Logical and physical items](../core-concepts/logical-and-physical-items.md#choose-one-of-three-ownership-cases) explains the boundary.

**Expected result:** the command ends with `Weaver project ready in .../parcel-ops.` and reports each Fabric item as created or already existing. Environment publication is deferred.

Move into the project:

```bash
cd parcel-ops
```

The generated project contains these paths:

```text
parcel-ops/
├── README.md
├── workspace-config.yml
├── workflow.yml
├── Environment/
│   └── Weaver.Environment/
└── Warehouse/
    └── Operations/
        └── .gitkeep
```

**Expected result:** your shell is in `parcel-ops`, beside `workspace-config.yml`. That file binds the logical item `Warehouse/Operations` to the Fabric Warehouse named `Operations`.

## 2. Add a Table

Create `Warehouse/Operations/Parcel.Status.sql` with this complete content:

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
) as v (ParcelId, ParcelStatus);
```

**Expected result:** the Warehouse item now contains a Table document named `Parcel.Status`. Its query will produce two rows when Load runs it.

## 3. Add a Test

A Test compares expected and actual rows. The optional primary key helps correlate diagnostic rows when the two sides differ.

Create `Warehouse/Operations/tests/Parcel.StatusMatches.sql` with this complete content:

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

The first query returns the expected rows. The second returns the actual rows from the Table.

**Expected result:** the authored part of the item is now:

```text
Warehouse/Operations/
├── Parcel.Status.sql
└── tests/
    └── Parcel.StatusMatches.sql
```

## 4. Check the project

Validate the source locally:

```bash
weaver check
```

**Expected result:** Weaver prints:

```text
Project valid.
```

Check parses the project and validates its declarations without contacting Fabric.

## 5. Build the installed estate

Install the Table and Test definitions:

```bash
weaver build
```

Weaver reads `workspace-config.yml` from the project root, creates the catalogue tables on the first Build and installs the Warehouse definitions. Build does not run the Table query that produces the two parcel rows.

**Expected result:** the command exits successfully. Its `Installation` summary reports no failed actions, and the installed estate contains `Parcel.Status` and `Parcel.StatusMatches`.

## 6. Load the Table

Run the installed data work for the Warehouse item:

```bash
weaver load Warehouse/Operations
```

**Expected result:** the report lists `Parcel.Status` as succeeded. On this first Load it reads and inserts two rows, with no rejected rows.

Load runs the definition installed by the last successful Build. If you later edit the Table document, Build again before loading it.

## 7. Run the Test

Run the installed validation:

```bash
weaver test Warehouse/Operations
```

**Expected result:** the report lists `Parcel.StatusMatches` as passed with `0 missing, 0 unexpected`, and the summary reports one passed Test.

## 8. Read health

Read the resulting state of this item:

```bash
weaver health --item Warehouse/Operations
```

**Expected result:** the report begins with `Weaver Health  Green`; its Build, Load and Tests sections are Green.

Health reads installed and operational state. It does not run Build, Load or Test again.

## 9. Run the lifecycle as a workflow

Initialisation created this `full` workflow in `workflow.yml`:

```yaml
workflows:
  full:
    - build
    - load
    - test
    - health
```

Run it:

```bash
weaver workflow full
```

Review and confirm the four displayed commands when prompted.

**Expected result:** Build, Load, Test and Health run in order in one Session. The Test passes, Health remains Green and the command ends with `✓ Commands completed: 4`.

For an unattended shell, authorise the workflow explicitly instead of piping a response into stdin:

```bash
weaver workflow full --yes --non-interactive
```

Piped input is not a real terminal confirmation. `--non-interactive` also prevents browser sign-in, so unattended credentials must already be configured.

You now have a working Weaver project. Read [How Weaver works](../core-concepts/how-weaver-works.md) for the model behind this lifecycle, or continue with [Build a Warehouse pipeline](../basics/warehouse-pipeline.md). Exact command options and failure behaviour are in [Reference](../reference/index.md).
