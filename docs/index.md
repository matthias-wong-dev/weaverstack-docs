# Weaver

Keep ordinary Python, SQL and native Power BI projects. Weaver handles the engineering around deploying definitions, running data work and checking its result.

## Start with your work

**An existing Power BI project**

[Deploy a native model and linked Report](basics/power-bi/deploy-pbip.md), then use [development and production targets](basics/power-bi/environments.md). A catalogue Warehouse, Lakehouse and Spark runtime are not prerequisites for this route. The Power BI service licence, access and permissions still matter.

**A small Fabric pipeline**

[Build your first Fabric project](getting-started/first-project.md): one Warehouse Table, one Test, and the Build → Load → Test result. Or choose [Lakehouse Python](basics/lakehouse-python.md) or [Warehouse SQL](basics/warehouse-pipeline.md) for an authoring task.

[Installation](getting-started/installation.md) identifies the supported snapshot and each route's prerequisites.

## Run, inspect or look something up

[Run and inspect an estate](basics/run-and-inspect-estate.md) covers normal operation. [Recovery](basics/recover-failed-work.md) helps choose a new run against partial state. [How Weaver works](core-concepts/how-weaver-works.md) explains the model; [Design philosophy](core-concepts/design-philosophy.md) explains the engineering choices.

Use [Reference](reference/index.md) for exact commands, APIs, configuration and operation boundaries. Optional controls in [Advanced](advanced/index.md) are available when a problem needs them, not prerequisites for a first result.
