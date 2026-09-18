# Author a Warehouse pipeline

This guide adds a T-SQL Table and a dependent View to an existing Weaver Warehouse item. The entire path uses the Warehouse SQL endpoint and does not require Spark or a published Fabric Environment.

## Prerequisites

- [Install Weaver](../getting-started/installation.md) and confirm `weaver --version` works.
- Complete [First project](../getting-started/first-project.md), or initialise a project with the logical item `Warehouse/Operations`:

```bash
weaver initialise \
  --workspace "Parcel Development" \
  --project-folder ./parcel-warehouse \
  --catalogue Catalogue \
  --warehouse Operations \
  --no-example
cd parcel-warehouse
```

Initialisation records the physical workspace, catalogue Warehouse and target Warehouse in `workspace-config.yml`. The declarations below contain no tenant-specific names.

## Add the Table

Create these files:

```text
parcel-warehouse/
├── workspace-config.yml
└── Warehouse/
    └── Operations/
        ├── Parcel.StatusEvent.sql
        └── Parcel.CurrentStatus.sql
```

Create `Warehouse/Operations/Parcel.StatusEvent.sql`:

```sql
/*
Table ID: Parcel.StatusEvent

Description: One row per parcel status event.

Lineage: A deterministic carrier feed represented by this example.

Primary key: Parcel ID, Event sequence

Schema:
  Parcel ID: varchar(20)
  Event sequence: int
  Status: varchar(30)
  Depot: varchar(50)
*/
select v.[Parcel ID]
     , v.[Event sequence]
     , v.[Status]
     , v.[Depot]
from (values
    ('P-1001', 1, 'Accepted', 'North'),
    ('P-1001', 2, 'In transit', 'Central'),
    ('P-1002', 1, 'Delivered', 'South')
) as v ([Parcel ID], [Event sequence], [Status], [Depot]);
```

A `.sql` declaration directly under a Warehouse item uses T-SQL. `Table ID` and the filename identify the same `Schema.Object`. The query supplies the rows that Load reconciles into the declared table.

## Add the View

Create `Warehouse/Operations/Parcel.CurrentStatus.sql`:

```sql
/*
View ID: Parcel.CurrentStatus

Description: The latest recorded status for each parcel.

Lineage: $Parcel.StatusEvent

Primary key: Parcel ID
*/
with ranked as (
    select [Parcel ID]
         , [Status]
         , [Depot]
         , row_number() over (
               partition by [Parcel ID]
               order by [Event sequence] desc
           ) as [Event rank]
    from [Parcel].[StatusEvent]
)
select [Parcel ID]
     , [Status]
     , [Depot]
from ranked
where [Event rank] = 1;
```

`View ID` makes this a View rather than a loadable Table. Its lineage reference records the dependency on `Parcel.StatusEvent`. Build creates the view definition; Load populates the Table it reads.

## Check and build

From the project root, run:

```bash
weaver check
weaver build --item Warehouse/Operations
```

A successful check confirms that the two files parse, their identities agree with their paths and the dependency resolves. It does not submit the T-SQL. Build applies the Table and View structure and installs the Table's load definition.

Neither command needs Spark for this Warehouse-only item. Do not publish an Environment for these T-SQL declarations; no authored Python runs in Fabric.

## Preview and load the Table

Preview the installed work, then run it:

```bash
weaver load Warehouse/Operations --dry-run
weaver load Warehouse/Operations
weaver health --item Warehouse/Operations
```

The dry run should include `Parcel.StatusEvent`; the View is not separate load work. After Load succeeds, query the Warehouse SQL endpoint:

```sql
select [Parcel ID], [Status], [Depot]
from [Parcel].[CurrentStatus]
order by [Parcel ID];
```

The observable result is two rows: `P-1001` at `Central` with status `In transit`, and `P-1002` at `South` with status `Delivered`. Health should report the Warehouse item as Green.

For a targeted rerun, select the installed Table by its Warehouse object name:

```bash
weaver load Warehouse/Operations \
  --name Parcel.StatusEvent
```

Name selection runs exactly the named installed object. Use item-wide selection when Weaver should apply dependency ordering; the [Load contract](../reference/operation-behaviour/load.md) defines both forms.

## Next action and troubleshooting

Replace the `values` source with a query over your landed Warehouse data, keep the declared schema aligned with its result and rerun `check`, `build` and `load`. [How Weaver works](../core-concepts/how-weaver-works.md) explains why source changes take effect only after Build.

If a command rejects an option or object name, check the [CLI reference](../reference/cli.md). If Fabric access fails, use `weaver doctor` as described in [Installation](../getting-started/installation.md). If the project lifecycle is unfamiliar, return to [First project](../getting-started/first-project.md).
