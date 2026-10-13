# Power BI requirements and compatibility

This reference targets Weaver source revision [`74b4d15ee65ed2740593af1f4d459771b801b132`](https://github.com/matthias-wong-dev/weaverstack/tree/74b4d15ee65ed2740593af1f4d459771b801b132), not the older published `weaverstack 0.9.0` interface. No release number or date is assigned to these main-branch capabilities here.

## Runtime and service access

Power BI-only deployment does not require a Weaver catalogue Warehouse, Lakehouse, Spark session or Fabric Environment. It does require the Weaver Python package, an existing service workspace, appropriate Power BI licensing/capacity for the selected model mode, authentication and permissions to create/update/read the selected models and Reports. Free Desktop alone is not a service deployment environment. Ordinary Build can create missing selected Power BI items, but does not create the workspace.

Models use Fabric native-definition APIs for deployment and readback, and Power BI APIs for DAX queries and refresh. The configured identity must have rights for each operation and source it reaches; a valid definition is not permission to query. DAX execution also depends on tenant/query settings and supported service identity/model mode. Source credentials and gateways remain independently administered. Direct Lake and non-Power-BI Fabric workloads retain their Fabric/source/capacity prerequisites.

[Microsoft's semantic-model creation API](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/create-semantic-model) and [licensing reference](https://learn.microsoft.com/en-us/fabric/enterprise/licenses) describe platform requirements. Weaver's supported credential chain and notebook identity discovery are separate from licensing; do not enable tenant settings or create credentials merely to make a check pass.

`weaver initialise` provisions a catalogue Warehouse and Fabric Environment even for its Power BI scaffold. It is not the catalogue-free setup route. Use a minimal manual workspace configuration for that route.

## Mode matrix

| Capability | Without a catalogue | With catalogue/Fabric integration |
| --- | --- | --- |
| Deploy native model and Report | Supported; configured targets or explicit bindings | Supported; also publishes installation/certification records |
| Environment-specific names | Workspace configuration controls physical names | Configured Build destinations become recorded installed bindings |
| Linked Report | Its local model must be selected in the same Build | Selected model or an already certified installed model in the supported Report-only case |
| Unrelated authored `byConnection` | Retained as authored; no reverse mapping | Same boundary |
| Refresh | Explicit model/project selector; no persisted Weaver state | Installed ordering, results, LoadStatus/Log and stale selection |
| Policy/custom annotations/composition | Available subject to any source-dependent feature used | Available with managed metadata where required |
| DAX Assumptions | Source/file mode and DAX query rights | Source mode or installed recording |
| DAX versus SQL | File mode still requires supported Warehouse/Lakehouse source and rights | Installed or configured source reconciliation |
| Managed-source table generation | Not an external-source-free feature; requires resolved metadata/catalogue prerequisites | Build sources first, then generate model from managed metadata |
| Lineage/status/history/Health | No missing-catalogue substitute | Recorded evidence for managed/registered objects, not automatic discovery of the whole workspace |
| Installed regex/stale/ancestor/descendant selection | Not offered for catalogue-free refresh | Exact [Load selection](../operation-behaviour/load.md) within requested items |

Reports have no data Load or Test. Refresh/validate the semantic model. Source Lakehouse/Warehouse items and Power BI items use separate Build calls, even when authored in one project; a Workflow can sequence them.

## Native formats and preservation

Authored `.SemanticModel` definitions require TMDL `definition/` with versioned `definition.pbism`; `model.bim` is not an accepted authored base in this discovery path. Deployed readback uses TMSL for verification. Named standalone `<Model>.tmdl` definitions and same-name overlays are supported. Native `.Report` definitions require `definition.pbir` and exactly one complete payload: PBIR `definition/report.json` plus `definition/version.json`, or PBIR-Legacy root `report.json`. PBIP entrypoints validate their local Report references but are not compulsory for discovery. Cache files do not become definition payloads.

Weaver retains authored native content not explicitly changed by policy, overlays, annotations or source mapping. Deployment payloads can differ from source; authored files remain unchanged. Required edits and bindings are verified after deployment before certification. Fabric normalization can generate warnings; it is not evidence of lossless Desktop round-tripping. Do not assume every service-side RLS edit or partition survives a later source deployment. No public compiled `.SemanticModel`/TMDL export follows merely from native deployed output.

## Report binding

A same-name model in the local Power BI group takes precedence. Otherwise native `byPath` resolves a model in that group; an unrelated `byConnection` remains authored. An unresolved `byPath` fails. Linked payloads bind to the resolved physical model identity rather than blindly retaining the source connection. The source file is not rewritten.

A selected model is deployed and verified before linked Reports. Without a catalogue a linked Report-only selection is refused: include its model. With a catalogue, Report-only Build can use an already certified local model's recorded installation; the installed model must match the resolved target and source requirements. An as-authored unlinked Report may deploy separately. Readback verifies the Report definition and actual model binding, including service-normalized definitions.

Selected models deploy even when source signatures are unchanged. Catalogue-backed unchanged Report-only Build can skip work. Catalogue-free selections redeploy/verify; they have no catalogue fixed point. Ordinary Build can create missing selected models/Reports; read-only preview and bundle-only preparation require suitable existing destinations and do not take that provisioning path.

## Source mapping and connections

`data_sources` maps shared M expression names to typed `Warehouse/Name` or `Lakehouse/Name`. Repeatable `--data-source Expression=Warehouse/Name` (Python `data_sources=`) overrides configuration for that expression. Logical item targets resolve through selected Build bindings or configured `targets`; otherwise the typed name addresses the physical item. Expressions named by logical Warehouse/Lakehouse identity can use those mappings without an explicit override. Explicit mappings that reach no selected shared expression fail.

Supported SQL expressions are rebound to the source endpoint/database while retaining supported native options and query/navigation logic. Native Lakehouse connectors use workspace/item IDs where supported. This is opt-in typed shared-expression mapping, not arbitrary global replacement of M, every connector or an external database.

`Weaver.Source` names a managed table/view and records lineage. Authored partitions are retained; bare tables can generate columns/partitions from source metadata. Unknown external lineage is not inferred into a complete managed graph.

Definition/source mapping and credential binding are different steps. `--bind-data-sources` requests supported connection binding after deployment. Load checks/binds supported sources as needed before refresh. Weaver uses existing matching connections; it does not create gateways, credentials or shared connections. Missing/ambiguous connections and unsupported source forms can warn or fail at their operation boundary; a successful deployment does not establish refresh rights.

See [workspace configuration](../configuration-files/workspace-config.md), [Annotations](annotations.md), [Build](../operation-behaviour/build.md), [Load](../operation-behaviour/load.md) and [DAX validations](validations.md).
