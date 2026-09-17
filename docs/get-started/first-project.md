# First project

This path creates one Warehouse table and one Test from deterministic T-SQL. It covers the normal Weaver lifecycle without requiring Spark-authored code:

```text
initialise → check → build → load → test → health → workflow
```

## 1. Create the project

Choose a Fabric workspace you can modify. The command creates or reuses the catalogue Warehouse and project Warehouse, then writes the local project:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-ops \
  --catalogue Catalogue \
  --warehouse Operations \
  --no-example
```

Current versions of `weaver initialise` also create or reuse the default `Weaver` Environment and write its local definition. This Warehouse-only example does not use or publish that Environment.

Without `--non-interactive`, setup reviews the choices before changing Fabric. For unattended setup, provide the project folder, workspace and Warehouse, then add `--non-interactive`.

Move into the generated project:

```bash
cd parcel-ops
```

The relevant files are:

```text
parcel-ops/
├── workspace-config.yml
├── workflow.yml
├── Environment/
│   └── Weaver.Environment/
└── Warehouse/
    └── Operations/
```

`workspace-config.yml` binds the logical `Warehouse/Operations` item to the physical Warehouse selected during setup. The catalogue is a separate Warehouse that holds Weaver's installed and operational state.

## 2. Declare a table

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

The containing item chooses the SQL dialect: a `.sql` document directly under a Warehouse item is T-SQL. Its filename and `Table ID` identify the same `Schema.Object`.

## 3. Declare a Test

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

A Warehouse Test supplies two result sets: the expected rows, then the actual rows. Weaver compares them by the declared primary key.

## 4. Check the project locally

```bash
weaver check
```

`check` parses and validates the current project without contacting Fabric. It catches repository, identity and metadata errors, but it does not prove workspace permissions or Fabric connectivity. Use `weaver doctor --workspace "Parcel Development"` to check access to the Fabric services Weaver needs.

## 5. Build the structure

```bash
weaver build
```

From the project root, Weaver reads `workspace-config.yml` automatically. Build applies the structural changes declared by the project and installs the Table and Test definitions. It does not run the table's query to populate business rows.

The first build also creates the catalogue tables in the configured catalogue Warehouse.

## 6. Load the rows

```bash
weaver load Warehouse/Operations
```

Load runs the installed loadable objects owned by the logical item. Here it executes the installed Warehouse load for `Parcel.Status` and records the outcome in the catalogue.

## 7. Run the Test

```bash
weaver test Warehouse/Operations
```

Test runs the installed Test and records whether the actual rows match the expected rows. A failed or invalid Test returns a non-zero exit status.

## 8. Read health

```bash
weaver health --item Warehouse/Operations
```

Health reports the Build, Load and Test state for the selected item. It exits zero only when the selected estate is Green; read the section status and finding when it is Amber or Red.

## 9. Run the lifecycle as a workflow

Initialisation generated `workflow.yml` with a `full` workflow:

```yaml
workflows:
  full:
    - build
    - load
    - test
    - health
```

Run it with:

```bash
weaver workflow full
```

The four commands run in order in one Session. A workflow stops when a command returns a non-zero result.

## Next runs

After changing a declaration, run the stages individually or use the workflow:

```bash
weaver check
weaver workflow full
```

Build, Load and Test are separate operations. Build installs changed declarations, Load runs installed data work, and Test checks the installed estate. A wipe is not part of the normal edit-build-load-test loop.
