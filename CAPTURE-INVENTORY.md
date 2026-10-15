# Capture after editorial approval

Capture against the matching installed release and disposable destinations, using the final page commands. Record real terminal output and service views, not mock results. The named-example verification used offline inventory and metadata boundaries; it did not deploy, load or refresh Fabric items.

| Capture | Continuing project | Page |
| --- | --- | --- |
| Initialise, inspect StatusEvent, Check, Build, Load and the two CurrentStatus rows | `weaver initialise --warehouse Operations --example Parcel` in `parcel` | [First Warehouse](docs/warehouse/first-project.md) |
| Folder → Python Table → Spark SQL and validations | `weaver initialise --lakehouse Landing --example Parcel`; keep its generated files | [Python pipeline](docs/lakehouse/python.md), [Spark SQL](docs/lakehouse/spark-sql.md), [Tests](docs/lakehouse/tests.md) |
| Changing external CSV, StatusFiles changes, LiveStatus upsert/delete and bookmark | Add the complete StatusFiles/LiveStatus declarations to Landing; retain Event/CurrentStatus and keep ParcelSourceArchive outside managed targets | [Loading changes and bookmarks](docs/lakehouse/incremental.md) |
| Changing external SQL records, LiveStatus upsert/delete and bookmark | Add LiveStatus and the physical Shortcut to Operations; retain StatusEvent/CurrentStatus and keep ParcelSource outside managed targets | [Warehouse changes](docs/warehouse/incremental.md) |
| Extension preserves existing code; cross-item Load and LakehouseCurrentStatus rows | Add Operations to the working Landing project, or Landing to Operations; no project replacement | [Connected items](docs/estate/connected-items.md) |
| Development mappings, Health, selected work and concurrency | Continue Landing/Operations with `workspace-development.yml` | [Mappings](docs/estate/environments.md), [Health](docs/estate/catalogue-and-health.md), [Operation](docs/estate/operate.md), [Selections](docs/estate/selective-runs.md), [Concurrency](docs/estate/concurrency.md) |
| Model-only Build/refresh, Delivery Count DAX, field visibility before/after AutoHideForeignKeys | Add the native Parcel model and Report with Initialise; preserve the original inline partitions | [Native TMDL](docs/semantic-models/native-tmdl.md) |
| Managed-source refresh and DAX/SQL reconciliation, with the inline model still working | Additional ParcelWarehouse model, loaded Operations source and an existing approved service connection | [Managed sources](docs/semantic-models/managed-sources.md), [Validation](docs/semantic-models/validation.md) |
| Native Report card and its selected semantic-model binding in each environment | The same Parcel native pair; both disposable environment configurations | [Report deployment](docs/reports/deploy.md), [Report environments](docs/reports/environments.md) |
| Mirror plan, explicit confirmation and resulting Health | Existing disposable destinations and the page's same-workspace prerequisites; agree destructive reset/re-mirror scope separately | [Mirror](docs/estate/mirror.md) |

Publication remains held for a matching PyPI release and Matthias's explicit approval. Capturing output does not authorise publication, new capacity, tenant changes or destructive recovery.

## Capture and presentation convention

Capture **actual human-readable CLI output** from the final documented commands, not invented examples or machine-readable JSON substituted for the normal terminal view. Record the exact command, package version, exit status and relevant example/workspace context with each transcript. Preserve the raw UTF-8 output; preserve ANSI escape codes too when available, but do not block capture if the environment emits plain text. Scrub credentials, tokens, tenant identifiers and unrelated private paths before committing any output.

After capture, render selected excerpts directly beside their commands in the existing documentation. Terminal transcripts should be selectable text in accessible, responsive `pre`/HTML panels. Retrospectively style known statuses, glyphs, sections and messages using the site's shared CSS; colouring is presentation only and must not alter the actual words, values, order, counts or outcomes. Do not fake additional statuses, glyphs or timings. Mark any truncation explicitly, and keep complete sanitised transcripts available for verification.

Use one coherent project from Initialise through Check, Build, Load, Test and Health, then continue it through later tasks. Keep each displayed excerpt short enough to demonstrate the result; replace redundant "should print/show" prose rather than appending large output blocks beneath it. Use diagrams for relationships and actual Fabric/Power BI screenshots only where they clarify something CLI text cannot.

For live capture, use existing authorised disposable Fabric resources and service connections only. Do not change tenant settings or use production data. Mirror, Wipe, reset or other destructive paths need explicit scope approval before execution; their planning/output examples can be captured independently where supported.
