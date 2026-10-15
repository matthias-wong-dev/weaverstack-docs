# Workspace and environment mappings

Where should the same project deploy? Keep its documents and logical item names unchanged. A workspace configuration selects the physical workspace, catalogue and targets; selecting another file changes where the same source is installed.

Three controls do different jobs: the configuration binds the estate, the selected file chooses development or production, and a published Fabric Environment supplies the Python packages used by Spark work. A target rename neither changes a model’s native data connection nor publishes a runtime.

## Bind the project to Fabric

Continue the [Landing → Operations connection](connected-items.md). Keep its Folder, Event and CurrentStatus Tables, and the independent and cross-item Operations work in the same project. Save the existing bindings as `workspace-development.yml`; keep the workspace and physical names from that connection:

```yaml title="workspace-development.yml"
workspace: Parcel Development
catalogue: Warehouse/Catalogue
environment: Weaver
targets:
  Lakehouse/Landing: Landing
  Warehouse/Operations: Operations
```

Use the workspace, catalogue, published runtime and physical names from your working configuration. `Lakehouse/Landing` and `Warehouse/Operations` remain logical identities in the source. Selecting this named file is explicit on each command:

```bash
weaver check .
weaver build . --item Lakehouse/Landing --item Warehouse/Operations --workspace-config workspace-development.yml
weaver load --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

The logical Shortcut has no Load, but the additional Operations LakehouseCurrentStatus Table does. Item-wide Load orders selected source work across the boundary. Test runs the generated Lakehouse and Warehouse validations; they remain beside their original pipelines.

Build reads `targets` and records settled physical bindings. Catalogue-backed Load, Test and Health use those recorded bindings, not replacement values in an edited configuration. Changing `targets` does not retarget installed work until Build installs it.

The exact filename `workspace-config.yml` is discovered only in the process’s current working directory. Other names, including the one above, require `--workspace-config`; filenames do not confer development or production semantics. See [Workspace configuration](../reference/configuration-files/workspace-config.md) for all keys and precedence.

## Keep development and production bindings separate

Use a second configuration to install that same Landing/Operations source in another workspace. For example:

```yaml title="workspace-production.yml"
workspace: Parcel Production
catalogue: Warehouse/ParcelCatalogue
environment: WeaverProduction
targets:
  Lakehouse/Landing: ParcelLanding
  Warehouse/Operations: ParcelOperations
```

Use existing compatible catalogue and item targets, and a matching published runtime in that destination. For this exercise, both workspaces should be disposable. Repeat the same commands with `--workspace-config workspace-production.yml`; the Shortcut still names `Lakehouse/Landing/Tables/Parcel.Event`, not the production Lakehouse's physical name. Keep `workspace-development.yml` selected for the following Health and development pages.

### A model and Report variation

Add the native model and linked Report to this same working project. From its root:

```bash
weaver initialise --workspace "Parcel Development" --project-folder . --semantic-model Parcel --example Parcel
```

The original pipelines remain in place. Parcel’s native model has inline sample data; the additional ParcelLakehouse and ParcelWarehouse models read their respective managed CurrentStatus sources. [Managed sources](../semantic-models/managed-sources.md) explains their connection requirements.

Initialise adds the targets to the default `workspace-config.yml`. Copy its new model/Report bindings into the existing development configuration, keeping all source, catalogue and runtime bindings:

```yaml title="Add under targets in workspace-development.yml"
  SemanticModel/Parcel: Parcel
  Report/Parcel: Parcel
  SemanticModel/ParcelLakehouse: ParcelLakehouse
  SemanticModel/ParcelWarehouse: ParcelWarehouse
```

Add the corresponding destinations to `workspace-production.yml`:

```yaml title="Add under targets in workspace-production.yml"
  SemanticModel/Parcel: Parcel_Production
  Report/Parcel: Parcel_Report_Production
  SemanticModel/ParcelLakehouse: ParcelLakehouse_Production
  SemanticModel/ParcelWarehouse: ParcelWarehouse_Production
```

Use existing compatible catalogue and source targets in both disposable workspaces, and service permissions for the model/Report operations. The source-backed Import models need existing supported connections with SQL access. Weaver does not create credentials.

Choose one configuration for the whole lifecycle:

```bash
weaver check
weaver build --item Lakehouse/Landing --item Warehouse/Operations --workspace-config workspace-development.yml
weaver build --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-development.yml
weaver load --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Repeat with `workspace-production.yml` for that destination. Source-data and Power BI definitions use separate Builds. The inline model and linked Report do not depend on a source workload; the additional managed models participate in source Load ordering. Reports have no separate Load or Test.

## Keep destination names separate from native sources

`targets` chooses where items deploy. `Weaver.Source` in an additional model identifies its logical managed source; Build resolves that source’s connector and metadata. Optional `data_sources` mappings can choose a different supported physical source without editing logical source declarations. These mappings do not rewrite arbitrary M or grant SQL access.

`--bind-data-sources` requests a supported existing matching connection. Explicit `--data-source` values can override configured source mappings. [Managed sources](../semantic-models/managed-sources.md#1-configure-destination-and-source-separately) owns the declaration and connection procedure.

Check the source-backed models’ refreshes in each workspace. In service lineage view, the development Parcel Report must link to its development inline Parcel model; the production Report must link to Parcel_Production in the production workspace. The [Report environment task](../reports/environments.md) shows this ordinary binding check. An unrelated authored `byConnection` remains authored instead of automatically switching destinations.

## Apply the mapping to Lakehouses and runtime

A Lakehouse target uses the same logical-to-physical mapping. For the existing [Landing → Operations connection](connected-items.md), keep both bindings in its complete configuration; native project references still name `Lakehouse/Landing` rather than its physical development name.

An `environment` binding selects an existing published Fabric Environment for Spark work. It does not create or publish that Environment. Desktop Lakehouse Build/Load/Test, including generated Spark SQL work, needs the matching hosted Weaver runtime; a Spark-backed Build checks compatibility before mutation even though it does not call authored `read()` methods. Pure Warehouse T-SQL and standalone Power BI avoid that Spark prerequisite. [Running Python in Fabric](../lakehouse/runtime.md) owns publication and attached-notebook runtime setup.

A `mirror` binding selects a source catalogue for deliberate same-workspace [Mirror](mirror.md). Loading the file does not run Mirror; ordinary development needs no mirrored baseline.

With one configuration selecting the intended estate, [read Catalogue and Health](catalogue-and-health.md) to see what was installed and what happened there. [Logical and physical items](../core-concepts/logical-and-physical-items.md) explains why the project keeps its identities while physical bindings change.
