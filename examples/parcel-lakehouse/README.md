# Lakehouse journey checkpoints

These documents support the continuous [Python → Spark SQL → validation journey](../../docs/lakehouse/python.md). Initialise a disposable project as shown on the Python page; it creates the catalogue/target bindings and Environment definition. Copy only the documents for the checkpoint you need into that project's `Lakehouse/Landing` directory. Do not replace its generated workspace configuration or initialise again between pages.

| Checkpoint | Files to copy | Expected Fabric outcome, not locally observed |
|---|---|---|
| Python | `Files/Parcel__Events.py`, `Tables/Parcel__Event.py` | Folder publishes events.csv; Event has three rows |
| Spark SQL | Python files plus `Tables/Parcel.CurrentStatus.sql` | CurrentStatus has P-1001 In transit/Central and P-1002 Delivered/South |
| Validation | Above plus `tests/Parcel.CurrentStatusMatches.sql`, `assumptions/Parcel.EventStatusIsKnown.sql` | Both validations succeed with zero findings |

`Tables/Parcel.ServiceLevel.sql` is an existing independent reference-data example. It is not required for this route and is retained unchanged. Copying the entire item includes that Table too.

The incremental page deliberately switches to the existing `examples/parcel-incremental` complete mutable-source variation in `Lakehouse/Tracking`. It does not replace this Python Event with a second SQL seed. Local Check only establishes authored shape; runtime publication, Build, Load, Test and SQL endpoint readback require Fabric.
