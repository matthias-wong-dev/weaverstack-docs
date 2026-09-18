# Portable execution between desktop and Fabric

Portability has three separate layers in Weaver:

- **Project portability** means the same Weaver documents can be read from a local checkout or a Fabric notebook's built-in Resources.
- **Operation portability** means the public Build, Load, Test and Health operations can run through the desktop CLI or the Python API in a Fabric notebook.
- **Installed-artifact portability** means built Lakehouse modules and Warehouse SQL objects execute in Fabric without a desktop process reopening the project.

The host supplies workspace discovery, credentials, storage and Spark. The project keeps the same logical item and document identities, and the selected catalogue remains the record of the installed estate.

## 1. Project portability: use one source tree

Notebook Resources are ordinary project source. There is no notebook-specific Weaver project format. The documentation repository includes a coherent parcel estate under `examples/parcel-portability`. Copy the contents of that directory into the notebook's built-in Resources as `project`, preserving this tree:

```text
Parcel-Estate.Notebook/
└── Resources/
    └── builtin/
        └── project/
            ├── Lakehouse/
            │   └── Landing/
            │       ├── Files/
            │       ├── Tables/
            │       └── assumptions/
            └── Warehouse/
                └── Operations/
                    └── programmables/
```

Inside that notebook, `builtin/` is the root of its built-in Resources folder:

```python
from pathlib import Path

import weaver

project = Path("builtin") / "project"
catalogue = "Warehouse/<catalogue-name>"
items = [
    "Lakehouse/Landing=Lakehouse/<physical-lakehouse-name>",
    "Warehouse/Operations=Warehouse/<physical-warehouse-name>",
]

result = weaver.build(
    project,
    catalogue=catalogue,
    items=items,
)
if not result.succeeded:
    raise RuntimeError(result.errors)
```

Replace each angle-bracketed value with an existing physical item name in the notebook's workspace. The notebook's attached runtime must contain Weaver and any libraries imported by the project. Build installs Python definitions but does not call their authored `read()` methods.

Workspace and runtime resolution remain explicit rules rather than a separate notebook mode:

1. an explicit `workspace=` or `workspace_config=` selects the base workspace;
2. otherwise a supplied Session's workspace is used;
3. otherwise `workspace-config.yml` in the process working directory is used;
4. otherwise Weaver reads the current Fabric workspace from `notebookutils.runtime`.

An explicit `catalogue=` or `environment=` overrides that value on the selected base. Build, Load, Test and Health need a catalogue such as `Warehouse/<catalogue-name>`; discovering the notebook workspace does not invent one. A Fabric Environment may be written as `<environment-name>` in the operation workspace or `<owner-workspace>/<environment-name>` when Fabric permits a cross-workspace attachment. The qualification changes the Environment's owner, not the operation's workspace.

A notebook already executing in its attached workspace uses its active Spark session and notebook identity. It does not need an `environment=` argument merely to start a remote Livy session. Its attached runtime still needs Weaver and the project's Python dependencies. From a desktop, Lakehouse Python Load or Test instead needs a published Environment selected by configuration or `--environment`; Warehouse-only work does not, and Spark SQL can use the workspace's default Spark runtime. See [Session and runtime behaviour](../reference/operation-behaviour/session-runtime.md).

## 2. Move the project both ways with Fabric Git

Fabric Git can include a notebook's built-in Resources folder. The setting is optional and off by default; enable **Resources folder support in Git** for the notebook before expecting `Resources/builtin/project` in the repository. Fabric's [notebook source-control documentation](https://learn.microsoft.com/fabric/data-engineering/notebook-source-control-deployment) describes that setting and its size limit.

**Fabric to desktop:** commit the notebook and its built-in Resources from the Fabric workspace, then clone or update the connected branch. The same project is now an ordinary local directory. Build it without conversion:

```bash
weaver build \
  "Parcel-Estate.Notebook/Resources/builtin/project" \
  --workspace-config "<path-to-workspace-config.yml>"
```

The selected workspace configuration must bind `Lakehouse/Landing`, `Warehouse/Operations` and the catalogue to the intended physical estate. A local checkout does not inherit the notebook's attached workspace or Environment.

**Desktop to Fabric:** edit the files beneath `Resources/builtin/project`, commit and push them, then update the Fabric workspace from the connected branch. The notebook again resolves the project as `Path("builtin") / "project"` and can Build it with the first example.

`weaver fabric notebook push` is a different path: it transports a notebook definition, not local notebook Resources. Use Fabric Git when the project itself lives in built-in Resources. In either direction, the host changes; the Weaver documents do not.

## 3. Operation portability: change the entry point

The CLI and top-level Python package expose the core lifecycle through both entry points:

| Operation | Desktop CLI | Python in the attached Fabric workspace |
| --- | --- | --- |
| Build | `weaver build SOURCE` | `weaver.build(source, ...)` |
| Load | `weaver load ITEM...` | `weaver.load(items, ...)` |
| Test | `weaver test ITEM...` | `weaver.test(items, ...)` |
| Health | `weaver health --item ITEM` | `weaver.health(items, ...)` |

The entry point changes, but logical identities, catalogue selection, installed bindings and the operation's selection rules do not. This is not a claim that every CLI command has a notebook counterpart. CLI interaction, confirmation and output remain CLI concerns.

Mirror and Wipe are also public Python operations. They retain their operation-specific planning and destructive boundaries, so they are not folded into the routine lifecycle shorthand above: inspect a Mirror or Wipe plan using the documented operation interface before executing it. See [Mirror behaviour](../reference/operation-behaviour/mirror.md) and [Wipe behaviour](../reference/operation-behaviour/wipe.md).

In an attached Fabric notebook, each top-level operation discovers the current workspace and uses the active Spark runtime and notebook identity. The catalogue remains explicit because workspace discovery does not invent one. Build binds the project items to physical Fabric items; Load, Test and Health then select the installed logical items:

```python
from pathlib import Path

import weaver

project = Path("builtin") / "project"
catalogue = "Warehouse/<catalogue-name>"
items = ["Lakehouse/Landing", "Warehouse/Operations"]
bindings = [
    "Lakehouse/Landing=Lakehouse/<physical-lakehouse-name>",
    "Warehouse/Operations=Warehouse/<physical-warehouse-name>",
]

build_result = weaver.build(
    project,
    items=bindings,
    catalogue=catalogue,
)
if not build_result.succeeded:
    raise RuntimeError(build_result.errors)

load_report = weaver.load(items, catalogue=catalogue)

test_report = weaver.test(items, catalogue=catalogue)
if not test_report.succeeded:
    raise RuntimeError(f"Test {test_report.status}")

health_report = weaver.health(items, catalogue=catalogue)
```

No desktop credential or `environment=` argument is needed for this attached-workspace path. The attached runtime must still contain Weaver and the project's Python dependencies. Supplying a [Session](../reference/python/session.md) is optional when a caller needs explicit context reuse or control.

The corresponding desktop sequence uses the configuration that binds the same logical items and catalogue:

```bash
weaver build \
  "Parcel-Estate.Notebook/Resources/builtin/project" \
  --workspace-config "<path-to-workspace-config.yml>"
weaver load Lakehouse/Landing Warehouse/Operations \
  --workspace-config "<path-to-workspace-config.yml>"
weaver test Lakehouse/Landing Warehouse/Operations \
  --workspace-config "<path-to-workspace-config.yml>"
weaver health \
  --item Lakehouse/Landing \
  --item Warehouse/Operations \
  --workspace-config "<path-to-workspace-config.yml>"
```

Build records the physical bindings in the selected catalogue. Load, Test and Health use those installed bindings; changing the current `targets` mapping does not retarget an installed generation until Build installs it.

The rest of the CLI is deliberately not folded into this table:

- `weaver.initialise()` is a public Python function as well as a CLI setup command. It creates project files and requested Fabric items; it is not an installed-estate operation.
- Doctor and frozen-bundle Install are CLI commands. `doctor` and `install` are not exports of the top-level `weaver` Python API.
- Check is local project validation rather than a hosted estate operation.
- `weaver fabric environment publish` and `weaver fabric notebook push|run` are CLI helpers for Fabric items. They have no top-level Python operation counterparts.
- A CLI workflow is represented in Python by an explicit sequence of public operation calls. Each call can discover the attached notebook context as shown above.

See [Python operations](../reference/python/operations.md) and the [CLI reference](../reference/cli.md) for exact signatures and selection rules.

## 4. Installed-artifact portability: run built work in Fabric

Build deploys Lakehouse load modules under the target Lakehouse's `Files/_/Load` tree. Python-authored Folders and Tables remain importable modules. A Spark SQL Table is compiled into a generated Python module with the same `Schema__Object` class spelling.

The following notebook code assumes that Build installed the checked-in `examples/parcel-portability` project into the notebook's attached physical `Lakehouse/Landing`. That project contains the Python Folder `Parcel.Events`, Python Table `Parcel.Event`, Spark SQL Table `Parcel.CurrentStatus` and Python Assumption `Parcel.HasDestination` used below. Replace `<catalogue-name>` with the catalogue Warehouse for that installed estate:

```python
import sys

import weaver

catalogue = "Warehouse/<catalogue-name>"
destination = weaver.default_lakehouse(spark)
runtime_root = f"{destination.files_root()}/_/Load"
if runtime_root not in sys.path:
    sys.path.insert(0, runtime_root)

from Files.Parcel__Events import Parcel__Events
from Tables.Parcel__CurrentStatus import Parcel__CurrentStatus
from Tables.Parcel__Event import Parcel__Event
from assumptions.Parcel__HasDestination import Parcel__HasDestination

folder_result = Parcel__Events(
    spark,
    lakehouse=destination,
    catalogue=catalogue,
).load()

python_rows = Parcel__Event(
    spark,
    lakehouse=destination,
).read()
python_load = Parcel__Event(
    spark,
    lakehouse=destination,
    catalogue=catalogue,
).load()

spark_sql_load = Parcel__CurrentStatus(
    spark,
    lakehouse=destination,
    catalogue=catalogue,
).load()

violations = Parcel__HasDestination(
    spark,
    lakehouse=destination,
).read()
validation_report = weaver.test(
    "Lakehouse/Landing",
    name="Parcel.HasDestination",
    catalogue=catalogue,
)
```

The four call forms have different state boundaries:

| Call | Catalogue anchor | Recorded effect |
| --- | --- | --- |
| Installed Table, Folder or Assumption `read()` | Not required | Runs the installed primitive directly. It does not advance a bookmark or write Load/Test evidence. |
| Installed Table or Folder `load()` | Required | Resolves the installed identity and records Load status, statistics and log evidence. A clean load advances its bookmark. |
| Installed validation `run()` | Required | Resolves the installed validation and records Test status and log evidence. |
| `weaver.test(...)` | Required | Selects installed validation work through the catalogue, applies normal Test operation semantics and records estate evidence. |

A freestanding object can call `read()`, but `load()` and validation `run()` refuse to execute without a catalogue anchor. Direct `read()` is therefore useful for inspecting authored logic; it is not a substitute for the recorded Load or Test lifecycle.

Warehouse installation is native too. The parcel Warehouse example installs the `Parcel.StatusEvent` Table, its generated load procedure and the `Parcel.CurrentStatus` View. A Warehouse Assumption becomes a validation procedure, and an authored programmable such as `Parcel.RefreshSummary` remains an ordinary stored procedure. After Build, those SQL objects live and execute in the target Warehouse; no desktop Weaver process needs to remain alive. Build, Load and Test use the generated procedures, while callers can query Views or invoke authored programmables through the Warehouse SQL endpoint.

## 5. Keep the lifecycle in Fabric

A complete hosted path can remain inside Fabric:

```text
Fabric Git
    ↓
Notebook built-in Resources
    ↓
Fabric notebook with an attached runtime
    ↓
weaver.build() → weaver.load() → weaver.test() → weaver.health()
    ↓
Fabric-native Lakehouse and Warehouse state
```

Desktop Python is optional in this path. A desktop remains useful for local editing, CI/CD and remote orchestration, but the project can be stored through Fabric Git, built and operated from a Fabric notebook, and executed against the installed estate without a personal machine running Python.

The same notebook can be run by Fabric's notebook job scheduler or from a Fabric pipeline. That makes Fabric both the execution host and the scheduler for the shown sequence; it does not change Weaver's operation semantics or replace the catalogue. Configure scheduling, identity, capacity and retry policy in Fabric rather than inferring them from a successful interactive run. See Microsoft's [Fabric job scheduler](https://learn.microsoft.com/fabric/fundamentals/job-scheduler) documentation for that platform boundary.
