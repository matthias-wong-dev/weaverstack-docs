# Choose development and production targets

Use the same authored model and Report in two workspaces. Switch the workspace configuration, not the source files.

Start from the [parcel project](https://github.com/matthias-wong-dev/weaverstack-docs/tree/docs/progressive-journeys-refresh/examples/parcel-powerbi) and the [deployment prerequisites](deploy-pbip.md). For this exercise, use two existing disposable workspaces. Do not use a real production workspace for this exercise.

## 1. Map the two destinations

`workspace-dev.yml`:

```yaml
workspace: Parcel BI Development
targets:
  SemanticModel/Parcel: Parcel_Dev
  Report/Parcel: Parcel_Report_Dev
```

`workspace-prod.yml`:

```yaml
workspace: Parcel BI Production
targets:
  SemanticModel/Parcel: Parcel
  Report/Parcel: Parcel_Report
```

Edit the workspace names to your own. Model and Report target names are separate mappings. This example has inline data. For source-backed models, configure source mapping and an existing service connection as in [Connect a semantic model to source data](fabric-integration.md).

## 2. Deploy and refresh each pair

```bash
weaver check .
weaver build . --item PowerBI/Parcel --workspace-config workspace-dev.yml
weaver load SemanticModel/Parcel --workspace-config workspace-dev.yml
weaver build . --item PowerBI/Parcel --workspace-config workspace-prod.yml
weaver load SemanticModel/Parcel --workspace-config workspace-prod.yml
```

In the first workspace, `Parcel_Report_Dev` must bind to `Parcel_Dev`. In the second, `Parcel_Report` must bind to `Parcel`, not the development model. Both cards should show 2. Inspect each actual binding and refresh outcome; two successful command exits do not establish that the Reports query the right model.

The source retains its logical association. Destination-specific model identities belong in the deployed Report payload. Weaver compilation and deployment do not write the transformed model back into the native project.

For a model reading a managed Lakehouse or Warehouse, source-expression mapping and existing service connections are additional controls. Destination naming alone does not switch its data source.

## Cleanup

Delete only the two fixture-created Report/model pairs, Reports first. Do not delete either workspace or an item that existed before the exercise.

## Related tasks

- [Connect a model to a Fabric estate](fabric-integration.md).
- [Look up workspace configuration](../../reference/configuration-files/workspace-config.md).
- [Look up Report binding and connection boundaries](../../reference/power-bi/requirements-and-compatibility.md).
