# First project

This path creates one Warehouse table from a deterministic T-SQL query. It exercises project generation, local validation, structural build and data load without requiring Spark-authored code.

## 1. Create the project

Choose a Fabric workspace you can modify. The command below creates or reuses the catalogue Warehouse, project Warehouse and Environment, then writes the local project. It does not publish the Environment.

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-ops \
  --catalogue Catalogue \
  --environment Weaver \
  --warehouse Operations \
  --no-example
```

Without `--non-interactive`, setup reviews the choices before changing Fabric. For unattended setup, provide the project folder, workspace and at least one Lakehouse or Warehouse, then add `--non-interactive`.

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

`workspace-config.yml` binds the logical `Warehouse/Operations` item to the physical Warehouse selected during setup. The catalogue is a separate Warehouse whose `_` schema stores Weaver's installed and operational state.

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

## 3. Check the project locally

```bash
weaver check
```

`check` parses and validates the current project without contacting Fabric. It catches repository, identity and metadata errors, but it does not prove workspace permissions or Fabric connectivity. Use `weaver doctor --workspace "Parcel Development"` for those crossings.

## 4. Build the structure

```bash
weaver build
```

From the project root, Weaver reads `workspace-config.yml` automatically. Build parses the repository, resolves the target, compares it with Fabric and the catalogue, prepares a frozen build bundle, installs the selected structural actions, and updates the catalogue. It does not run the table's query to populate business rows.

The first build also creates the catalogue tables in the configured catalogue Warehouse.

## 5. Load the rows

```bash
weaver load Warehouse/Operations
```

Load runs installed loadable objects for the named logical item. In this example it executes the installed Warehouse load for `Parcel.Status` and records the outcome in the catalogue.

Finish by reading the estate's operational state:

```bash
weaver health --item Warehouse/Operations
```

`health` exits zero only when the selected estate is Green. A recent successful load can still coexist with an Amber or Red finding that needs attention; read the section status and finding rather than relying on command completion alone.

## Next runs

After changing the declaration, repeat:

```bash
weaver check
weaver build
weaver load Warehouse/Operations
weaver health --item Warehouse/Operations
```

Build selects changed and dependency-impacted objects from the declared repository and installed state. A wipe is not part of the normal edit-build-load loop.
