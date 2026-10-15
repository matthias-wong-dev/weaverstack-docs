# Exact generated-file matrix

Runtime: `89e93c78f8497454b4544e7919567cc078dbad11`. Generated through the public API imported from the separately installed built wheel, with network connections refused. Fabric inventory/creation was an explicit offline boundary, not service execution.

Parameters: workspace `Example`, Lakehouse `Landing`, Warehouse `Operations`, native model/Report `Parcel` or `Sales` respectively. Different selected item names re-root their item-owned paths. `N` means the supported native model plus linked Report selection; the Report is deployed only when selected for Build.

Each matrix cell is the exact union of its named groups. Supporting/project-file groups are included, so this lists every generated file, not just selected source highlights. The companion JSON lists all 21 generated projects, including the seven no-example selections.

## Supporting and project files

### S1

```text
.weaver-initialise.json
Environment/Weaver.Environment/.platform
Environment/Weaver.Environment/Libraries/PublicLibraries/environment.yml
PowerBI/.gitkeep
README.md
workflow.yml
workspace-config.yml
```

### S2

```text
.weaver-initialise.json
Environment/Weaver.Environment/.platform
Environment/Weaver.Environment/Libraries/PublicLibraries/environment.yml
README.md
workflow.yml
workspace-config.yml
```

### S3

```text
.weaver-initialise.json
README.md
workflow.yml
workspace-config.yml
```

## Parcel

| Selection | Exact file groups | File count |
| --- | --- | --- |
| Lakehouse | `L` + `S1` | 12 |
| Warehouse | `W` + `S1` | 11 |
| native Power BI | `N` + `S3` | 17 |
| Lakehouse + Warehouse | `L` + `W` + `C` + `S1` | 18 |
| Lakehouse + native Power BI | `L` + `N` + `NL` + `S2` | 25 |
| Warehouse + native Power BI | `W` + `N` + `NW` + `S2` | 24 |
| Lakehouse + Warehouse + native Power BI | `L` + `W` + `N` + `C` + `NL` + `NW` + `S2` | 32 |

### Parcel — L

```text
Lakehouse/Landing/Files/Parcel__Events.py
Lakehouse/Landing/Tables/Parcel.CurrentStatus.sql
Lakehouse/Landing/Tables/Parcel__Event.py
Lakehouse/Landing/assumptions/Parcel.EventStatusIsKnown.sql
Lakehouse/Landing/tests/Parcel.CurrentStatusMatches.sql
```

### Parcel — W

```text
Warehouse/Operations/Parcel.CurrentStatus.sql
Warehouse/Operations/Parcel.StatusEvent.sql
Warehouse/Operations/assumptions/Parcel.StatusIsKnown.sql
Warehouse/Operations/tests/Parcel.CurrentStatusMatches.sql
```

### Parcel — N

```text
PowerBI/Parcel/Parcel.Report/definition.pbir
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/page.json
PowerBI/Parcel/Parcel.Report/definition/pages/ParcelOverview/visuals/DeliveryCount/visual.json
PowerBI/Parcel/Parcel.Report/definition/pages/pages.json
PowerBI/Parcel/Parcel.Report/definition/report.json
PowerBI/Parcel/Parcel.Report/definition/version.json
PowerBI/Parcel/Parcel.SemanticModel/definition.pbism
PowerBI/Parcel/Parcel.SemanticModel/definition/database.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/model.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/relationships.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Delivery.tmdl
PowerBI/Parcel/Parcel.SemanticModel/definition/tables/Depot.tmdl
PowerBI/Parcel/Parcel.pbip
```

### Parcel — C

```text
Warehouse/Operations/Parcel.LakehouseCurrentStatus.sql
Warehouse/Operations/shortcuts.yml
```

### Parcel — NL

```text
PowerBI/Parcel/ParcelLakehouse.tmdl
```

### Parcel — NW

```text
PowerBI/Parcel/ParcelWarehouse.tmdl
```

## Sales

| Selection | Exact file groups | File count |
| --- | --- | --- |
| Lakehouse | `L` + `S1` | 10 |
| Warehouse | `W` + `S1` | 11 |
| native Power BI | `N` + `S3` | 19 |
| Lakehouse + Warehouse | `L` + `W` + `C` + `S1` | 16 |
| Lakehouse + native Power BI | `L` + `N` + `NL` + `S2` | 25 |
| Warehouse + native Power BI | `W` + `N` + `NW` + `S2` | 26 |
| Lakehouse + Warehouse + native Power BI | `L` + `W` + `N` + `C` + `NL` + `NW` + `S2` | 32 |

### Sales — L

```text
Lakehouse/Landing/Files/Sales__Customers.py
Lakehouse/Landing/Tables/Sales__Customer.py
Lakehouse/Landing/assumptions/Sales__CustomerValid.py
```

### Sales — W

```text
Warehouse/Operations/Sales.Customer.sql
Warehouse/Operations/Sales.CustomerByRegion.sql
Warehouse/Operations/Sales.Region.sql
Warehouse/Operations/assumptions/Sales.CustomerByRegionValid.sql
```

### Sales — N

```text
PowerBI/Sales/Sales.Report/.platform
PowerBI/Sales/Sales.Report/definition.pbir
PowerBI/Sales/Sales.Report/definition/pages/overview/page.json
PowerBI/Sales/Sales.Report/definition/pages/overview/visuals/byRegion/visual.json
PowerBI/Sales/Sales.Report/definition/pages/overview/visuals/customers/visual.json
PowerBI/Sales/Sales.Report/definition/pages/overview/visuals/introduction/visual.json
PowerBI/Sales/Sales.Report/definition/pages/pages.json
PowerBI/Sales/Sales.Report/definition/report.json
PowerBI/Sales/Sales.Report/definition/version.json
PowerBI/Sales/Sales.SemanticModel/.platform
PowerBI/Sales/Sales.SemanticModel/definition.pbism
PowerBI/Sales/Sales.SemanticModel/definition/database.tmdl
PowerBI/Sales/Sales.SemanticModel/definition/model.tmdl
PowerBI/Sales/Sales.SemanticModel/definition/tables/Customer.tmdl
PowerBI/Sales/Sales.pbip
```

### Sales — C

```text
Warehouse/Operations/Sales.LakehouseCustomerByRegion.sql
Warehouse/Operations/shortcuts.yml
```

### Sales — NL

```text
PowerBI/Sales/SalesLakehouse.tmdl
```

### Sales — NW

```text
PowerBI/Sales/SalesWarehouse.tmdl
```

## Verified preservation

- Both named examples: every item-owned source from each smaller selection remains present with identical bytes in every containing larger selection: **24 proper subset pairs** through the installed wheel.
- **10 installed-wheel extension orders** (five for each example), with idempotent reruns. Source-level regressions additionally preserve changed Python business data, T-SQL data, native DAX, edited configuration and user README text; collisions and retargeting refuse before creation/writes.
- Native-only generation creates no catalogue Warehouse or Fabric Environment by default. Adding data items supplies the missing support without changing native source files.

No live Fabric Build/Load, DAX evaluation, model refresh, Report rendering or released-PyPI acceptance is asserted.
