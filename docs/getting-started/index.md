# Start here

Install Weaver, then start with the Fabric item you already work in. Each item has its own first task; you do not need to build a whole estate first.

1. [Install Weaver](installation.md) and sign in.
2. Pick a first task:
    - [Warehouse: a SQL Table and View](../warehouse/first-project.md). This is the shortest route to a first result: T-SQL only, no Spark runtime to publish. If you have no preference, start here.
    - [Lakehouse: a CSV file into a Delta Table](../lakehouse/python.md), using Python and Spark SQL.
    - [Semantic model: deploy native TMDL](../semantic-models/native-tmdl.md). This works in an ordinary Power BI workspace without a Fabric Warehouse or Catalogue; see the [two Power BI operating modes](../semantic-models/index.md#two-ways-to-use-weaver-with-power-bi).
    - [Report: deploy a native Report with its model](../reports/deploy.md).

Every task uses the same `parcel` project. A later task adds to the folder you already have, so you can go from a Warehouse to a Lakehouse to a model without starting again.

Once two items work, [Coordinate your estate](../estate/index.md) shows how to connect them, map development and production, and read their results together.

<span id="getting-started"></span>
