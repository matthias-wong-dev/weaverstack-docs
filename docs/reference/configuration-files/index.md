# Configuration files

Weaver uses three independent file formats:

| File | Selects or defines | Does not do |
| --- | --- | --- |
| [`workspace-config.yml`](workspace-config.md) | A Fabric workspace, catalogue, optional runtime, optional Mirror source, execution settings and logical-to-physical item bindings | Declare Weaver documents, publish an Environment or run Mirror |
| [`workflow.yml`](workflow.md) | Named, ordered lists of ordinary Weaver CLI commands | Define another command language or make the commands transactional |
| [Fabric Environment definition](fabric-environment.md) | The files and Python packages published to one Fabric Environment | Select a project estate or install Weaver documents |

Keep four decisions separate:

1. **Physical bindings** — `workspace`, `catalogue` and `targets` say where an estate is installed.
2. **Configuration selection** — discovery, `--workspace-config`, `--workspace` and a Session decide which workspace configuration an operation receives.
3. **Environment publication** — `weaver fabric environment publish` creates or updates a Fabric Environment. The workspace configuration's `environment` key only selects an already published runtime for Spark work.
4. **Mirror source configuration** — `mirror` names the source catalogue read by Mirror and by later mirrored-state reads. It is not a second workspace binding and loading the file does not run Mirror.

Selecting another workspace configuration can change every physical binding while the project, logical item and document identities remain unchanged. See [Shared selection and identity](../operation-behaviour/shared-selection-and-identity.md) for those identity forms.
