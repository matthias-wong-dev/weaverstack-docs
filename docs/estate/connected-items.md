# Connect items and dependencies

Keep a producer’s logical name when another item reads it. Weaver then installs the connection in order and can coordinate selected source loads with their consumers, rather than leaving each item with a schedule that guesses when another has finished.

Continue from [Landing’s working Python pipeline](../lakehouse/python.md): Folder `Parcel.Events` feeds Table `Parcel.Event`; the [Spark SQL extension](../lakehouse/spark-sql.md) adds `Parcel.CurrentStatus`. Direct entrants can use the complete [parcel-lakehouse snapshot](https://github.com/matthias-wong-dev/weaverstack-docs/tree/main/examples/parcel-lakehouse) and complete those item tasks first. This extension presents that existing Event in a Warehouse; it does not replace Landing’s source or the separate Operations StatusEvent pipeline.

## Present Landing’s Event in Dispatch

Use an existing disposable `ParcelDispatchDev` Warehouse in the same workspace as Landing and its catalogue. Add its binding to the working configuration, leaving all existing bindings and runtime settings intact:

```yaml title="Add under targets in workspace-config.yml"
  Warehouse/Dispatch: ParcelDispatchDev
```

If you need a complete configuration rather than an addition, use this shape and replace workspace/catalogue/runtime/physical Landing names with the ones already used by your working checkpoint:

```yaml title="workspace-config.yml"
workspace: Parcel Development
catalogue: Warehouse/Catalogue
environment: Weaver
targets:
  Lakehouse/Landing: Landing
  Warehouse/Dispatch: ParcelDispatchDev
```

The catalogue, Landing Lakehouse, published runtime and Dispatch Warehouse must exist with the required permissions. [Running Python in Fabric](../lakehouse/runtime.md) owns the runtime setup. Do not bind externally owned data as an ordinary managed target: Build may prune undeclared co-located content within selected managed items.

Create `Warehouse/Dispatch/shortcuts.yml`:

```yaml
logical:
  "Warehouse/Dispatch/Parcel.Event": "Lakehouse/Landing/Tables/Parcel.Event"
```

The mapping reads from destination to source. Build creates a Dispatch View over the existing Landing Table and records the managed relationship. Warehouse Shortcut Views have no separate Load.

```bash
weaver check .
weaver build . --item Lakehouse/Landing --item Warehouse/Dispatch
weaver load Lakehouse/Landing
weaver health --item Lakehouse/Landing --item Warehouse/Dispatch
```

Build installs the selected source before the Shortcut. Query the Dispatch SQL endpoint after Landing’s data is available there:

```sql
select [Parcel ID], [Event sequence], [Status]
from [Parcel].[Event]
order by [Parcel ID], [Event sequence];
```

The View should expose the same three events as Landing. The source identity in `shortcuts.yml` stays unchanged when you choose different physical destinations through [workspace mappings](environments.md).

## Order selected work, not every related item

Python imports and supported Warehouse SQL references normally supply document dependencies without a second authored graph. An explicit `Dependencies` declaration replaces inference, including an empty list. Spark SQL data documents still require that field explicitly. The item graph must be acyclic.

For a connection with loadable work on both sides, select both logical items in an item-wide Load. Weaver orders selected producers before consumers and inserts supported OneLake-publication and SQL-endpoint readiness barriers where the installed cross-engine path requires them. The View above reads the source directly, so there is no Dispatch data load to add.

Dependencies never add an unnamed item. Build changes affected descendants only inside selected items; item-wide Load orders only its selected work. Plain `--name` Load is an operator override without inferred dependency ordering or readiness barriers. [Run part of an estate](selective-runs.md) shows how deliberate ancestor/descendant expansion restores ordering within the requested boundary.

A physical Shortcut or a directly qualified external relation is different: it identifies data outside this project’s ownership, not a managed producer that Weaver can Build or order. See [Shortcuts and existing data](../lakehouse/shortcuts.md) for that boundary and [Dependencies](../core-concepts/dependencies.md) for the complete reasoning.

## Extend the same coordination to a model

A semantic model’s `Weaver.Source` annotation can connect its Table to a managed source. Estate Load then places selected source work before model refresh, and Health can show a model behind its source. A linked Report depends on the model for deployment, but has no data Load or Test of its own.

[Connect a managed Fabric source](../semantic-models/managed-sources.md) is the complete source-backed checkpoint for this extension. It deliberately uses Operations `Parcel.Delivery` with the Parcel model’s Warehouse-backed Delivery partition and inline Depot reference data. It is not a combined runnable version of Landing Event and the first Warehouse StatusEvent example. Use that snapshot as a whole: source-data Build and model/Report Build remain separate calls, and native source mapping, permissions and existing connections remain additional controls.

Once the connections work, [map development and production](environments.md) without changing those logical source identities. [How Weaver works](../core-concepts/how-weaver-works.md) follows the source into installed operations; [Design philosophy](../core-concepts/design-philosophy.md) explains the choices behind keeping native authoring and queryable state.
