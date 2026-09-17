# Advanced

The following workflows are implemented but need dedicated operating guides:

- generating a bundle with `weaver build --bundle-only` and installing it separately;
- running several commands through one `weaver session`;
- defining ordered command sequences in `workflow.yml`;
- publishing a released or development build into a Fabric Environment;
- mirroring an installed catalogue into another estate;
- using stale-only loads and explicit freshness cutoffs;
- running Weaver from a Fabric notebook;
- managing Fabric notebooks and capacities through `weaver fabric`.

The [CLI reference](../reference/cli.md) gives the current command grammar. The [coverage gap map](../gaps.md) names the future guide and contract page for each workflow. This section does not imply that internal planner, catalogue or transport modules are public extension points.
