# Unbind behaviour

Unbind deletes a catalogue's claims for explicitly named physical Lakehouses, Warehouses, semantic models or Reports. It does not empty or delete those items, deploy a definition, refresh a model, remove a connection or alter source data. The catalogue is retained.

## Selection and preflight

At least one `Lakehouse/Name`, `Warehouse/Name`, `SemanticModel/Name` or `Report/Name` is required. Names identify physical targets in the selected workspace, not logical project items; repeated targets are deduplicated. A resolved catalogue is required. The catalogue cannot be a target.

Planning reads catalogue installations and the workspace inventory. Every selected target must have a recorded installation. The plan lists every logical item recorded against each selected physical target and whether the target still exists. Missing physical items can still have claims removed. Unselected targets are not added through dependencies.

## Confirmation and execution

The CLI displays the settled plan. It asks for confirmation if at least one selected item still exists in Fabric; claims for absent targets alone do not require it. Review and confirm the scope if correct. In unattended execution use `--yes` when authorisation is required. `--dry-run` returns the plan without claim deletion.

Execution removes selected installation, certification, dictionary, dependency, semantic metadata and operational-state claims through catalogue DML. It uses no physical target mutation client. The deletion plan is computed for all selected installations together so shared catalogue tables are handled in dependency order. Unselected claims remain.

A successful result contains the plan and removed `logical_items` (rendered as `unbound` in the mapping). A failed deletion raises a command error. There is no physical-item rollback to perform because Unbind changes no physical item; do not assume an operation-wide transaction over every catalogue action.

## Resulting state

The selected logical items no longer participate as installed items in that catalogue's Load, Test or Health. Their Fabric definitions and data remain as they were, and linked Reports or external consumers are not reconfigured. A subsequent Build is a new reconciliation against the remaining physical state, not automatic adoption of retained data. Keep irreplaceable retained data outside a managed Build boundary.

Python offers `weaver.plan_unbind(...)` and `weaver.unbind(plan=...)`, or direct planning arguments to `unbind`. A settled plan cannot be combined with planning arguments; `session` and `dry_run` still control execution.

See [`weaver unbind`](../cli/unbind.md), [Wipe](wipe.md), [Python operations](../python/operations.md) and [Catalogue schema](../catalogue-schema.md).
