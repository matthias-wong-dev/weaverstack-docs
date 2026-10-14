# Workspace and environment mappings

Keep project documents and logical item names unchanged when deploying elsewhere. A workspace configuration selects the physical workspace, catalogue and targets; selecting another file changes where the same source is installed.

Three controls do different jobs: the configuration binds the estate, the selected file chooses development or production, and a published Fabric Environment supplies the Python packages used by Spark work. A target rename neither changes a model’s native data connection nor publishes a runtime.

## Bind the project to Fabric

For the working [Warehouse pipeline](../warehouse/first-project.md), save this file beside the project and use the existing workspace, catalogue and physical Warehouse names from your setup:

```yaml title="workspace-development.yml"
workspace: Parcel Operations
catalogue: Warehouse/ParcelCatalogueDev
targets:
  Warehouse/Operations: ParcelOperationsDev
```

`Warehouse/Operations` is the logical item containing `Parcel.StatusEvent` and the `Parcel.CurrentStatus` View. `ParcelOperationsDev` is its physical Fabric Warehouse. The catalogue is another physical Warehouse that holds the installed definitions, bindings and operation results.

```bash
weaver check .
weaver build . --item Warehouse/Operations --workspace-config workspace-development.yml
weaver load --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Build reads `targets` and records settled physical bindings. Catalogue-backed Load, Test and Health use those recorded bindings, not replacement values in an edited configuration. Changing `targets` does not retarget installed work until Build installs it.

The exact filename `workspace-config.yml` is discovered only in the process’s current working directory. Other names, including the one above, require `--workspace-config`; filenames do not confer development or production semantics. See [Workspace configuration](../reference/configuration-files/workspace-config.md) for all keys and precedence.

## Keep development and production bindings separate

For a whole-project example including model and Report targets, use the complete [managed-source Parcel snapshot](../semantic-models/managed-sources.md). This deliberately replaces the first Warehouse exercise with its Operations `Parcel.Delivery` source, Warehouse-backed Delivery partition and inline Depot reference data. It does not add that model to the StatusEvent/View pipeline by renaming a source.

The snapshot supplies this development configuration:

```yaml title="workspace-dev.yml"
workspace: Parcel Fabric Development
catalogue: Warehouse/Parcel_Catalogue_Dev
targets:
  Warehouse/Operations: Parcel_Operations_Dev
  SemanticModel/Parcel: Parcel_Dev
  Report/Parcel: Parcel_Report_Dev
data_sources:
  Warehouse/Operations: Warehouse/Parcel_Operations_Dev
```

A production configuration for that same project can use:

```yaml title="workspace-prod.yml"
workspace: Parcel Fabric Production
catalogue: Warehouse/Parcel_Catalogue
targets:
  Warehouse/Operations: Parcel_Operations
  SemanticModel/Parcel: Parcel
  Report/Parcel: Parcel_Report
data_sources:
  Warehouse/Operations: Warehouse/Parcel_Operations
```

Use your intended physical names and existing compatible catalogue/Operations targets. For an exercise, use two disposable workspaces, not a real production estate. Model/Report deployment and refresh require their service permissions; Import refresh also requires an existing supported connection and credentials with Warehouse SQL access. Weaver does not create credentials.

Choose one file for the entire lifecycle. For development:

```bash
weaver check .
weaver build . --item Warehouse/Operations --workspace-config workspace-dev.yml
weaver build . --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-dev.yml
weaver load --workspace-config workspace-dev.yml
weaver test --workspace-config workspace-dev.yml
weaver health --workspace-config workspace-dev.yml
```

Use `workspace-prod.yml` for the same sequence at the production destination. Source-data and model/Report definitions use **separate Build calls**. The model is deployed before its linked Report. Load runs installed source work and model refreshes; Test runs installed validations. Reports participate in Build only.

## Keep destination names separate from native sources

`targets` chooses where items deploy. `data_sources` maps an exact shared M expression name to a supported typed Lakehouse/Warehouse source. Here the native expression is named `Warehouse/Operations`, and the Delivery partition still navigates `[Parcel].[Delivery]`. The `Weaver.Source` annotation supplies managed lineage; neither a target name nor lineage alone rewrites arbitrary M, grants SELECT rights or creates a service connection.

`--bind-data-sources` requests supported binding to an existing matching connection. Explicit `--data-source` mappings can override configured mappings; only supported native expression forms are substituted. The [managed-source task](../semantic-models/managed-sources.md#1-configure-destination-and-source-separately) owns that complete declaration and connection procedure.

Inspect the deployed shared expression and model refresh in each workspace. Then verify the actual Report-to-model binding: `Parcel_Report_Dev` should use `Parcel_Dev`; `Parcel_Report` should use `Parcel`. The [Report environment task](../reports/environments.md) shows this binding check on the separate inline model snapshot. An unrelated authored `byConnection` remains authored rather than automatically switching with target names.

## Apply the mapping to Lakehouses and runtime

A Lakehouse target uses the same logical-to-physical mapping. For the existing [Landing → Dispatch connection](connected-items.md), keep both bindings in its complete configuration; native project references still name `Lakehouse/Landing` rather than its physical development name.

An `environment` binding selects an existing published Fabric Environment for Spark work. It does not create or publish that Environment. Desktop Lakehouse Build/Load/Test, including generated Spark SQL work, needs the matching hosted Weaver runtime; a Spark-backed Build checks compatibility before mutation even though it does not call authored `read()` methods. Pure Warehouse T-SQL and standalone Power BI avoid that Spark prerequisite. [Running Python in Fabric](../lakehouse/runtime.md) owns publication and attached-notebook runtime setup.

A `mirror` binding selects a source catalogue for deliberate same-workspace [Mirror](mirror.md). Loading the file does not run Mirror; ordinary development needs no mirrored baseline.

With one configuration selecting the intended estate, [read Catalogue and Health](catalogue-and-health.md) to see what was installed and what happened there. [Logical and physical items](../core-concepts/logical-and-physical-items.md) explains why the project keeps its identities while physical bindings change.
