# Advanced

Use these routes when the ordinary Build, Load and Test cycle is not the whole task.

- [Mirror an estate for specialised development](specialised-estate-mirroring.md): branch installed state, borrow selected data or materialise one item locally.
- [Push and run a Fabric notebook](fabric-notebooks.md): deploy a local notebook definition and start it with an explicit Lakehouse and Environment.
- [Control a Fabric capacity](fabric-capacity.md): inspect, resume and suspend the Azure capacity around a workload.

These routes change different layers. Mirror reconstructs catalogue and item destinations. Notebook commands manage and execute a Fabric Notebook but do not Build project declarations. Capacity commands act on the Azure resource and do not read or write a Weaver catalogue.

Use the [Guides](../guides/index.md) for ordinary authoring and estate operation. The [CLI reference](../reference/cli.md) owns complete command syntax; [Contracts](../contracts/index.md) owns operation behaviour and failure boundaries.
